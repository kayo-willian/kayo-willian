# GO BEYOND — ゴー・ビヨンド

Personal website, cultural archive and project showcase. Not a résumé or a copy of the profile README.

## Delivery roadmap

| Stage | Scope | Status |
| --- | --- | --- |
| 01 FOUNDATION | Isolated site directory, content catalog, reproducible static build, validation and Pages workflow | In progress: CI and Pages configuration verification pending |
| 02 IDENTITY | Original Japanese/editorial, underground, analog and Afrofuturist visual system | Planned |
| 03 HOME | Personal introduction, visible navigation, four supplied quotations on the homepage (source and rights review before publication) | Planned |
| 04 PROJECTS | Inventory all public repositories; individual pages, evidence, architecture and OSS contributions | Planned |
| 05 SOUND ARCHIVE / GOATS | Full confirmed artist catalog; Michael Jackson and Kanye West together; text-only Verocai, Péricles and Belo | Planned |
| 06 FIGHT CLUB | All 18 confirmed fighters; chosen display names; PRIDE-inspired visual language; four featured fighters | Planned |
| 07 SEINEN | All seven confirmed manga | Planned |
| 08 HERETICS | All nine confirmed comics characters | Planned |
| 09 UNDERGROUND | Leon (Mr. Robot), hacker culture, Unix and independent web | Planned |
| 10 LIBRARY | Full reading catalog, status, ratings, ranking, filters; reconcile totals | Planned |
| 11 BLACK CULTURE | Music, art, Black culture and Afrofuturism | Planned |
| 12 ORIGINS / EARTH | Brazil, Amazon, geography and nature | Planned |
| 13 MACHINES / FREEDOM | Computing, imaginary machines, free software and open source | Planned |
| 14 PERSONAL ARCHIVE | Aesthetics, Games, Memory, Experiments and Connection | Planned |
| 15 ENGINEERING | Accessibility, performance, security, translations, rights and links | Planned |
| 16 RELEASE | Final review, Pages release, preservation and maintenance | Planned |

## Non-negotiable requirements

- Existing profile repository and README remain independent of the website. Direct main commits are authorized; request permission before deleting existing files or performing high-impact changes.
- Keep every confirmed section, including all projects. No hidden features, secret pages, forced audio, tracking, advertising, accounts or personal portraits.
- Visible, accessible navigation; Portuguese and English; performant on modest hardware; no invented personal facts.
- Use original or properly licensed assets. The supplied photos, cover art and four quotations are not included in this public foundation until their rights/source are reviewed. No private financial details or precise residential location.
- Preserve the owner's selected names rather than silently replacing them with official nicknames. Removed fighters must remain excluded. No fabricated opinions.
- Catalog is a content seed, not an assertion that every detail is verified. Reading totals are inconsistent and must be reconciled with the owner; A Arte da Guerra is present in the purchase list only, so status is unspecified. Project seeds are not a complete inventory.

## Architecture decision 001

Initial foundation uses a Python 3 standard-library static generator, HTML and CSS, with JSON content. It has no network dependency, client-side framework or runtime server. This is a deliberate alternative to installing an untested npm dependency set. Astro/Svelte, Rust/WASM or GLSL may be adopted later if an actual visual or engineering need justifies them. Relative internal links make the project-site base path portable. Generated output is disposable and must not be committed.

Deployment is manual until the site is ready; ordinary pushes build and validate. The repository Pages source must be set to GitHub Actions before manual deployment. Do not publish the unfinished design as the final site.
