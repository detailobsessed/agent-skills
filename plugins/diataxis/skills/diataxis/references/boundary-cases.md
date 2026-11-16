# Boundary cases: formats that hold more than one mode

## Contents

- [Why these are formats, not modes](#why-these-are-formats-not-modes)
- [Pages that mix modes](#pages-that-mix-modes)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Migration and upgrade guides](#migration-and-upgrade-guides)
- [Release notes and changelogs](#release-notes-and-changelogs)
- [README files and small projects](#readme-files-and-small-projects)

## Why these are formats, not modes

diataxis.fr argues there are four and only four kinds of documentation, because its two axes cover the whole territory ([foundations](https://diataxis.fr/foundations/)). A FAQ, a troubleshooting page or a migration guide is therefore not a fifth kind. It is a container, and each piece inside it answers one of the four needs.

diataxis.fr discusses only one of the formats below directly: troubleshooting, which it names once, as an example how-to title. The rest of this file is the compass applied to each format. It is this skill's reading, not a ruling from diataxis.fr, so present it to the user that way.

## Pages that mix modes

diataxis.fr treats blurring as natural and constant: neighbouring modes share an axis and bleed into each other ([map](https://diataxis.fr/map/)). A mixed page is the normal starting point, not a failure. To work on one:

1. Run the compass on each section, and on the sentences of any section that feels uneven ([compass](https://diataxis.fr/compass/)).
2. Decide the page's main need, usually the one its title and most readers serve.
3. Pick one block of the other mode to move, as one change. If a page in that mode already exists, move the block there. If none exists and the block is enough to stand as a real page, propose that page with the block as its content. If it is a line or two, it may only need cutting to one line plus a link.
4. Leave a link where the block was, so a reader who needed it still finds it.
5. List every fact that moves. Nothing true is lost in the move.

The usual first move for a how-to guide carrying a full options table: keep in the guide the values this task needs, move the full table to reference with every row intact, and link it ([how-to guides](https://diataxis.fr/how-to-guides/): link to reference rather than listing everything).

## Troubleshooting

diataxis.fr gives *Troubleshooting deployment problems* as an example of a how-to guide ([start here](https://diataxis.fr/start-here/)): a competent user, at work, with a problem to get out of. Applying the compass to the rest of a typical troubleshooting page:

- symptom, then the steps to fix it: **how-to guide**
- a catalogue of error messages or codes and what each means: **reference** (error messages are among the things diataxis.fr lists as reference content, [reference](https://diataxis.fr/reference/))
- why a class of failure happens, how the internals produce it: **explanation**

So a troubleshooting page is often a how-to guide that should link to an error reference, with any long "why" passage moved to explanation.

## FAQ

diataxis.fr does not discuss FAQs. Applying the compass per entry: "How do I…?" is a how-to guide; "What is the default or limit for…?" is reference; "Why does it…?" is explanation; "Where do I start?" is often a sign that a tutorial is missing.

An FAQ grows into a page where every answer sits outside the context its reader looks in. One step at a time, move one answer to the page that owns its need and link the FAQ entry to it. Whether to keep the FAQ as a list of pointers, or retire it once it is empty, is the user's decision. Do not dismantle it in one go.

## Migration and upgrade guides

diataxis.fr does not discuss migration guides. Applying the compass: moving from one version to another is a goal a competent user has at work, so the steps are a **how-to guide**. Its usual companions belong elsewhere:

- the list of removed, renamed or changed options, APIs and defaults: **reference** (often the changelog or release notes)
- why the change was made, and the trade-offs: **explanation**

Keep the steps in the guide, link to the list and to the reasoning, and make sure every breaking change on the list has a step, or a stated reason why none is needed.

## Release notes and changelogs

Not discussed on diataxis.fr. Applying the compass: a record of what changed in each release is facts consulted while working, so it is **reference**, and should be kept austere and consistent. Upgrade steps inside a changelog are a how-to guide, and design discussion is explanation.

## README files and small projects

Nothing in Diátaxis requires one page per mode. The compass works on sections and sentences ([compass](https://diataxis.fr/compass/)), and diataxis.fr's workflow says that getting started does not mean dividing the documentation into four sections, nor creating empty ones ([how to use Diátaxis](https://diataxis.fr/how-to-use-diataxis/)). It also describes documentation as always able to be *complete* at its stage of growth, even though it is never finished.

So a README can be good Diátaxis documentation as it stands: an opening paragraph on what the project is and why (explanation), an install or usage section (how-to), a table of options (reference), perhaps a short worked first run (tutorial). Review each section in its own mode. Recommend a split into pages only when a section has outgrown the file. Otherwise tell the user no restructure is needed, and offer the one improvement that would help most.
