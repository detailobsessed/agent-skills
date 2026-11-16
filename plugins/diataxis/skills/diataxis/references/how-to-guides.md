# Writing and reviewing how-to guides

Source: <https://diataxis.fr/how-to-guides/>, with the distinction from tutorials at <https://diataxis.fr/tutorials-how-to/>.

## Contents

- [What a how-to guide is](#what-a-how-to-guide-is)
- [Principles](#principles)
- [Titles](#titles)
- [Language](#language)
- [Reviewing a how-to guide](#reviewing-a-how-to-guide)

## What a how-to guide is

Directions that take a competent user through a real-world problem or towards a result. It serves *work*. diataxis.fr's model is a recipe: it says what you will make and how, and it is not a cooking lesson. Even a chef who invented the dish may follow it.

It is written from the user's side, not the machinery's. A guide answers a human project ("how to calibrate the radar array", "how to configure reconnection back-off"), and tools appear only as the means. A guide that walks through what a screen or command can do ("to deploy, select the options and press Deploy") looks like guidance but tells a competent user nothing they need. "How to build a web application" is not a how-to guide either: it is an open-ended field of skill, not a specific goal.

It is not just a procedure. Real problems fork, overlap, and have several ways in and out, and the guide often has to rely on the user's judgment.

A rich list of how-to guides also shows what the product can do, and diataxis.fr expects well-chosen ones to be the most-read part of the documentation.

## Principles

- **Keep to the goal.** Explanation and reference are the usual temptations. Neither helps the user act; link to them instead.
- **Assume competence.** The reader knows what they want and can follow instructions.
- **Address real-world complexity.** A guide useful for exactly one narrow case is rarely valuable; leave room for the user to adapt it.
- **Omit the unnecessary.** Practical usability beats completeness. Start and end somewhere meaningful, and let the reader join it to their own work.
- **Give actions**, including thinking and judgment where the task needs them.
- **Order steps by meaning.** Sometimes the order is forced. Otherwise, put first what sets up the user's environment or thinking for the next step.
- **Seek flow.** Avoid making the user switch between tools and contexts, hold thoughts open for long, or jump back to earlier concerns. At best, a guide seems to anticipate the user.

## Titles

Say exactly what the guide shows. diataxis.fr's example: "How to integrate application performance monitoring" is good; "Integrating application performance monitoring" is worse, since it might be about whether to; "Application performance monitoring" is worse still, since it might be about what it is.

## Language

- "This guide shows you how to…" to name the problem or task
- conditional imperatives: "If you want x, do y. To achieve w, do z."
- "Refer to the x reference for a full list of options" instead of listing every option in the guide

## Reviewing a how-to guide

These checks are this skill's, applying the principles above.

- Does the title name a goal a user has, in "How to…" form or an equivalent?
- Is any step there only to describe the machinery rather than move the user towards the goal?
- Does it stop to teach or explain? Cut to a link.
- Does it carry a full table of options, flags or settings? Keep the values this task needs; move the full table to reference (keeping every row) and link it.
- Does it prepare the user for the likely ways the task can go wrong?
- Check each command, flag and default it states against the code or CLI.
