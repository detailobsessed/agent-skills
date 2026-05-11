# macos-expert

An [Agent Skill](https://agentskills.io) for modern macOS development, explicitly grounded in Apple's Human Interface Guidelines and official Apple developer documentation.

The goal is not "Swift on desktop." The goal is Mac-native product and engineering guidance: windows, menus, toolbars, sidebars, file workflows, accessibility, SwiftUI, AppKit, bridging, persistence, sandboxing, menu bar apps, and shipping. The skill is opinionated about when SwiftUI is enough, when AppKit is required, and when bridging is the right answer — because the wrong call here produces apps that look like Mac apps but feel like iPad apps in a window.

## Design goals

- Cover the major areas Apple emphasizes for macOS without the obvious gaps
- Reflect reality, not framework marketing — name the documented SwiftUI gaps and tell the agent when to bridge to AppKit
- Prefer stable, official Apple guidance over trend-driven or speculative platform claims
- Keep the skill cohesive and self-contained
- Keep `SKILL.md` concise (with the Shape A vs Shape B triage rubric near the top) and push depth into focused reference files

## What this skill is honest about

The reference files explicitly call out concrete SwiftUI macOS gaps that Apple's own documentation acknowledges or implies:

- `.contextMenu` has no "menu is open" signal and no focus-ring styling on the right-clicked row
- `.draggable` has no session-end / cancel callback (no SwiftUI equivalent to `NSDraggingSource.draggingSession(_:endedAt:operation:)`)
- `onMoveCommand` is macOS / tvOS only — not iOS or iPadOS
- `TextField` consumes arrow keys for cursor movement, breaking Spotlight-style search-with-arrow-nav patterns
- `ToolbarItemPlacement` semantic placements are platform-variable by design (Apple's own wording)
- `backgroundProminence` works only inside `List` and `Table`, not in custom rows

The skill names the AppKit alternative for each gap rather than inventing SwiftUI workarounds.

## Source policy

This skill was built from Apple's own macOS design and developer documentation, plus practical experience with real Mac apps that exercise the boundaries between SwiftUI and AppKit (NetNewsWire's AppKit-shell pattern, Ruddarr's SwiftUI-only pattern).

## Primary Apple HIG pages used

- `https://developer.apple.com/design/human-interface-guidelines/designing-for-macos`
- `https://developer.apple.com/design/human-interface-guidelines/windows`
- `https://developer.apple.com/design/human-interface-guidelines/toolbars`
- `https://developer.apple.com/design/human-interface-guidelines/sidebars`
- `https://developer.apple.com/design/human-interface-guidelines/the-menu-bar`
- `https://developer.apple.com/design/human-interface-guidelines/dock-menus`
- `https://developer.apple.com/design/human-interface-guidelines/menus`
- `https://developer.apple.com/design/human-interface-guidelines/file-management`
- `https://developer.apple.com/design/human-interface-guidelines/drag-and-drop`
- `https://developer.apple.com/design/human-interface-guidelines/going-full-screen`

## Primary Apple API documentation families used

- AppKit
- SwiftUI
- SwiftData
- Accessibility on macOS
- ServiceManagement
- Quick Look
- Uniform Type Identifiers
- Core Transferable

## Sosumi verification notes

During authoring and review, the Sosumi MCP server was used to cross-check concrete Apple symbols and documentation pages. The skill files refer only to official Apple documentation.

The following symbols, modifiers, and concepts were explicitly verified against Apple's docs while building the skill, with particular attention to availability lines and discussion sections:

- `Window`, `WindowGroup`, `Settings`, `DocumentGroup`, `MenuBarExtra`
- `NavigationSplitView` (and its auto-added sidebar toggle)
- `Table` (selection, sort, hierarchy, customization)
- `ToolbarItemPlacement` (semantic vs positional placements; overflow language)
- `.contextMenu(menuItems:)`, `.contextMenu(forSelectionType:menu:primaryAction:)`
- `.draggable(_:)`, `.draggable(_:preview:)`
- `onMoveCommand(perform:)` (macOS / tvOS only — confirmed)
- `onKeyPress(_:action:)` and variants
- `@Environment(\.appearsActive)` (replacement for `controlActiveState`)
- `@Environment(\.backgroundProminence)` (with `List`/`Table` constraint confirmed)
- `.focusable(_:)`, `@FocusState`
- `.listRowBackground`, `.tableStyle`
- `NSHostingView`, `NSHostingController`
- `NSDraggingSource` (full lifecycle: `willBeginAt`, `movedTo`, `endedAt:operation:`)
- `NSFilePromiseProvider`
- `SMAppService`
- `notarytool`

## Module-by-module source map

### `SKILL.md`

Synthesized from Apple sources plus the Shape A / Shape B triage rubric derived from observing how real Mac apps split responsibilities between SwiftUI and AppKit.

### `references/official-sources.md`

Primary basis: Apple HIG as design source of truth, Apple Developer docs as API source of truth.

Emphasis: making future updates verifiable, with explicit guidance on reading "Available on" lines and Discussion sections that document API constraints.

### `references/designing-for-macos.md`

Primary basis: `Designing for macOS` HIG plus related guidance on windows, menus, toolbars, sidebars, drag and drop, and full-screen.

Emphasis: practical macOS product heuristics, with concrete "iPad-in-a-window" anti-pattern signals.

### `references/windows-navigation.md`

Primary basis: HIG pages for windows, toolbars, sidebars; SwiftUI scene and navigation APIs; AppKit window and split-view APIs.

Emphasis: matching scene types to workflows; the `ToolbarItemPlacement` non-determinism caveat; when `NSToolbar` beats `.toolbar`.

### `references/menus-commands-input.md`

Primary basis: HIG menu and Dock-menu guidance; SwiftUI command APIs; AppKit menu and responder-chain patterns.

Emphasis: standard commands as first-class Mac UI, plus the SwiftUI keyboard and drag-lifecycle gaps with concrete bridging signals.

### `references/file-management-documents.md`

Primary basis: HIG file-management guidance; document-based app patterns; SwiftUI file workflow APIs; AppKit file panels and `NSDocument`.

Emphasis: standard file workflows, security-scoped bookmark balancing, and `NSFilePromiseProvider` for drag-out scenarios SwiftUI doesn't cover.

### `references/accessibility.md`

Primary basis: Apple accessibility guidance for macOS; VoiceOver and accessibility API documentation.

Emphasis: keyboard navigation completeness, the `TextField` focus-trap pattern, and explicit semantics for custom rows that aren't in `List`/`Table`.

### `references/swiftui-macos.md`

Primary basis: SwiftUI scene, navigation, table, command, menu bar, file workflow, focus, drag, and toolbar APIs for macOS; Apple's own discussion of platform-variable placement and the documented constraints on `backgroundProminence`, `appearsActive`, `onMoveCommand`, and `onKeyPress`.

Emphasis: native SwiftUI patterns plus an honest catalogue of the gaps Apple's documentation acknowledges, with concrete trigger signals for when to bridge.

### `references/appkit-and-bridging.md`

Primary basis: AppKit documentation; `NSHostingView` / `NSHostingController` and representable bridging patterns; `NSDraggingSource`, `NSToolbarDelegate`, `NSMenuItemValidation`, and responder-chain documentation.

Emphasis: concrete trigger signals for when AppKit beats SwiftUI on Mac, with bridging rules and common pitfalls.

### `references/persistence-and-data.md`

Primary basis: SwiftData documentation; document-based app guidance; Apple platform conventions for preferences vs documents vs relational app data; `@SceneStorage` and AppKit window restoration.

Emphasis: matching storage technology to the user's mental model, with Core Data still acknowledged as a valid choice.

### `references/platform-capabilities-distribution.md`

Primary basis: sandboxing and entitlement guidance; ServiceManagement docs for login items; extension and Quick Look documentation; Apple distribution expectations for signed and notarized Mac apps.

Emphasis: capabilities, entitlements, signing, and distribution as one combined product-and-engineering decision; modern tooling (`notarytool`, `SMAppService`).

## What this skill intentionally does not do

- Recommend SwiftUI workarounds for documented API gaps without naming the gap and the AppKit bridge
- Make version-specific or newly announced platform claims without verification
- Treat AppKit as legacy — it isn't; on Mac, it's still the right answer for some app shapes
- Provide deeper coverage than the most recent macOS release that's been verified against Apple's published docs

## Install

```bash
npx skills add https://github.com/detailobsessed/agent-skills --skill macos-expert
```

## License

MIT
