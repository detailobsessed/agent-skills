# SwiftUI for macOS

Prefer SwiftUI patterns that feel native on macOS rather than cross-platform abstractions that flatten Mac behavior.

## Reach for these first

- `NavigationSplitView` for source/list/detail layouts
- `Table` for data-heavy or sortable tabular content
- `WindowGroup`, `Window`, `Settings`, and `DocumentGroup` for scenes
- `.toolbar` and `.commands` for primary actions
- `.searchable` for standard search UI instead of custom search chrome
- `MenuBarExtra` for menu bar utilities
- `.fileImporter`, `.fileExporter`, and `.dropDestination` for file workflows

## State and observation

- Prefer the Observation framework on modern deployment targets
- Keep view state local and lightweight
- Move shared business state into observable models, actors, or repositories rather than bloated views
- Keep window-scoped state separate from app-global state when users may open multiple windows

## Scene and window design

- Use additional windows for real secondary workspaces, not for every dialog-sized task
- Keep settings in `Settings`
- Use `DocumentGroup` when the app is truly document-based
- Pair split-view layouts with toolbars and commands instead of overloading inline buttons

## Commands, menus, and toolbars

- Treat `.commands` as part of the product, not as an afterthought
- Put high-frequency actions in the toolbar
- Put complete command coverage in menus
- Use standard shortcuts before inventing new ones

## Mac-specific affordances

- Use `.contextMenu` and `.help`
- Support keyboard focus with `@FocusState`
- Use drag and drop for files, reordering, and object movement where appropriate
- Prefer `Table` over custom grid layouts for true desktop data views

## When SwiftUI is not enough

Bridge to AppKit when you need:

- richer text editing
- higher-performance tables or outlines
- mature document architecture
- highly customized windows or responder-chain behavior
- advanced drag-and-drop, menu, or view lifecycle control

## Review checklist

- SwiftUI scene types match the app’s real workflow
- Split-view, table, menu, and toolbar patterns feel native on macOS
- Observation and state lifetimes are clean
- Mac-specific affordances are present instead of emulated
- AppKit is introduced only where SwiftUI meaningfully falls short

## Pair this file with

- `appkit-and-bridging.md` for when and how to bridge to AppKit
- `windows-navigation.md` for window, toolbar, and navigation layout guidance
- `menus-commands-input.md` for commands, shortcuts, and menu structure
- `persistence-and-data.md` for SwiftData and document storage choices
