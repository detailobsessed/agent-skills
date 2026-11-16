---
name: diataxis
description: Writes, reviews and restructures project documentation the way Diátaxis (Diataxis) is described by its author at diataxis.fr. Improves docs one small, publishable change at a time, uses the compass to tell tutorials, how-to guides, reference and explanation apart down to a single sentence, and lets structure grow from the content instead of imposing four folders. Proposes every change before making it, keeps each true fact when moving material, and brings removals of wrong, outdated or duplicated content to the user as decisions. Use when asked to write, review, tidy, split, reorganise or restructure docs, a README or a docs site (MkDocs, Zensical, Sphinx, Docusaurus or any other), when deciding whether a page is a tutorial or a how-to guide, when a page mixes steps with reference tables or background, or when someone asks whether their project's docs need restructuring.
license: MIT
---

# Diátaxis

Diátaxis is Daniele Procida's approach to technical documentation, published at <https://diataxis.fr>. It names four kinds of documentation, each serving a different need, and a way of working that improves documentation one small step at a time. This skill paraphrases diataxis.fr as published from its source at commit `957c09c`, read on 2026-11-16. Each claim about Diátaxis in `references/` links the page it comes from; [references/sources.md](references/sources.md) lists them, says which rules are this skill's own rather than Diátaxis's, and covers the license.

## Two misreadings to avoid

**Diátaxis is not a structure to impose.** Its author calls it "a guide, not a plan", says not to spend energy getting the structure right, and calls creating empty tutorials/how-to/reference/explanation sections "horrible" ([how to use Diátaxis](https://diataxis.fr/how-to-use-diataxis/)). The four-part shape appears *because* the docs were improved, from the inside. So never open with a target directory tree, never create empty sections or placeholder pages, and never propose pages just to fill a category.

**Diátaxis does not make docs correct.** Accuracy and completeness are what diataxis.fr calls functional quality, and it says plainly that Diátaxis cannot address it; it can only expose lapses ([quality](https://diataxis.fr/quality/)). Checking each claim against the code is separate work, and you still have to do it: [references/quality.md](references/quality.md) says how.

## The workflow

This is the cycle diataxis.fr prescribes ([how to use Diátaxis](https://diataxis.fr/how-to-use-diataxis/), [start here](https://diataxis.fr/start-here/)). Follow it whatever the size of the request.

1. **Choose one thing.** If the user named a page, a section or a paragraph, that is it. If they asked about the docs in general, take what is in front of you: the page they mentioned, the README, the page most readers land on. Do not survey everything hunting for problems. Smaller is better: a page at most, a section or a paragraph if you can.
2. **Assess it against the need it serves.** Which user need does it serve (run the compass below)? How well does it serve it? What could be added, moved, removed or changed to serve it better? Do its language and logic fit its mode? Check the facts it states against the code, config or CLI while you are there.
3. **Decide the single next action** that would improve it right away. If what you chose states something wrong, correcting it comes first: deep quality is conditional on functional quality ([quality](https://diataxis.fr/quality/)), and a wrong flag or version misleads every reader, while a misplaced paragraph only slows them down. Propose the correction as the first change and the restructuring after it.
4. **Propose that action and wait for approval.** See "Proposing a change" below.
5. **Make the change once approved**, as one change the user can commit or publish on its own. Then go back to step 1. Each change usually shows you the next one.

A request to "restructure the docs" or "apply Diátaxis to the docs" still runs this cycle. Read enough to orient yourself (the page list, the nav, the opening of each page). Then report three things: one line per page saying which need it serves now and its main problem; the first improvement, proposed in full; and a short ordered list of the next few candidates, each publishable on its own. Do not include a target tree. Propose a structural move, such as grouping pages under a heading, only when the content you already have demands it: several how-to guides scattered through a "Usage" page, say.

## The compass

When it is unclear what kind of documentation something is, or should be, ask two questions ([compass](https://diataxis.fr/compass/)):

| The content… | …and serves the user's… | …so it belongs in |
| --- | --- | --- |
| informs action (doing) | acquisition of skill (study) | a tutorial |
| informs action (doing) | application of skill (work) | a how-to guide |
| informs cognition (knowing) | application of skill (work) | reference |
| informs cognition (knowing) | acquisition of skill (study) | explanation |

Apply it at any scale: a whole page, a section, a paragraph, a single sentence. When the parts of a page give different answers, the page mixes modes, and that is the usual source of trouble. Trust the compass over first impressions, which diataxis.fr warns are often wrong. [references/compass.md](references/compass.md) covers the two confusions it settles most often (tutorial against how-to guide, reference against explanation) and how neighbouring modes blur.

## Writing in each mode

| Mode | Answers | The reader is | Keep out |
| --- | --- | --- | --- |
| Tutorial | "Can you teach me to…?" | learning, by doing, under your care | explanation, choices, alternatives |
| How-to guide | "How do I…?" | competent, with a real goal | teaching, digressions, full option lists |
| Reference | "What is…?" | at work, looking something up | instruction, opinion, explanation |
| Explanation | "Why…?" | stepping back to understand | step-by-step instruction, exhaustive facts |

Before writing or reviewing a page in a mode, read its guide: [tutorials](references/tutorials.md), [how-to guides](references/how-to-guides.md), [reference](references/reference.md), [explanation](references/explanation.md). For troubleshooting pages, FAQs, migration guides, release notes, READMEs and pages that mix modes, read [references/boundary-cases.md](references/boundary-cases.md).

## Rules for changing docs

These are this skill's rules for working in someone else's docs, on top of what Diátaxis says.

**Propose first; change nothing until the user approves.** That covers edits, moves, renames, deletions, new pages and navigation changes. A request to write a specific page approves writing that page and nothing else, so propose anything around it (where it goes, what links to it, what it replaces). Unasked restructuring is the main harm an agent does to someone's docs, and the user can only weigh a change they have seen.

**Content.** Preserve information that is still true: move and reorganise it, never lose it in the move. Content that is wrong, outdated, or duplicated elsewhere gets corrected or removed, and each removal is brought to the user as a decision.

- Call something wrong only with evidence: the file and line, the config value, or the command output that contradicts it. If you cannot check a claim, say it is unverified rather than removing it.
- When splitting a page, account for every fact: each table row, caveat, warning and example. Say where each moved block goes.
- Duplicates: keep the copy in the mode that owns the fact (an option's default belongs in reference) and link to it from the others.

**Gaps are observations.** Say what is missing and who it affects ("there is no tutorial, so a newcomer starts at the install guide"). Never create a stub, a "coming soon" page, or a heading with nothing under it. If the user wants the missing page, write the real page.

**Navigation follows the content.** Change the nav in the same proposal as the move that needs it, never ahead of the content. Moving a published page breaks inbound links: update internal links, and propose a redirect where the docs tool supports one. [references/structure.md](references/structure.md) covers where MkDocs, Zensical, Sphinx and Docusaurus keep their navigation, landing pages, and docs with several audiences or platforms.

**Keep the project's conventions**: file names, front matter, link style, admonition syntax, and the tool's Markdown flavour.

**Fit the size of the project.** A README is documentation too. A small project does not need separate pages per mode: sections of one file can each serve one need, and the compass works on them just as well. Recommend splitting a README only when its content demands it. Otherwise say no restructure is needed and offer the one improvement worth making.

## Proposing a change

Lay out each proposal like this, so the user can approve or reject it at a glance:

1. **What**: the page, section or paragraph, by path and heading.
2. **Compass reading**: the need it serves now, and the need it should serve if that differs.
3. **Problem**: what gets in the reader's way, with evidence for any factual error.
4. **Change**: the new text, or a before and after, exact enough to apply as written.
5. **Moved**: each block of information that moves, and where it goes.
6. **Removals, for decision**: each thing you would delete or correct, and why. Ask about each one.
7. **Links and navigation**: what else changes so nothing breaks.

Then list observations (gaps, other problems you noticed) separately, as observations, not tasks. Stop and wait for the user.
