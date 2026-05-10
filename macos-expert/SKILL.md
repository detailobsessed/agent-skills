---
name: macos-expert
description: Comprehensive modern macOS app development guidance grounded in Apple's Human Interface Guidelines and official Apple developer documentation. Use when building, reviewing, or refactoring macOS software with SwiftUI, AppKit, AppKit-SwiftUI bridging, SwiftData, accessibility, menus, windows, toolbars, sidebars, document and file workflows, drag and drop, sandboxing, distribution, or other Mac-specific platform behavior.
---

# macos-expert

Use this skill to keep macOS work native, modern, and source-backed. The skill is opinionated about when SwiftUI is enough, when AppKit is required, and when bridging is the right answer — because the wrong call here produces apps that look like Mac apps but feel like iPad apps in a window.

## When to use

- Building, reviewing, or refactoring a macOS app with SwiftUI, AppKit, or both
- Designing windows, toolbars, sidebars, menus, commands, or keyboard shortcuts for macOS
- Implementing document-based apps, file import/export, open/save panels, or Quick Look
- Working with drag and drop, clipboard, undo/redo, or context menus
- Adding or auditing VoiceOver, keyboard navigation, focus, contrast, or motion accessibility
- Choosing between SwiftData, Core Data, UserDefaults, or file-based persistence
- Bridging AppKit and SwiftUI with NSHostingView, NSViewRepresentable, or coordinators
- Configuring sandboxing, entitlements, security-scoped bookmarks, or App Groups
- Building menu bar apps with MenuBarExtra or NSStatusItem
- Setting up login items, extensions, signing, notarization, or distribution
- Reviewing whether a macOS app feels native or carries iOS anti-patterns

## Recommended companion tools

Using [Sosumi](https://sosumi.ai/) alongside this skill is highly recommended. Sosumi provides direct access to Apple Developer documentation and Human Interface Guidelines as Markdown, making it easy to verify APIs, symbols, and platform behavior referenced in this skill against current official sources. The verification workflow lives in `references/official-sources.md`.

## Source priority

Use sources in this order:

1. Apple Human Interface Guidelines and Apple Developer documentation
2. Reference files in this skill

If a named API, symbol, modifier, entitlement, or platform behavior is uncertain, verify it against current official Apple documentation **before** presenting it as fact. Pay particular attention to the "Available on" line on each API page — platform availability is the most common source of stale guidance. See `references/official-sources.md` for the full verification workflow.

## Two macOS app shapes — pick the right one before writing code

The single highest-leverage decision when starting or reviewing a macOS app is choosing between two architectural shapes. Get this right and the rest of the work is straightforward. Get this wrong and you'll spend the project fighting the framework.

### Shape A: SwiftUI-only Mac app

A pure-SwiftUI Mac app is the right call when the product looks like:

- A **content browser** (lists of items, detail panes, light forms — read-mostly, tap-to-drill)
- A **utility / menu bar app** without a heavy main window
- A **cross-platform port** where iOS is the primary target and macOS rides along via `#if os(macOS)`
- A **document app** where the content area is your own custom drawing
- An app whose interactions fit `NavigationSplitView` + `Table` + `.toolbar` + `.searchable` cleanly

Shape A apps use `WindowGroup` / `Window` / `Settings` / `MenuBarExtra` scenes, `NavigationSplitView` for layout, and pure SwiftUI views inside. AppKit shows up only as `NSApplicationDelegate` plumbing for app-lifecycle and notification hooks.

### Shape B: AppKit shell with surgically hosted SwiftUI

An AppKit shell with hosted SwiftUI is the right call when the product needs:

- A **power-user list/outline** with multi-selection drag rearrangement, custom row styling that depends on focus/emphasis, or a context-menu focus ring on the right-clicked row
- **Drag-source lifecycle** beyond "drag started" — knowing when the session ended, where, with which operation, or producing file promises for Finder
- **Keyboard-first workflows** mixing focused text fields with arrow-key navigation through results (Spotlight pattern), modal key handling alongside text input, or vim-style modes
- **Deterministic toolbar layout** with explicit identifier order, allowed/default identifier lists, customization sheet, or tracking separators
- **Rich text editing** beyond plain `TextEditor`
- **Custom window chrome** (title bar accessory views, transparent windows, etc.) or detailed responder-chain control
- **High-volume tables** beyond what `Table` performs at

Shape B apps use `NSWindow`, `NSWindowController`, `NSToolbar`, `NSSplitViewController`, `NSTableView` / `NSOutlineView` for the parts that need power-user behavior, and `NSHostingView` / `NSHostingController` to embed SwiftUI for panes that don't (settings forms, account configuration, mostly-static content). NetNewsWire is a textbook Shape B app.

### Triage signals — pattern-match the request

When asked to build or review a macOS app, look for these signals and use them to pick the shape:

| Signal | Implication |
|---|---|
| "Mostly browsing content, with detail views" | Shape A |
| "Settings-heavy utility" | Shape A |
| "iPhone/iPad app we want on Mac too" | Shape A |
| "Menu bar app" | Shape A |
| "Power-user list/outline with multi-select drag" | Shape B |
| "Drag must know when it was cancelled" | Shape B |
| "Search with arrow keys nav through results" | Shape B |
| "Three-pane layout with deterministic toolbar" | Shape B |
| "Rich text editor with attributed runs" | Shape B |
| "Existing AppKit app adopting SwiftUI" | Shape B |

Many real apps mix shapes — a Shape B main window can have Shape A preferences and onboarding. The wrong call is choosing Shape A when the product needs Shape B affordances and then fighting SwiftUI's gaps.

## Core workflow

1. Classify the task: design review, implementation, migration, bug fix, architecture, or distribution
2. Identify the minimum macOS version, primary UI framework, and whether the app is document-based, window-based, or menu-bar-first
3. Apply the Shape A vs Shape B triage above
4. Load the reference files that match the task instead of reading everything
5. Prefer standard macOS behaviors before inventing custom UI or app flow
6. Call out version constraints, fallback paths, and trade-offs explicitly
7. Distinguish design guidance from API guidance
8. When recommending an API, verify availability against Apple docs before claiming it exists on the target platform/version

## Load the right references

- Read `references/designing-for-macos.md` for macOS-first product and UX decisions, including concrete "iPad-in-a-window" anti-pattern signals
  - *Triggers: design review, native feel, platform expectations, Mac vs iPad patterns, layout density*
- Read `references/windows-navigation.md` for windows, toolbars, sidebars, sheets, popovers, inspectors, and full-screen behavior — including the SwiftUI toolbar determinism caveat
  - *Triggers: WindowGroup, DocumentGroup, NavigationSplitView, NSWindow, NSToolbar, NSSplitViewController, toolbar, sidebar, inspector, sheet, popover, full-screen, window resize*
- Read `references/menus-commands-input.md` for menu bar structure, commands, shortcuts, undo/redo, clipboard, pointer, keyboard, and drag-and-drop — including SwiftUI keyboard and drag-lifecycle gaps
  - *Triggers: menu bar, NSMenu, .commands, CommandGroup, keyboard shortcut, ⌘, undo, redo, copy, paste, context menu, drag and drop, .draggable, .dropDestination, NSDraggingSource, Dock menu, onMoveCommand, onKeyPress*
- Read `references/file-management-documents.md` for open/save/import/export, document workflows, file access, Quick Look, and Finder-facing behavior
  - *Triggers: DocumentGroup, FileDocument, ReferenceFileDocument, NSDocument, NSOpenPanel, NSSavePanel, .fileImporter, .fileExporter, UTType, Quick Look, Finder, open panel, save panel, recent documents, file promises, NSFilePromiseProvider*
- Read `references/accessibility.md` for VoiceOver, keyboard navigation, focus, contrast, motion, and testing — including TextField focus-trap patterns
  - *Triggers: VoiceOver, accessibility, .accessibilityLabel, NSAccessibility, focus, keyboard navigation, contrast, reduce motion, assistive technology*
- Read `references/swiftui-macos.md` for modern SwiftUI patterns specific to macOS — and the documented gaps that should drive bridging decisions
  - *Triggers: SwiftUI on macOS, NavigationSplitView, Table, MenuBarExtra, Settings, .searchable, @FocusState, Observation, scene, SwiftUI commands, SwiftUI toolbar, .draggable, .contextMenu*
- Read `references/appkit-and-bridging.md` for AppKit-heavy work, AppKit-SwiftUI integration, and concrete trigger signals for choosing AppKit
  - *Triggers: AppKit, NSHostingView, NSHostingController, NSViewRepresentable, NSViewControllerRepresentable, coordinator, bridging, responder chain, NSTableView, NSOutlineView, NSDraggingSource, NSToolbarDelegate*
- Read `references/persistence-and-data.md` for SwiftData, Core Data, document data, settings, and migration choices
  - *Triggers: SwiftData, Core Data, @Query, ModelActor, FetchDescriptor, @AppStorage, @SceneStorage, UserDefaults, persistence, migration, schema, database, CloudKit*
- Read `references/platform-capabilities-distribution.md` for sandboxing, bookmarks, extensions, menu bar apps, login items, signing, notarization, and distribution
  - *Triggers: sandbox, entitlement, security-scoped bookmark, App Group, SMAppService, login item, MenuBarExtra, NSStatusItem, extension, Finder Sync, XPC, notarization, Developer ID, Hardened Runtime, Mac App Store, distribution, notarytool*
- Read `references/official-sources.md` for the verification workflow and the canonical Apple source map
  - *Triggers: any time you're about to claim an API exists or recommend a modifier; any availability-related question*

## Non-negotiables

- Prefer Apple-standard windows, toolbars, menus, commands, shortcuts, dialogs, and file flows
- Do not import iOS interaction patterns onto macOS without a clear Mac-specific reason
- Treat accessibility as a default requirement, not a polish pass
- Treat keyboard support, context menus, drag and drop, and undo/redo as core Mac affordances
- If custom UI replaces a standard control, preserve discoverability, keyboard support, and accessibility semantics
- Avoid version-specific or newly announced platform claims unless verified against current official docs
- Don't recommend SwiftUI primitives for affordances they don't fully support (custom-row selection emphasis, drag lifecycle, deterministic toolbar layout, focused-TextField key interception) without acknowledging the gap and offering the AppKit bridge

## Common anti-patterns

- Hiding core actions behind a single overflow menu instead of using the menu bar and toolbar
- Giant touch-sized controls that waste space on desktop
- No keyboard navigation, no shortcuts, or no context menus
- Replacing standard window chrome or toolbar behavior without a strong reason
- Building custom file pickers instead of using system open/save panels
- Treating drag and drop as optional in workflows where files or lists are central
- Importing iOS tab bars, bottom sheets, or navigation stacks where Mac-native sidebars, inspectors, or split views belong
- Choosing Shape A when the product needs Shape B affordances and ending up with custom workarounds for selection emphasis, drag lifecycle, or toolbar layout
- Recommending an API without checking its "Available on" line — the most common source of broken cross-platform code

## Response expectations

- For reviews, explain what is non-native, why it matters on macOS, and the simplest native fix. Be specific — name the affordance, the API, and the bridge if needed
- For implementation guidance, prefer native Apple APIs over third-party abstractions unless there is a strong reason not to
- For architecture questions, lead with the Shape A vs Shape B triage; keep the answer proportional to app size and deployment target
- For file and sandbox questions, address both user experience and entitlement/security implications
- When SwiftUI doesn't do what's asked, say so directly and name the AppKit alternative — don't invent workarounds for documented gaps
- Cite Apple documentation specifically when a claim is non-obvious (especially "Available on" lines and Discussion sections)
