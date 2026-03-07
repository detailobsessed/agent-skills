# Menus, commands, shortcuts, and input

Menus and commands are part of the product surface on macOS. Treat them as first-class UI.

## Standard menu expectations

Preserve the standard macOS structure unless there is a strong reason not to:

- App menu
- File
- Edit
- View
- Window
- Help

Add custom menus only when a domain has enough commands to justify one.

## Command coverage

Core actions should usually be available in more than one place:

- Toolbar or inline UI for discoverability
- Menu item for completeness and keyboard access
- Keyboard shortcut for speed when appropriate
- Context menu when the action is object-specific

## Keyboard shortcuts

Prefer established conventions:

- New: `⌘N`
- Open: `⌘O`
- Save: `⌘S`
- Close window: `⌘W`
- Undo / Redo: `⌘Z` / `⇧⌘Z`
- Find: `⌘F`
- Preferences / Settings: `⌘,`

Do not override fundamental system shortcuts casually.

## Undo, redo, clipboard, and selection

For editable content, support the Mac basics:

- Undo / redo
- Cut / copy / paste
- Select all
- Find / replace where text is central
- Drag and drop for reordering or file ingress/egress when relevant

If the app owns rich document workflows, commands should integrate cleanly with the responder chain or SwiftUI command system.

## Context menus

Use context menus to accelerate object-level actions:

- Open
- Rename
- Duplicate
- Move
- Share
- Delete

Context menus should supplement the app’s main command surface, not replace it.

## Pointer and keyboard interaction

- Hover can enhance but must not be the only way to discover or trigger important actions
- Keyboard focus order must be logical
- Lists and tables should work with arrow keys, selection, and standard activation patterns
- Right-click and control-click should reveal contextual actions where users expect them

## Drag and drop

Treat drag and drop as a core Mac affordance in file-centric and list-centric apps:

- Accept dropped files when importing is central to the workflow
- Support dragging items out when export or reuse makes sense
- Support reordering by drag where lists or collections are user-managed

## SwiftUI tools

- `.commands`
- `CommandGroup` and `CommandMenu`
- `.keyboardShortcut`
- `.contextMenu`
- `.draggable` and `.dropDestination`
- `@FocusState`
- `.help`

## AppKit tools

- `NSMenu`, `NSMenuItem`, `NSMenuItemValidation`
- responder chain actions
- `NSPasteboard`
- `NSDraggingSource` and `NSDraggingDestination`
- `validateUserInterfaceItem(_:)`

## Review checklist

- The app’s primary actions are visible in menus
- Important shortcuts follow Mac conventions
- Undo/redo and copy/paste exist where users expect them
- Context menus and drag-and-drop improve workflows instead of duplicating clutter
- Keyboard navigation is complete enough for expert use
