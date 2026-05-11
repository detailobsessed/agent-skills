# Designing for macOS

This reference turns Apple's macOS HIG into a practical review and implementation lens.

## Core macOS principles

- Design for **keyboard, mouse, trackpad, and menu bar**, not just direct-manipulation touch metaphors
- Treat **windows** as first-class workspaces — users multitask across multiple windows, apps, displays, and Spaces
- Use the **menu bar, toolbars, sidebars, inspectors, context menus, drag and drop, and clipboard** as part of the core experience
- Favor **clarity, efficiency, and information density** over oversized mobile-style layouts
- Respect the system's appearance, typography, focus model, accent color, sidebar styling, and accessibility settings
- Mac users expect every command to live in a menu, every menu item to have a stable location, and every primary action to have a keyboard path

## What "native on macOS" usually means

- The app has a sensible menu structure with all commands present, including standard items
- Important actions are discoverable from menus, toolbars, or contextual UI — not only from one
- Windows resize well and preserve useful state across launches
- Sidebar/list/detail layouts use standard column behavior instead of custom chrome
- Dialogs, sheets, popovers, and panels are used for the right level of interruption
- Users can move data with copy/paste, drag and drop, import/export, and open/save flows
- Inactive windows desaturate; selection emphasis behaves correctly when focus moves
- Drag and drop has lifecycle (sources know when their drag was cancelled)
- Right-click reveals context menus with the right items for the clicked target

## "iPad app in a window" signals

When reviewing a Mac app, these are the concrete signs that an iOS-shaped product was shipped on Mac without translation. Each is worth flagging:

- The window has a tab bar at the bottom instead of a sidebar at the leading edge
- Important actions live only in floating buttons or only in a single overflow menu — no menu bar coverage
- No keyboard shortcuts beyond what `keyboardShortcut(_:)` auto-provides on a button
- The window can't resize meaningfully, or has no minimum / maximum / ideal size
- Right-click does nothing or shows a menu copied from iOS that lacks Mac conventions (Open, Show in Finder, Copy, Reveal, etc.)
- Lists don't respond to arrow keys, Return, or Space
- No undo, no copy/paste plumbing, no drag and drop on file-shaped data
- "Settings" lives inside a navigation stack instead of in `Settings` (⌘,)
- Fonts, paddings, and tap targets are touch-sized rather than mouse-sized
- The app uses iOS-style sheet presentation for tasks Mac would model as a panel, sheet, or inspector

## Review heuristics

When reviewing a macOS app, ask:

1. Does this feel like a Mac app or an iPad app placed in a window?
2. Are the main actions available from the right places: menu bar, toolbar, context menu, keyboard?
3. Does the app support multiple windows or document flows where users would expect them?
4. Are advanced tasks efficient with keyboard and pointer input?
5. Does the app cooperate with Finder, file dialogs, and standard system services?
6. Do inactive windows and de-emphasized selections look right when focus moves?
7. Does drag and drop have correct lifecycle, or does it leave the UI in inconsistent states on cancel?

## Common anti-patterns

- Hiding core actions behind a single overflow menu instead of using the menu bar and toolbar
- Replacing normal window chrome or toolbar behavior without a strong reason
- Giant touch-sized controls that waste space on desktop
- No keyboard navigation, no shortcuts, or no context menus
- Treating drag and drop as optional in workflows where files or lists are central
- Building custom file pickers instead of using system open/save panels
- Using SwiftUI primitives for affordances they don't fully support (custom-row selection emphasis, drag lifecycle, menu-state observation, deterministic toolbar layout) without bridging
- Tab bars where a sidebar belongs
- iOS-style "back" navigation in a window that should use real navigation columns

## What to prefer by default

- `NavigationSplitView`, `Table`, `Form`, system toolbars, standard alerts and confirmation dialogs in SwiftUI
- `NSWindow`, `NSToolbar`, `NSSplitViewController`, `NSTableView`, `NSOutlineView`, `NSOpenPanel`, `NSSavePanel` in AppKit
- Standard macOS commands for About, Settings, Hide, Quit, Window management, Find, Undo/Redo, Copy/Paste
- The Mac convention of disabling, not hiding, temporarily unavailable menu items

## When SwiftUI alone is enough

A pure-SwiftUI Mac app is the right call when:

- The product is a content browser, settings-heavy utility, or cross-platform port whose iOS shape carries over reasonably
- Lists are mostly read-only or simple-edit; no drag rearrangement with lifecycle, no custom selection emphasis, no context-menu focus styling
- Toolbars are simple enough that platform-variable placement is fine
- Keyboard handling is limited to standard shortcuts, not search-while-arrow-nav patterns
- One main `Window` or `WindowGroup`, optional `Settings`, optional `MenuBarExtra`

## When AppKit is the right shell

Use an AppKit shell with surgically hosted SwiftUI when:

- The main window is a power-user list/outline/detail layout (NetNewsWire shape, Mail shape, source-list-driven)
- Custom selection emphasis, context-menu focus rings, or drag rearrangement with live indicators are required
- Drag-source lifecycle matters operationally (cancel handling, file promises, drop-outside-window)
- Toolbars need deterministic placement, customization sheets, tracking separators, or specialized item identifiers
- Keyboard handling extends to focused-text-field-with-arrow-nav patterns, modal modes, or custom responder participation

The "AppKit shell, hosted SwiftUI inside" pattern (`NSHostingView` / `NSHostingController`) gets you the best of both: AppKit owns the parts SwiftUI is bad at, SwiftUI owns the parts it's good at.

## Pair this file with

- `windows-navigation.md` for layout and scene structure, plus toolbar determinism caveats
- `menus-commands-input.md` for shortcuts, commands, pointer, drag-and-drop, and SwiftUI keyboard gaps
- `file-management-documents.md` for file-centric workflows
- `accessibility.md` for inclusive interaction requirements
- `swiftui-macos.md` for SwiftUI patterns and the documented gaps
- `appkit-and-bridging.md` for AppKit shell patterns and bridging
