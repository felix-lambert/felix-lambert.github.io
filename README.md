# felix-lambert.github.io

Bilingual (English / French) portfolio, CV and blog of Felix Lambert, built
with Jekyll and published on GitHub Pages.

## Editing content

Everything shown on the home page, the CV page and the PDF comes from
`_data/`:

| File                  | What it drives                                   |
| --------------------- | ------------------------------------------------ |
| `_data/profile.yml`   | name, title, tagline, availability, links, stats |
| `_data/experience.yml`| work history (EN + FR copy per entry)            |
| `_data/projects.yml`  | project cards (`ongoing: true` shows on the home) |
| `_data/skills.yml`    | skill groups on the CV                           |
| `_data/education.yml` | degrees                                          |
| `_data/i18n.yml`      | UI strings for both languages                    |

Blog posts live in `all_collections/_posts/`. Add `lang: fr` to a post
written in French (English is the default).

## Local preview

```sh
bundle install
bundle exec jekyll serve
```

## Regenerating the CV PDFs

The PDFs in `download/` are printed from the `/cv/` and `/fr/cv/` pages
with headless Chromium (Playwright). After editing the data files:

```sh
tools/build-cv-pdf.sh
```

The PDF build passes `_config_pdf.yml`, which is the only build that
renders the phone number.
