# Quality, and what Diátaxis cannot do

Source: <https://diataxis.fr/quality/>.

## Contents

- [Functional and deep quality](#functional-and-deep-quality)
- [What Diátaxis can and cannot do](#what-diátaxis-can-and-cannot-do)
- [Checking accuracy](#checking-accuracy)

## Functional and deep quality

diataxis.fr distinguishes two kinds of quality.

**Functional quality** is accuracy, completeness, consistency, usefulness, precision "and so on": an open list, not a fixed set of dimensions. Its characteristics are independent of each other (documentation can be accurate yet incomplete, or complete, accurate and consistent yet useless), objective, measured against the world the documentation describes, and they feel to the author like constraints that every release puts to the test again.

**Deep quality** is feeling good to use, having flow, fitting human needs, being beautiful, anticipating the user. These cannot be measured, only judged. They are interdependent, subjective (assessed against the human, not the world), and conditional on functional quality: nobody experiences inaccurate documentation as beautiful.

## What Diátaxis can and cannot do

diataxis.fr is direct about this: Diátaxis **cannot address functional quality**. Accuracy and completeness come from skill, knowledge of the domain and attention to detail.

What it can do for functional quality is *expose* lapses. Its example: making reference mirror the structure of the code makes the reference's gaps visible.

For deep quality it does more. Its modes are built around user needs, so placing material in the right mode helps it fit those needs. And it protects flow, by keeping, say, a digression into explanation from breaking up a how-to guide.

Even so, diataxis.fr says it offers principles, not a formula. It cannot replace user-experience, interaction or visual design skills, and it does not guarantee deep quality. At most it lays down conditions that make deep quality possible.

## Checking accuracy

This section is this skill's own. Since Diátaxis cannot check facts, check them separately whenever you assess a piece of documentation:

- Compare each command, flag, option, default, path, version and limit the text states with the code, configuration, CLI help or tests. Run a command when it is safe and cheap to run.
- Another document is not evidence. When a page disagrees with a skill, a second page or a wiki, that shows only that the two disagree: check both against the code, config or live system before calling either one wrong, outdated or incomplete.
- Every fact you add, move or reword gets the same check, even when it comes from another document in the same repo. A fact copied unchecked from a sibling doc carries that doc's errors onto the new page.
- Record the evidence for each discrepancy: file and line, config value, or command and output.
- Bring each correction or removal to the user as a decision, with that evidence, in the proposal's "Removals, for decision" list.
- If a claim cannot be checked (behaviour on a platform you cannot run, an external service), mark it unverified and leave it in place.
