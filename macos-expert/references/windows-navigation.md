# Windows and navigation

Use standard macOS containers and navigation patterns before creating custom shells. Match the scene type to the workflow, not the other way around.

## Choose the right top-level structure

- `WindowGroup` — the user can open multiple instances of this window (browse-style, multi-document editor, multi-room chat)
- `Window` (singular, macOS 13.0+) — a single-instance main window. Use this when the app conceptually has *one* main window (most utilities, most "iOS app on Mac" ports, most browser-like content apps)
- `DocumentGroup` — the app is genuinely document-based and benefits from `NSDocument`-style behavior (open recent, autosave, version browser, file-tied lifecycle)
- `Settings` — preferences. Auto-binds ⌘, and lives in the app menu
- `MenuBarExtra` — menu bar utility (macOS 13.0+). Pair with `LSUIElement = true` in Info.plist for menu-bar-only apps. Use `.menuBarExtraStyle(.window)` for popover-like content panels
- Secondary `Window` or `WindowGroup` scenes — inspectors, dashboards, or genuinely separate workspaces. Don't use auxiliary windows for dialog-sized tasks; use sheets, popovers, or inspectors

## Window behavior

- Support resizing gracefully; don't hard-code a single usable size unless the app is genuinely fixed-purpose
- Use `.windowResizability(.contentSize)` only when content really should drive the window dimensions
- Preserve useful state: selection, sidebar visibility, inspector visibility, scroll position. `@SceneStorage` is the right primitive for per-scene state restoration
- Use full-screen support where it benefits sustained work, not as a substitute for window design
- Support multiple windows when users may compare, edit, or monitor more than one item at once

## Toolbars

Toolbars expose actions users need often, not every action the app has.

Good toolbar content:

- Sidebar toggle (added automatically by `NavigationSplitView` on macOS — remove with `.toolbar(removing: .sidebarToggle)` if you need clean control; `.toolbar(removing:)` requires macOS 14+)
- Search (or use `.searchable` which lives in the right toolbar slot)
- View mode or filter controls
- Primary actions: add, share, refresh
- Inspector toggle when relevant

Avoid:

- Putting destructive or rare actions in the most prominent spot
- Duplicating a dense toolbar and a dense inline action bar
- Replacing standard toolbar placements with arbitrary custom ordering

### SwiftUI toolbar placement is non-deterministic by design

Apple's `ToolbarItemPlacement` documentation states this directly: "SwiftUI determines the appropriate placement for the item based on this intent and its surrounding context, like the current platform." It also warns: "If not all items fit in the available space, an overflow menu may be created and remaining items placed in that menu."

Implications:

- Semantic placements (`.primaryAction`, `.secondaryAction`, `.principal`, `.automatic`, `.status`) are *intents*, not commands. SwiftUI decides the actual location per platform and per layout context
- Three-pane layouts (`NavigationSplitView` with content + detail) are particularly hard to predict
- There is no SwiftUI analogue to `NSToolbarDelegate.toolbarAllowedItemIdentifiers` / `toolbarDefaultItemIdentifiers` — no way to declare an explicit identifier list, allow user customization via the standard sheet, or control overflow rules
- Tracking separators between split-view columns require `NSTrackingSeparatorToolbarItem`, which has no SwiftUI counterpart

Use `NSToolbar` (host the window in AppKit, embed SwiftUI inside toolbar items via `NSHostingView` if needed) when any of these matter:

- Exact item ordering
- Customization sheet behavior
- Tracking separators
- Overflow control
- Search-field placement that must follow column boundaries

For most apps, SwiftUI's toolbar is fine. Reach for AppKit's toolbar deliberately, not as a default.

## Navigation patterns

### Sidebar and content

Prefer split-view patterns for hierarchical or list/detail apps:

- Two-column for list/detail or source/detail (`NavigationSplitView { sidebar } detail: { … }`)
- Three-column when there is a meaningful intermediate level (`NavigationSplitView { sidebar } content: { … } detail: { … }`)

Use tabs only when sections are true peers and don't benefit from a shared sidebar. On macOS, tabs feel iOS-y unless they're inside a content view that genuinely has tabbed sub-sections (e.g. a debugger pane).

### `NavigationSplitView` notes

- macOS 13.0+
- Auto-adds a sidebar toggle toolbar item; remove via `.toolbar(removing: .sidebarToggle)`
- Column widths via `.navigationSplitViewColumnWidth(_:)` or `.navigationSplitViewColumnWidth(min:ideal:max:)`
- Style via `.navigationSplitViewStyle(.balanced)` or `.prominentDetail` if the visual emphasis matters
- Programmatic visibility via `NavigationSplitViewVisibility` binding
- Compact-class collapse behavior: SwiftUI auto-stacks columns; on iPad in Slide Over the table inside hides headers and additional columns. macOS doesn't hit this path

### Sheets, popovers, inspectors

- Sheets for focused tasks that block progress in the current window
- Popovers for lightweight contextual controls
- `.inspector(isPresented:content:)` (macOS 14.0+) for persistent secondary details that stay available while the user works

## SwiftUI defaults

- `NavigationSplitView` for split layouts
- `WindowGroup`, `Window`, `Settings`, `DocumentGroup`, `MenuBarExtra` for scenes
- `.toolbar`, `.toolbarRole(.editor)`/`.browser`, `.defaultSize`, `.windowResizability`, `.windowToolbarStyle`
- `.searchable` for in-window search
- `.inspector` for persistent secondary panes
- `openWindow(id:value:)` from the environment when auxiliary windows make sense

## AppKit defaults

- `NSWindow` and `NSWindowController`
- `NSToolbar`, `NSToolbarItem`, `NSToolbarDelegate`, `NSTrackingSeparatorToolbarItem`, `NSSearchToolbarItem`
- `NSSplitViewController` and `NSSplitViewItem` for column behavior with persisted holding priorities and collapse animations
- `NSPanel` for utility-style supporting windows (HUD-style if appropriate)
- `NSPopover` for transient contextual UI
- `NSTitlebarAccessoryViewController` for title-bar accessory views

## Review checklist

- Window titles, scene types, and hierarchy match how the user thinks about the app
- The main action areas are reachable from toolbar or standard controls
- Sidebars, inspectors, and split-view conventions are used where Mac users expect them
- Full-screen behaves sensibly for content-heavy tasks
- Auxiliary windows exist only when they represent a real separate workspace
- Toolbar layout requirements (deterministic, customizable, with tracking separators) drive the choice between SwiftUI's `.toolbar` and `NSToolbar`
- State restoration is wired (`@SceneStorage`, AppKit `NSWindow.restorationClass`)

## Pair this file with

- `designing-for-macos.md` for broader macOS product and UX expectations
- `menus-commands-input.md` for toolbar actions, commands, and shortcuts
- `swiftui-macos.md` for SwiftUI scene and navigation API patterns and known gaps
- `appkit-and-bridging.md` for AppKit window, toolbar, and split-view details and bridging
