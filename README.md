# felix-lambert.github.io

Bilingual (English / French) portfolio and CV of Felix Lambert, built
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

## Local preview

```sh
bundle install
bundle exec jekyll serve
```

## CV PDF

`download/Felix-Lambert-CV.pdf` is the hand-made CV, served for both
languages. To update it, replace the file (keep the name).
