# Windows and navigation

Use standard macOS containers and navigation patterns before creating custom shells.

## Choose the right top-level structure

- Use **`WindowGroup`** for standard app windows
- Use **`DocumentGroup`** for document-based apps
- Use **`Settings`** for preferences
- Use **`MenuBarExtra`** for menu bar utilities
- Use **secondary windows** for inspectors, previews, dashboards, or editors when they are truly separate workspaces

## Window behavior

- Support resizing gracefully; do not hard-code a single usable size unless the app is genuinely fixed-purpose
- Preserve useful state such as selection, sidebar visibility, and inspector visibility
- Use full-screen support where it helps sustained work, not as a substitute for window design
- Support multiple windows when users may compare, edit, or monitor more than one item at once

## Toolbars

Toolbars should expose the actions users need often, not every action the app has.

Good toolbar content:

- Sidebar toggle
- Search
- View mode or filter controls
- Primary actions like add, share, or refresh
- Inspector toggle when relevant

Avoid:

- Putting destructive or rare actions in the most prominent spot
- Duplicating a dense toolbar and a dense inline action bar
- Replacing standard toolbar placements with arbitrary custom ordering

## Navigation patterns

### Sidebar and content

Prefer split-view patterns for hierarchical or list/detail apps:

- Two-column for list/detail or source/detail
- Three-column when there is a meaningful intermediate level

Use tabs only when sections are true peers and do not benefit from a shared sidebar.

### Sheets, popovers, and inspectors

- Use **sheets** for focused tasks that block progress in the current window
- Use **popovers** for lightweight, contextual controls
- Use **inspectors** for persistent secondary details that should stay available while the user works

## SwiftUI defaults

- `NavigationSplitView`
- `WindowGroup`, `Window`, `Settings`, `DocumentGroup`
- `.toolbar`, `.toolbarRole`, `.defaultSize`, `.windowToolbarStyle`
- `.searchable` for standard in-window search where search is a primary workflow
- `openWindow(id:)` when auxiliary windows are appropriate

## AppKit defaults

- `NSWindow` and `NSWindowController`
- `NSToolbar`
- `NSSplitViewController`
- `NSPanel` for utility-style supporting windows
- `NSPopover` for transient contextual UI

## Review checklist

- Window titles and hierarchy are clear
- The main action areas are reachable from toolbar or standard controls
- The app uses sidebars and inspectors where macOS users expect them
- Full-screen is supported sensibly for content-heavy tasks
- Auxiliary windows exist only when they represent a real separate workspace

## Pair this file with

- `designing-for-macos.md` for broader macOS product and UX expectations
- `menus-commands-input.md` for toolbar actions, commands, and shortcuts
- `swiftui-macos.md` for SwiftUI scene and navigation API patterns
- `appkit-and-bridging.md` for AppKit window and split-view details
