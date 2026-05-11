# Menus, commands, shortcuts, and input

Menus, commands, and the responder chain are part of the product surface on macOS. Treat them as first-class UI, not a polish layer.

This file covers menu structure, keyboard expectations, context menus, drag-and-drop, and the SwiftUI gaps in each — so you know when SwiftUI primitives are enough and when AppKit's responder chain wins.

## Standard menu expectations

Preserve the standard macOS structure unless there is a strong reason not to:

- App menu
- File
- Edit
- View
- Window
- Help

Add custom menus only when a domain has enough commands to justify one.

Keep standard menu items visible even when temporarily unavailable; **disable**, don't hide. The Mac convention is that menu items are discoverable in the same place every time.

## App-wide menu basics

- Put About, Settings, Hide, Hide Others, Show All, and Quit in the app menu (SwiftUI's `Settings` scene wires ⌘, automatically)
- Support the system Services submenu where it applies to the current context
- Help menu is small and focused
- File menu has New (`⌘N`), Open (`⌘O`), Open Recent, Close (`⌘W`), Save (`⌘S`), Save As (`⇧⌘S`), Revert, Print (`⌘P`) where applicable
- Edit menu has standard Cut/Copy/Paste/Delete/Select All plus Undo/Redo and Find/Find Next where applicable

## Command coverage

Core actions should usually be available in more than one place:

- Toolbar or inline UI for discoverability
- Menu item for completeness and keyboard access
- Keyboard shortcut for speed when appropriate
- Context menu when the action is object-specific

This is the "law of three places" Mac users internalize. Skipping the menu is the most common iOS-import mistake.

## Keyboard shortcuts

Prefer established conventions:

- New: `⌘N`
- Open: `⌘O`
- Save: `⌘S`
- Close window: `⌘W`
- Quit: `⌘Q`
- Undo / Redo: `⌘Z` / `⇧⌘Z`
- Find / Find Next / Find Previous: `⌘F` / `⌘G` / `⇧⌘G`
- Preferences / Settings: `⌘,`
- Print: `⌘P`
- Select All: `⌘A`
- Cut / Copy / Paste: `⌘X` / `⌘C` / `⌘V`
- Hide / Hide Others: `⌘H` / `⌥⌘H`
- Minimize: `⌘M`
- Toggle full-screen: `⌃⌘F`

Do not override fundamental system shortcuts casually. If you must, use a modifier combination that doesn't collide with system reservations.

## Undo, redo, clipboard, and selection

For editable content, support the Mac basics:

- Undo / redo (use `UndoManager`; SwiftUI `@Environment(\.undoManager)`)
- Cut / copy / paste / delete
- Select all
- Find / replace where text is central
- Drag and drop for reordering or file ingress/egress when relevant

If the app owns rich document workflows, commands should integrate with the responder chain or SwiftUI's `.commands` system. AppKit's responder chain delivers the action to the focused control automatically; SwiftUI's `.commands` is global to the scene and is not focus-aware in the same way (see `appkit-and-bridging.md` for the gap).

## Context menus

Use context menus to accelerate object-level actions:

- Open
- Rename
- Duplicate
- Move
- Share
- Show in Finder / Reveal
- Delete (destructive role)

Context menus should supplement the app's main command surface, not replace it.

### SwiftUI context menu options

- `.contextMenu(menuItems:)` — simple, view-attached menu. macOS doesn't show the contextMenu *preview* on Mac (Apple's docs note this explicitly: "This view modifier produces a context menu on macOS, but that platform doesn't display a preview")
- `.contextMenu(forSelectionType:menu:primaryAction:)` (macOS 13.0+) — selection-aware menu attached to a `List` or `Table`. The closure receives a `Set<I>` of selected items; an empty set means activation in empty space
- `primaryAction:` runs on macOS double-click / iOS tap

### What SwiftUI context menus don't do

- **No "menu is open" signal.** No environment value, no callback. You cannot dim the rest of the UI or change row styling while the menu is up
- **No focus ring on the right-clicked row** in custom containers. `NSTableView` and `NSOutlineView` automatically draw a focus ring on the right-clicked row even when it isn't selected; SwiftUI's `List` does this internally but you can't customize it, and `ScrollView`/`LazyVStack` rows get nothing
- **No way to vary preview shape** beyond `contentShape(_:_:eoFill:)` with `.contextMenuPreview` kind on iOS

If knowing the menu state is operationally important, bridge to AppKit's `NSMenu` and `menuNeedsUpdate(_:)` / `menu(_:willHighlight:)`.

## Dock menus

Dock menus are a macOS-only shortcut surface for high-value actions when the app is running but not frontmost.

- Prefer a small set of high-value items (recent windows, new-item actions, refresh/sync)
- Make custom Dock menu items available elsewhere too — never the only route to a command
- SwiftUI: `.commands` doesn't expose Dock menu directly; use `NSApplicationDelegate.applicationDockMenu(_:)` (which SwiftUI lets you wire via `@NSApplicationDelegateAdaptor`)

## Pointer and keyboard interaction

- Hover affordances must not be the only way to discover or trigger important actions — keyboard and click paths must work too
- Keyboard focus order must be logical
- Lists and tables must work with arrow keys and standard activation (Return, Space, Enter)
- Right-click and Control-click must reveal contextual actions where users expect them
- `.help(_:)` for tooltips on focusable controls

## Keyboard handling and the SwiftUI gap

SwiftUI offers a layered set of keyboard primitives:

- `keyboardShortcut(_:modifiers:)` — declares a shortcut for a button or command
- `.commands { CommandMenu("…") { Button("Action", action: …).keyboardShortcut(…) } }` — declares scene-level commands
- `onKeyPress(_:action:)` and variants (macOS 14.0+ / iOS 17.0+) — observe key events on a focused view; return `.handled` or `.ignored`
- `onMoveCommand(perform:)` — arrow-key handler. **macOS 10.15+ and tvOS 13.0+ only — not iOS or iPadOS.** This is a real cross-platform footgun
- `onDeleteCommand`, `onExitCommand`, `onPlayPauseCommand` — semantic commands

### What SwiftUI keyboard handling doesn't do

- **The Spotlight pattern.** When a `TextField` has focus, it consumes character input including arrow keys for cursor movement. `onKeyPress` returning `.ignored` is partial mitigation, but the TextField is still the first responder. AppKit's responder chain with explicit `keyDown(with:)` overrides on a subclassed `NSTextField` or `NSSearchField` is the right tool when you need search-while-typing with arrow-nav-through-results
- **Non-focused key handling.** `onKeyPress` only fires when the view is focused. AppKit's `NSResponder.keyDown(with:)` overrides plus `performKeyEquivalent(with:)` give you precise control without focus
- **Cross-platform arrow keys.** `onMoveCommand` works on macOS/tvOS; on iPadOS you need `onKeyPress(.upArrow)` etc. with different semantics. Cross-platform code needs `#if` branches

### When to bridge to AppKit for keys

- Search field with arrow keys navigating result list
- vim-style or modal key handling
- Chord shortcuts (multi-key sequences)
- Menu validation that depends on which view has focus
- Any custom `NSResponder` participation in the chain

## Drag and drop

Treat drag and drop as a core Mac affordance in file-centric and list-centric apps:

- Accept dropped files when importing is central
- Support dragging items out when export or reuse makes sense
- Support reordering by drag where lists are user-managed

### SwiftUI drag and drop

- `.draggable(_:)` — declare a view as a drag source with a `Transferable` payload (macOS 13.0+)
- `.draggable(_:preview:)` — same, with a custom preview view
- `.dropDestination(for:action:isTargeted:)` — drop target with `Transferable`
- `Transferable` and `ProxyRepresentation` for payload types

### What SwiftUI drag-and-drop doesn't do

Apple's documentation lists exactly two related modifiers next to `draggable(_:)`: `draggable(_:preview:)` and `dropDestination(…)`. There is no SwiftUI equivalent to:

- `NSDraggingSource.draggingSession(_:willBeginAt:)` — drag started callback with location
- `NSDraggingSource.draggingSession(_:movedTo:)` — drag-in-progress callback
- `NSDraggingSource.draggingSession(_:endedAt:operation:)` — **drag ended, success or cancellation, with the operation result**
- `NSDraggingSource.ignoreModifierKeys(for:)` — modifier-key behavior control
- `NSFilePromiseProvider` — lazy file generation for drops to Finder
- Per-item drag images that differ from the source view rendering
- Multi-component drag images via `NSDraggingItem.imageComponentsProvider`

This means you cannot:

- Dim the source on drag start and reliably undim it on cancel/abort
- React when the drop target was outside the window or returned no operation
- Promise files that should be created lazily on drop

### When to bridge to AppKit for drag

- Drag rearrangement in lists with live drop indicators (use `NSTableView`/`NSOutlineView`, both `NSDraggingSource` conforming)
- Dragging-out-to-Finder with file promises (`NSFilePromiseProvider`)
- Any UI behavior that depends on drag-end state
- Modifier-key-aware drag behavior

The conforming AppKit types out of the box: `NSCollectionView`, `NSOutlineView`, `NSTableView`, `NSTextView`. They give you the full lifecycle for free.

## SwiftUI tools

- `.commands`, `CommandGroup`, `CommandMenu`, `CommandGroupPlacement` (`.replacing`, `.before`, `.after`)
- `.keyboardShortcut(_:modifiers:)`
- `.contextMenu(menuItems:)` and `.contextMenu(forSelectionType:menu:primaryAction:)`
- `.draggable(_:)` and `.dropDestination(for:action:isTargeted:)`
- `@FocusState`, `.focusable(_:)`, `.focused(_:)`
- `.onKeyPress(_:action:)`, `.onMoveCommand(perform:)`, `.onDeleteCommand`, `.onExitCommand`
- `.help(_:)` for tooltips
- `@Environment(\.undoManager)`

## AppKit tools

- `NSMenu`, `NSMenuItem`, `NSMenuItemValidation`
- `NSMenuDelegate.menuNeedsUpdate(_:)` for dynamic context menus
- Responder chain actions and `NSResponder.keyDown(with:)`
- `validateUserInterfaceItem(_:)` and `NSUserInterfaceValidations`
- `NSPasteboard`, `NSPasteboardItem`, `NSPasteboardWriting`, `NSPasteboardReading`
- `NSDraggingSource`, `NSDraggingDestination`, `NSDraggingItem`, `NSDraggingSession`
- `NSFilePromiseProvider`
- `UndoManager`

## Review checklist

- Primary actions appear in menus, not only in toolbars or popovers
- Important shortcuts follow Mac conventions
- Undo/redo and copy/paste exist where users expect them
- Context menus and drag-and-drop improve workflows instead of duplicating clutter
- Keyboard navigation is complete enough for expert use
- If keyboard or drag handling needs lifecycle behavior SwiftUI can't express, AppKit is used at that seam
- Menu validation is responder-chain-aware where focus matters

## Pair this file with

- `designing-for-macos.md` for macOS-first product and interaction expectations
- `windows-navigation.md` for toolbar placement and window structure
- `accessibility.md` for keyboard navigation and focus requirements
- `file-management-documents.md` for drag-and-drop file workflows
- `appkit-and-bridging.md` for responder chain, menu validation, and AppKit drag/menu bridging
