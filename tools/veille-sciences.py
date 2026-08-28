#!/usr/bin/env python3
"""Veille sur les découvertes en physique et en chimie, à partir de flux triés.

Interroge une dizaine de flux RSS/Atom de rédactions scientifiques (Nature,
Science, Quanta, Phys.org, ScienceDaily, NASA, ESA, Nobel), garde ce qui relève
de la physique ou de la chimie, écarte le bruit éditorial (podcasts, tribunes,
nécrologies…) et ne ressort que les nouveautés jamais vues lors des passages
précédents.

Usage:  python3 tools/veille-sciences.py [--jours 8] [--max 40] [--json]
                                         [--sans-etat] [--tout]

  --jours N    ne garder que les articles des N derniers jours (défaut : 8)
  --max N      nombre maximum d'entrées retournées (défaut : 40)
  --json       sortie JSON (par défaut : Markdown lisible)
  --sans-etat  ne pas lire ni écrire tools/veille-etat.json (essai à blanc)
  --tout       ignorer l'état : ressortir même ce qui a déjà été vu

L'état (tools/veille-etat.json) mémorise les liens déjà sortis, pour qu'un
article ne soit proposé qu'une fois. Sortie 0 même sans nouveauté ; sortie 1
seulement si aucun flux n'a répondu (utilisable en cron / CI).
"""
import argparse
import hashlib
import html
import json
import os
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ETAT = os.path.join(RACINE, 'tools', 'veille-etat.json')
UA = {'User-Agent': 'veille-sciences/1.0 (felix-lambert.github.io)'}
MAX_ETAT = 3000

# « cible » : flux déjà limité à la physique ou à la chimie, aucun filtrage
# thématique nécessaire. Les autres sont généralistes et passent au tamis.
FLUX = [
    ('Nature',        'https://www.nature.com/nature.rss',                          False),
    ('Science',       'https://www.science.org/rss/news_current.xml',               False),
    ('Quanta',        'https://api.quantamagazine.org/feed/',                       False),
    ('Phys.org',      'https://phys.org/rss-feed/physics-news/',                    True),
    ('Phys.org',      'https://phys.org/rss-feed/chemistry-news/',                  True),
    ('Phys.org',      'https://phys.org/rss-feed/space-news/',                      False),
    ('ScienceDaily',  'https://www.sciencedaily.com/rss/matter_energy/physics.xml', True),
    ('ScienceDaily',  'https://www.sciencedaily.com/rss/matter_energy/chemistry.xml', True),
    ('NASA',          'https://www.nasa.gov/news-release/feed/',                    False),
    ('ESA',           'https://www.esa.int/rssfeed/Our_Activities/Space_Science',   False),
    ('Nobel',         'https://www.nobelprize.org/feed/',                           False),
]

THEME = re.compile(r'''quantum|particle|physic|chemi|molecul|atom|nucle|laser|
    supercond|magnet|gravitational|black.hole|neutrino|quark|fusion|plasma|
    photon|electron|proton|isotope|antimatter|dark.matter|dark.energy|
    relativity|thermodynam|semiconduct|graphene|batter|catalys|polymer|crystal|
    material|superfluid|entangle|qubit|spectro|synthesi|periodic.table|element|
    telescope|exoplanet|galax|cosmic|universe|astronom|collider|accelerator|
    reaction|bond|alloy|nanomat''', re.I | re.X)

BRUIT = re.compile(r'''podcast|opinion|obituar|book review|correction|retraction|
    career|jobs|editorial|daily briefing|news round.?up|quiz|comment:|letter to|
    in memoriam|webinar|newsletter|this week in|nature podcast''', re.I | re.X)

# Les flux généralistes (Nature, Science) charrient beaucoup de biologie, que
# « molecular » ou « synthesis » suffisent à faire passer pour de la chimie.
BIO = re.compile(r'''sperm|gene\b|genom|protein|cell\b|cells\b|cancer|patient|
    neuron|brain|immun|microbio|bacteri|virus|vaccin|clinical|enzyme|rna|dna|
    species|ecosystem|climate polic|forest|insect|primate|evolutionary''',
    re.I | re.X)

DUR = re.compile(r'''quantum|particle|physic|laser|supercond|magnet|neutrino|
    quark|photon|qubit|black.hole|gravitational|antimatter|dark.matter|
    dark.energy|collider|accelerator|isotope|plasma|semiconduct|graphene|
    crystal|catalys|polymer|alloy|periodic.table|spectroscop|telescope|
    exoplanet|galax|cosmic''', re.I | re.X)

DECOUVERTE = re.compile(r'''first|discover|detect|observ|breakthrough|record|
    confirm|unprecedented|solved|evidence|measur|reveal|new state|created|
    synthesi|achiev|milestone|for the first time''', re.I | re.X)


# On lit le XML à l'expression régulière plutôt qu'avec xml.etree : les flux
# RSS/Atom sont générés par des machines et restent réguliers, et cela évite de
# dépendre de pyexpat, absent ou cassé sur certaines installations de Python.
BLOC = re.compile(r'<(item|entry)[\s>].*?</\1>', re.S | re.I)


def champ(bloc, *balises):
    for b in balises:
        m = re.search(r'<%s(?:\s[^>]*)?>(.*?)</%s>' % (b, b), bloc, re.S | re.I)
        if m and m.group(1).strip():
            return decdata(m.group(1))
    return ''


def decdata(t):
    m = re.search(r'<!\[CDATA\[(.*?)\]\]>', t, re.S)
    return (m.group(1) if m else t).strip()


def lien_de(bloc):
    """RSS met l'URL dans le texte de <link>, Atom dans son attribut href."""
    m = re.search(r'<link(?:\s[^>]*)?>\s*(?:<!\[CDATA\[)?\s*(https?://[^<\]\s]+)',
                  bloc, re.I)
    if m:
        return m.group(1)
    for m in re.finditer(r'<link\b([^>]*)/?>', bloc, re.I):
        attrs = m.group(1)
        if re.search(r'rel\s*=\s*["\'](?!alternate)', attrs, re.I):
            continue
        h = re.search(r'href\s*=\s*["\']([^"\']+)', attrs)
        if h:
            return h.group(1)
    m = re.search(r'<guid(?:\s[^>]*)?>\s*(https?://[^<\s]+)', bloc, re.I)
    return m.group(1) if m else ''


def nettoie(brut):
    return ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', brut or '')).split())


def date_de(brut):
    if not brut:
        return None
    try:
        d = parsedate_to_datetime(brut)
    except (TypeError, ValueError):
        try:
            d = datetime.fromisoformat(brut.replace('Z', '+00:00'))
        except ValueError:
            return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def lis_flux(source, url, cible):
    """Renvoie (liste d'entrées, erreur éventuelle)."""
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            brut = r.read().decode(r.headers.get_content_charset() or 'utf-8',
                                   errors='replace')
    except (urllib.error.URLError, OSError, UnicodeError) as e:
        return [], '%s (%s) : %s' % (source, url, e)

    entrees = []
    for m in BLOC.finditer(brut):
        bloc = m.group(0)
        titre = champ(bloc, 'title')
        lien = lien_de(bloc)
        if not titre or not lien:
            continue
        entrees.append({
            'source': source,
            'titre': nettoie(titre),
            'lien': lien.strip(),
            'resume': nettoie(champ(bloc, 'description', 'summary',
                                    'content:encoded', 'content'))[:600],
            'date': date_de(champ(bloc, 'pubDate', 'published', 'updated',
                                  'dc:date', 'date')),
            'cible': cible,
        })
    return entrees, None


def pertinent(e):
    blob = '%s %s' % (e['titre'], e['resume'])
    if BRUIT.search(blob):
        return False
    if e['cible']:
        return True
    if BIO.search(blob) and not DUR.search(blob):
        return False
    return bool(THEME.search(blob))


def score(e):
    """Plus c'est haut, plus ça ressemble à une découverte datable."""
    blob = f"{e['titre']} {e['resume']}"
    n = len(DECOUVERTE.findall(blob))
    if e['source'] in ('Nature', 'Science', 'Nobel'):
        n += 2
    if e['source'] == 'Quanta':
        n += 1
    return n


def charge_etat():
    try:
        with open(ETAT) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {'vus': [], 'dernier_passage': None}


def cle(e):
    return hashlib.sha1(e['lien'].encode()).hexdigest()[:16]


def markdown(items, quand):
    lignes = [f'# Veille physique / chimie — {quand:%d/%m/%Y}', '']
    if not items:
        lignes.append('Aucune nouveauté depuis le dernier passage.')
        return '\n'.join(lignes)
    for e in items:
        d = e['date'].strftime('%d/%m/%Y') if e['date'] else 'date inconnue'
        lignes += [f"## {e['titre']}",
                   f"*{e['source']} — {d}*",
                   '',
                   e['resume'] or '(pas de résumé)',
                   '',
                   e['lien'],
                   '']
    return '\n'.join(lignes)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--jours', type=int, default=8)
    p.add_argument('--max', type=int, default=40)
    p.add_argument('--json', action='store_true')
    p.add_argument('--sans-etat', action='store_true')
    p.add_argument('--tout', action='store_true')
    args = p.parse_args()

    with ThreadPoolExecutor(max_workers=8) as ex:
        resultats = list(ex.map(lambda f: lis_flux(*f), FLUX))

    entrees, erreurs = [], []
    for lot, err in resultats:
        entrees += lot
        if err:
            erreurs.append(err)
    for e in erreurs:
        print(f'  ! flux injoignable : {e}', file=sys.stderr)
    if not entrees:
        print('Aucun flux n\'a répondu.', file=sys.stderr)
        return 1

    limite = datetime.now(timezone.utc) - timedelta(days=args.jours)
    etat = {'vus': [], 'dernier_passage': None} if args.sans_etat else charge_etat()
    vus = set() if args.tout else set(etat.get('vus', []))

    gardes, cles_vues = [], set()
    for e in entrees:
        k = cle(e)
        if k in vus or k in cles_vues or not pertinent(e):
            continue
        if e['date'] and e['date'] < limite:
            continue
        cles_vues.add(k)
        e['score'] = score(e)
        gardes.append(e)

    gardes.sort(key=lambda e: (-e['score'], -(e['date'].timestamp() if e['date'] else 0)))
    gardes = gardes[:args.max]

    maintenant = datetime.now(timezone.utc)
    if not args.sans_etat:
        etat['vus'] = (etat.get('vus', []) + [cle(e) for e in gardes])[-MAX_ETAT:]
        etat['dernier_passage'] = maintenant.isoformat(timespec='seconds')
        with open(ETAT, 'w') as f:
            json.dump(etat, f, indent=1)

    if args.json:
        print(json.dumps([{**e, 'date': e['date'].isoformat() if e['date'] else None}
                          for e in gardes], ensure_ascii=False, indent=1))
    else:
        print(markdown(gardes, maintenant))
    return 0


if __name__ == '__main__':
    sys.exit(main())
