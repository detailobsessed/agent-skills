# Writing and reviewing reference

Source: <https://diataxis.fr/reference/>; the structure rule also appears at <https://diataxis.fr/start-here/>.

## Contents

- [What reference is](#what-reference-is)
- [Principles](#principles)
- [Language](#language)
- [Reviewing reference](#reviewing-reference)

## What reference is

Technical description of the machinery and how to operate it. It holds propositional knowledge the user consults while working. Unlike tutorials and how-to guides, which are led by the user's needs, reference is led by the product it describes: APIs, classes, functions, commands, options, configuration keys, error messages.

Users need it for truth and certainty, firm ground to stand on while they work. One does not read it, one consults it. It should be austere and wholly authoritative, with no doubt or ambiguity. diataxis.fr's analogy is the information on a food packet, presented in a standard way, without recipes or marketing mixed in.

Reference may describe how something works or the correct way to use it, but it does not show how to perform tasks. Generated reference (API docs from the code) helps it stay accurate, but diataxis.fr warns against treating generated reference as all the documentation a project needs.

## Principles

- **Describe, and only describe.** Neutral description is hard because explaining, instructing and opining come more naturally. When description seems too thin, link to the how-to guide, explanation or tutorial rather than adding them here.
- **Adopt standard patterns.** Reference is useful when it is consistent: the same shape for every entry, where the user expects it, in a familiar format. This is no place for stylistic variety.
- **Respect the structure of the machinery.** The documentation's structure should mirror the product's, as a map mirrors territory: a method under its class, under its module. Not forced, but the code's logical arrangement should help make sense of the docs. A side effect diataxis.fr notes: mirroring the code makes gaps in the reference easy to see.
- **Provide examples.** A short usage example illustrates without sliding into instruction or explanation.

## Language

- state facts about the machinery and its behaviour
- list commands, options, operations, features, flags, limitations, error messages
- give warnings where needed: "You must use a. You must not apply b unless c."

## Reviewing reference

These checks are this skill's, applying the principles above.

- Is every entry in the same shape?
- Does the arrangement follow the code, CLI or config structure?
- Where does an entry start explaining why, or walking through a task? Move that to explanation or a how-to guide and link it.
- Check each default, type, limit and flag against the source. Reference is where a wrong fact does the most damage, because readers trust it.
- Compare the listed items against the code (every option, every subcommand) and report what is missing as an observation.
