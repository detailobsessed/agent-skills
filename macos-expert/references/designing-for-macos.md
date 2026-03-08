# Designing for macOS

This reference turns Apple’s macOS HIG into a practical review and implementation lens.

## Core macOS principles

- Design for **keyboard, mouse, trackpad, and menu bar**, not just direct-manipulation touch metaphors
- Treat **windows** as first-class workspaces
- Expect users to multitask across multiple windows, apps, and displays
- Use the **menu bar, toolbars, sidebars, inspectors, context menus, drag and drop, and clipboard** as part of the core experience
- Favor **clarity, efficiency, and information density** over oversized mobile-style layouts
- Respect the system’s appearance, typography, focus model, accent color, and accessibility settings

## What “native on macOS” usually means

- The app has a sensible menu structure and keyboard shortcuts
- Important actions are discoverable from menus, toolbars, or contextual UI
- Windows resize well and preserve useful state
- Sidebar/list/detail layouts use standard column behavior instead of custom chrome
- Dialogs, sheets, popovers, and panels are used for the right level of interruption
- Users can move data with copy/paste, drag and drop, import/export, and open/save flows

## Review heuristics

When reviewing a macOS app, ask:

1. Does this feel like a Mac app or an iPad app placed in a window?
2. Are the main actions available from the right places: menu bar, toolbar, context menu, keyboard?
3. Does the app support multiple windows or document flows where users would expect them?
4. Are advanced tasks efficient with keyboard and pointer input?
5. Does the app cooperate with Finder, file dialogs, and standard system services?

## Common anti-patterns

- Hiding core actions behind a single overflow menu
- Replacing normal window chrome or toolbar behavior without a strong reason
- Giant touch-sized controls that waste space on desktop
- No keyboard navigation, no shortcuts, or no context menus
- Treating drag and drop as optional in workflows where files or lists are central
- Building custom file pickers instead of using system open/save panels

## What to prefer by default

- `NavigationSplitView`, `Table`, `Form`, system toolbars, standard alerts and confirmation dialogs in SwiftUI
- `NSWindow`, `NSToolbar`, `NSSplitViewController`, `NSTableView`, `NSOpenPanel`, and `NSSavePanel` in AppKit
- Standard macOS commands for About, Settings, Hide, Quit, Window management, Find, Undo/Redo, Copy/Paste

## Pair this file with

- `windows-navigation.md` for layout and scene structure
- `menus-commands-input.md` for shortcuts, commands, pointer, and drag-and-drop behavior
- `file-management-documents.md` for file-centric workflows
- `accessibility.md` for inclusive interaction requirements
