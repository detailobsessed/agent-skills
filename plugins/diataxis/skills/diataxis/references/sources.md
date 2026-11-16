# Sources, attribution and license

## The source

Diátaxis is the work of Daniele Procida, published at <https://diataxis.fr> from the repository <https://github.com/evildmp/diataxis-documentation-framework>. This skill was written from the source files at commit `957c09ca40b4a1edc23874f713e01937d50d54d5`, read on 2026-11-16.

| Page | Used in |
| --- | --- |
| <https://diataxis.fr/start-here/> | `SKILL.md`, `boundary-cases.md`, `reference.md` |
| <https://diataxis.fr/how-to-use-diataxis/> | `SKILL.md`, `structure.md`, `boundary-cases.md` |
| <https://diataxis.fr/compass/> | `SKILL.md`, `compass.md`, `boundary-cases.md` |
| <https://diataxis.fr/map/> | `compass.md`, `boundary-cases.md` |
| <https://diataxis.fr/foundations/> | `compass.md`, `boundary-cases.md` |
| <https://diataxis.fr/tutorials/> | `tutorials.md` |
| <https://diataxis.fr/how-to-guides/> | `how-to-guides.md`, `boundary-cases.md` |
| <https://diataxis.fr/reference/> | `reference.md`, `boundary-cases.md` |
| <https://diataxis.fr/explanation/> | `explanation.md`, `structure.md` |
| <https://diataxis.fr/tutorials-how-to/> | `compass.md`, `tutorials.md`, `how-to-guides.md` |
| <https://diataxis.fr/reference-explanation/> | `compass.md`, `explanation.md` |
| <https://diataxis.fr/quality/> | `SKILL.md`, `quality.md` |

**Removed page.** `https://diataxis.fr/complex-hierarchies/` returns 404, so it is not linked here. Its source file was deleted in commit `c9534824c8` (2026-08-03, "Added translation machinery and content"), and no current page carries its content. `structure.md` cites its last version, at commit `0c9022e`: <https://github.com/evildmp/diataxis-documentation-framework/blob/0c9022ecbd82f8cd42069886faae40cd91eb8995/complex-hierarchies.rst>. When refreshing this skill, check whether the material has returned to the site.

To refresh: compare the current source files with commit `957c09c` (`git diff 957c09c..main -- '*.rst'` in a clone), and re-check every claim that cites a changed page.

## What is Diátaxis and what is this skill

These come from diataxis.fr: the four modes and how to write each, the compass, the map and its blurring, the iterative workflow, organic structure, the warning against empty structures, functional and deep quality, and the landing-page and complex-hierarchy guidance.

These are this skill's own, and are labelled where they appear:

- propose every change and wait for approval
- the content rule: keep what is true when moving it; bring each removal of wrong, outdated or duplicated content to the user as a decision
- gaps as observations, never stubs
- the proposal layout
- the review checklists at the end of each mode guide
- the readings of FAQ, migration guides and release notes, and most of troubleshooting, in `boundary-cases.md` (the compass applied; diataxis.fr does not discuss these formats)
- the docs-tool navigation and redirect notes, and the accuracy checks in `quality.md`

## License

diataxis.fr's text is licensed under Creative Commons Attribution-ShareAlike 4.0 International (`LICENSE.rst` in the repository; GitHub's licence detection reports it as NOASSERTION because it does not parse the `.rst` file). This skill is MIT-licensed, so it does not reproduce or adapt diataxis.fr's text. It describes the ideas in its own words, quotes only a few words at a time, credits the author, and links each page it draws on.
