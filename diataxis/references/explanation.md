# Writing and reviewing explanation

Source: <https://diataxis.fr/explanation/>, with the distinction from reference at <https://diataxis.fr/reference-explanation/>.

## Contents

- [What explanation is](#what-explanation-is)
- [Principles](#principles)
- [Language](#language)
- [Reviewing explanation](#reviewing-explanation)

## What explanation is

A discursive treatment of a subject that permits reflection. It deepens and broadens understanding, and its scope is a topic: an area of knowledge bounded in some reasonable way. It answers "can you tell me about…?", and it is the kind of documentation that makes sense to read away from the product.

It is less *urgent* than the other three but no less *important*. Without it, a practitioner's knowledge stays loose and fragile. Often a project has no explanation as such; instead it is scattered in small parcels across other pages. When those parcels interrupt the page they sit in, moving one into an explanation page that answers its why question is a small step of the kind the workflow asks for (this skill's suggestion).

It need not be called "Explanation". diataxis.fr offers *Discussion*, *Background*, *Conceptual guides* and *Topics*.

## Principles

- **Start from a why question**, real or imagined. Explanation has no natural boundary the way a task or a machine does; a question gives it one. Otherwise, draw a reasonable boundary and keep to it.
- **Make connections**, even to things outside the topic.
- **Provide context**: design decisions, history, technical constraints, implications, specific examples.
- **Talk about the subject.** An implicit "About" should fit in front of each title: "About user authentication".
- **Admit opinion and perspective.** Explanation can and must consider alternatives, counter-examples and other approaches.
- **Keep it bounded.** Explanation tends to absorb instructions and technical description. Those belong elsewhere, and pulling them in hides them from where readers look for them.

## Language

- "The reason for x is that, historically, y…"
- "W is better than z, because…": judgments and opinions where appropriate
- "An x in system y is like a w in system z. However…"
- "Some users prefer w, because z. That can work, but…"
- "An x interacts with a y as follows…": how the machinery works inside, to show why it does what it does

## Reviewing explanation

These checks are this skill's, applying the principles above.

- Can you name the why question the page answers? If not, it may be a mixture of several pages.
- Does it slide into numbered steps or option tables? Those belong in a how-to guide or reference.
- Are design decisions stated with their reasons and alternatives, or only asserted?
- Where else in the docs are there parcels of explanation (a "why" paragraph in a tutorial, a design note in reference) that would read better here?
