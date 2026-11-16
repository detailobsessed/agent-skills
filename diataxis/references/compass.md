# The compass, and telling the modes apart

## Contents

- [Using the compass](#using-the-compass)
- [Tutorial or how-to guide](#tutorial-or-how-to-guide)
- [Reference or explanation](#reference-or-explanation)
- [How neighbouring modes blur](#how-neighbouring-modes-blur)
- [The order readers move in](#the-order-readers-move-in)

## Using the compass

Source: <https://diataxis.fr/compass/>, <https://diataxis.fr/start-here/>, <https://diataxis.fr/foundations/>.

The compass reduces "what kind of documentation is this?" to two questions: **action or cognition?** and **acquisition or application?** The answers pick one of the four modes (the table in `SKILL.md`). diataxis.fr presents it as a course-correction tool, for the moments when you think you are doing one thing but something feels off, or when intuition gives a quick answer that turns out wrong.

Read the terms loosely, especially at first:

- **action**: practical steps, doing
- **cognition**: theoretical or propositional knowledge, thinking
- **acquisition**: study
- **application**: work

Ask the questions from whichever side helps: what am I writing for? what is this text in front of me doing? what does the reader need? what do I want to do here? And ask them close up, of a sentence or a word, as well as of a whole document. A tutorial step that stops to explain why the protocol works the way it does has switched from action to cognition for that sentence; the compass catches it there.

The two axes cover the whole territory, which is why diataxis.fr argues there are exactly four kinds of documentation and no fifth ([foundations](https://diataxis.fr/foundations/)). When a page seems to be "none of the four", it is usually a format (FAQ, troubleshooting, changelog) holding pieces of several; see `boundary-cases.md`.

## Tutorial or how-to guide

Source: <https://diataxis.fr/tutorials-how-to/>.

diataxis.fr calls this the most common conflation in software documentation. Both contain steps, both promise success if you follow them, and both need the reader's hands on the product. The difference is the need: a tutorial serves the reader **at study**, a how-to guide serves the reader **at work**.

| Tutorial | How-to guide |
| --- | --- |
| helps a learner acquire basic competence | helps a competent user do a particular task correctly |
| a carefully managed path, in a contrived setting | the real world, where the path cannot be managed |
| eliminates the unexpected | prepares for the unexpected and says how to handle it |
| one line, no choices or alternatives | forks: "if this, then that" |
| must be safe; you can always start again | cannot promise safety; sometimes there is one chance |
| responsibility lies with the author | the user is responsible for getting in and out of trouble |
| explicit about basic things: where to type, how long to wait | relies on that as implicit knowledge |
| concrete and particular | general, since each real case differs |

The difference is **not** basic against advanced. A how-to guide can cover a routine, simple procedure, and a tutorial can teach something advanced to experienced people. When reviewing a page called "Getting started" that assumes the reader knows what they want and offers options at each step, it is a how-to guide whatever its title says.

## Reference or explanation

Source: <https://diataxis.fr/reference-explanation/>.

Both hold knowledge rather than steps; again the difference is work against study. Rules of thumb from diataxis.fr:

- boring and unmemorable, lists of things (classes, methods, options), tables of information: probably reference
- something you could imagine reading in the bath, or the answer to "can you tell me more about…?" over a drink: probably explanation

The real test when in doubt: would someone turn to this *while doing the work*, or once they have stepped away from it to think? The usual slip is reference that grows expansive: an illustrative example turns into a discussion of why, or what if. That harms both, since the reference gets interrupted and the explanation never gets room to do its own job.

## How neighbouring modes blur

Source: <https://diataxis.fr/map/>.

Each mode shares one axis with each of its two neighbours on the map, and that shared ground is where they bleed into each other:

| Shared ground | Modes that blur |
| --- | --- |
| guide action | tutorials and how-to guides |
| serve the application of skill | how-to guides and reference |
| contain propositional knowledge | reference and explanation |
| serve the acquisition of skill | explanation and tutorials |

So expect these specific mixes when reviewing: tutorials that turn into how-to guides (or the reverse), how-to guides that carry full option tables, reference that drifts into explanation, and tutorials loaded with explanation. When distinctions blur, the style and content of one mode creep into another, and the structure suffers too, which makes the discipline harder still. The worst case diataxis.fr describes is tutorials and how-to guides collapsing into each other so neither need is met.

## The order readers move in

Source: <https://diataxis.fr/map/>.

diataxis.fr describes a cycle a practitioner moves through: learning (tutorial), then putting the skill to work (how-to), consulting facts when the work calls for them (reference), and reflecting away from the work (explanation). It also says not to read this literally: a reader can enter the documentation anywhere, and what they want changes from moment to moment. So do not argue that the docs must be read in that order, or that a site must lead with a tutorial.
