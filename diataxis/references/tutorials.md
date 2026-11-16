# Writing and reviewing tutorials

Source: <https://diataxis.fr/tutorials/>, with the distinction from how-to guides at <https://diataxis.fr/tutorials-how-to/>.

## Contents

- [What a tutorial is](#what-a-tutorial-is)
- [Principles](#principles)
- [Language](#language)
- [Reviewing a tutorial](#reviewing-a-tutorial)

## What a tutorial is

A tutorial is a lesson: a practical activity in which the learner learns by doing something meaningful towards an achievable goal. It serves *acquisition*. Its purpose is not to get something done but to let the reader learn, and what the learner does is not necessarily what they learn: through doing, they pick up names, tools, concepts and how things respond.

Nearly all the responsibility sits with the author. The learner's only job is to follow the directions attentively. The exercise must be:

- **meaningful**: the learner gets a sense of achievement
- **successful**: the learner can complete it
- **logical**: the path makes sense
- **usefully complete**: the learner meets every action, concept and tool they need to become familiar with

Tutorials are costly. A product change can cascade through the whole story, since the end-to-end journey has to keep making sense. Weigh that before proposing a new one, and say so when you do.

## Principles

diataxis.fr's first rule of teaching is **don't try to teach**: give the learner things to do, through which they learn. In practice:

- **Show where they are going.** Open by saying what the learner will build and what they will meet along the way. diataxis.fr calls "In this tutorial you will learn…" presumptuous and a poor pattern.
- **Deliver visible results early and often.** Every step should produce a result the learner can see and understand, however small.
- **Keep up a narrative of the expected.** Say what will happen ("after a few moments the server responds with…"), show the actual expected output, flag the likely signs of going wrong, and warn about surprising output.
- **Point out what to notice**, in passing: a changed prompt, a new file.
- **Allow repetition.** Make steps repeatable where possible; learners repeat things just to see them work again.
- **Ruthlessly minimise explanation.** One line is enough ("we use HTTPS because it is more secure"), with a link to the explanation for when the reader wants it.
- **Stay concrete.** This problem, this action, this result. General patterns emerge from the concrete on their own.
- **Ignore options and alternatives.** Keep to what reaches the goal.
- **Aspire to perfect reliability.** It must work for every learner, every time. Flaws only show up when real people follow it, so it needs testing.

## Language

diataxis.fr's patterns, paraphrased:

- the first-person plural ("we"), which says the author and learner are in this together
- "In this tutorial, we will…" to describe what the learner will accomplish
- unambiguous direction: "First, do x. Now do y."
- minimal explanation in plain words, with a link onwards
- "The output should look something like…" to set expectations
- "Notice that… Remember that… Let's check…" to help the learner orient
- a closing that describes, and mildly admires, what the learner has built

## Reviewing a tutorial

These checks are this skill's, applying the principles above. Check each against the page and cite the line:

- Does it open by saying what will be built, not what will be "learned"?
- Can a newcomer complete every step on a clean setup? Run the steps if you can; a step that fails breaks the learner's confidence in the whole thing.
- Does every step show its expected result?
- Where does it stop to explain? Each such passage is a candidate to cut to one line plus a link.
- Does it offer choices ("you can use either X or Y")? A tutorial picks one.
- Does it assume competence the learner lacks? Then it is a how-to guide in a tutorial's place, or it needs the missing steps.
