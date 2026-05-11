# SwiftUI for macOS

SwiftUI on macOS is good for some app shapes and bad for others. This file is honest about which is which, names the concrete API gaps Apple's own documentation acknowledges, and tells you when to bridge to AppKit instead of working around SwiftUI's limits.

Verify any API claim here against current Apple docs (especially the "Available on" line and Discussion section) before relying on it. SwiftUI evolves; this file may lag.

## Where SwiftUI is the right answer

SwiftUI-only is fine and often best when the app is shaped like:

- A **content browser**: lists of items, detail panes, light forms, settings — read-mostly, tap-to-drill
- A **utility / menu bar app** without a heavy main window
- A **document app** where the content area is your own custom drawing
- A **cross-platform port** where iOS is the primary target and macOS rides along via `#if os(macOS)`
- An app whose main interactions fit `NavigationSplitView` + `Table` + `.toolbar` + `.searchable` cleanly

If your app's center of gravity matches the above, the rest of this file's caveats matter less. Use SwiftUI, ship, move on.

## Where SwiftUI runs out of road

SwiftUI is the wrong primary choice when the Mac-shaped product needs any of:

- A **power-user list/outline** with multi-selection drag rearrangement, custom row styling that depends on focus/emphasis, or a context-menu focus ring on the right-clicked row
- **Drag-source state** beyond "drag started" — knowing when the session ended, where, and with which operation
- **Keyboard-first workflows** mixing focused text fields with arrow-key navigation through results (Spotlight pattern), modal key handling alongside text input, or vim-style navigation
- **Deterministic toolbar layout** with explicit identifier order, allowed/default identifier lists, and overflow control
- **Rich text editing** beyond plain `TextEditor` capabilities
- **Custom window chrome** or detailed responder-chain control
- **High-volume tables** where `Table` performance breaks down

The concrete API gaps that drive this are listed below. None of them are speculation — they're observable from Apple's own documentation as of macOS 15 / SwiftUI's current shape.

## Reach for these first (with current caveats)

- `NavigationSplitView` for source/list/detail layouts.
  - **macOS 13.0+.** Note: SwiftUI auto-adds a sidebar toggle toolbar item on macOS; remove it with `.toolbar(removing: .sidebarToggle)` if you need clean toolbar control (requires macOS 14+).
- `Table` for sortable tabular content.
  - **macOS 12.0+.** Single or multiple selection, sort descriptors, hierarchical rows, column customization. Adequate for tens of thousands of rows in practice; if you need NSTableView-class performance or fine-grained drawing, bridge.
- `WindowGroup`, `Window`, `Settings`, `DocumentGroup` for scenes.
  - `Settings` is the right home for preferences. `Window` (singular, macOS 13.0+) is the right home for a single-instance main window.
- `MenuBarExtra` for menu bar utilities.
  - **macOS 13.0+.** Use `.menuBarExtraStyle(.window)` for popover-like content panels. Set `LSUIElement` in Info.plist for menu-bar-only apps.
- `.toolbar` and `.commands` for primary actions.
  - See the toolbar caveat below — semantic placements are platform-variable by design.
- `.searchable` for standard search.
- `.fileImporter`, `.fileExporter`, `.fileMover` for system file panels.
- `.contextMenu(forSelectionType:menu:primaryAction:)` for selection-aware item menus.
  - See the context-menu caveat below.

## State and observation

- Use the Observation framework (`@Observable`, macOS 14+) on modern targets; `ObservableObject` on older ones.
- Keep view state local; lift shared state to observable models, actors, or repositories.
- Window-scoped state should be separate from app-global state when users may open multiple windows. `@SceneStorage` is the right tool for state that should restore per scene.
- For per-document or per-window controllers that AppKit would model with `NSWindowController`, give them a real lifetime — don't hide them inside transient view structs.

## Scene and window design

- Use additional windows for genuinely separate workspaces, not for dialog-sized tasks. Use sheets, popovers, or inspectors for those.
- `Settings` scene gets ⌘, automatically and lives in the app menu — don't reimplement it.
- `DocumentGroup` only when the app is truly document-based. If you're shoving a database-backed app through it, you'll fight it.
- Pair split-view layouts with toolbars and commands rather than overloading inline buttons.

## Commands, menus, and toolbars

- Treat `.commands` as part of the product surface, not as polish. Mac users expect complete menu coverage.
- Toolbar gets the high-frequency actions; menus get complete coverage; shortcuts get the speed paths.
- Use the standard shortcuts (⌘N, ⌘O, ⌘S, ⌘W, ⌘Z, ⇧⌘Z, ⌘F, ⌘,) before inventing.
- `CommandGroup(replacing:)`, `CommandGroup(after:)`, `CommandGroup(before:)` are the right tools for mutating standard menus.

### Toolbar placement is non-deterministic by design

Apple's `ToolbarItemPlacement` documentation states this directly: "SwiftUI determines the appropriate placement for the item based on this intent and its surrounding context, like the current platform." It also notes: "If not all items fit in the available space, an overflow menu may be created and remaining items placed in that menu."

Implications for Mac-assed apps:

- `.primaryAction`, `.automatic`, `.secondaryAction`, `.principal` are **suggestions** to SwiftUI, not commands.
- You cannot reliably predict where items appear in three-pane layouts.
- There is no SwiftUI analogue to `NSToolbarDelegate.toolbarAllowedItemIdentifiers` or `toolbarDefaultItemIdentifiers` — no way to declare an explicit identifier list and let the system place items by identifier.
- If the toolbar must be deterministic — exact ordering, exact overflow rules, customizable via the standard customization sheet — host the window in AppKit and use `NSToolbar`. SwiftUI inside the toolbar items is fine; SwiftUI managing the toolbar is the problem.

## Mac-specific affordances — what works and what doesn't

These are the SwiftUI primitives that map to AppKit affordances, with the gaps Apple's docs imply or state.

### `.contextMenu` and `.contextMenu(forSelectionType:menu:primaryAction:)`

Works for: showing a contextual menu, varying contents by selection set, attaching a primary (double-click) action.

Does not work for:

- **Knowing whether a context menu is currently open.** No environment value, no callback. If you need to dim the rest of the UI or change row styling while the menu is up, you cannot.
- **Styling the context-menu target row.** AppKit's `NSTableView` draws a focus ring around the right-clicked row even when it isn't the selection; SwiftUI's `List` does this automatically and you can't customize it. Custom rows in `ScrollView`/`LazyVStack` get nothing.
- **Distinguishing menu activation on a selection vs an empty area** beyond what `forSelectionType`'s closure tells you (empty set vs non-empty set). The selection itself is unchanged by right-click.

### `.draggable(_:)` and `.draggable(_:preview:)`

Works for: declaring a view as a drag source with `Transferable` payload and an optional preview view. **macOS 13.0+ / iOS 16.0+.**

Does not work for:

- **Drag-session lifecycle.** Apple's documentation lists the related APIs as exactly `draggable(_:preview:)` and `dropDestination(…)`. There is no SwiftUI equivalent to `NSDraggingSource.draggingSession(_:willBeginAt:)`, `draggingSession(_:movedTo:)`, or — most importantly — `draggingSession(_:endedAt:operation:)`.
- **Knowing the drag was cancelled or dropped outside the window.** If you dim the source view on drag start, you have no callback to undim it on cancel/abort.
- **Custom drag images per item, controlled at session level.** You get one preview per source view.

If drag-and-drop is operationally important to your app (reorder, move-between-containers, drag-out-to-Finder, drag-with-modifier-keys), bridge to `NSDraggingSource`. The conforming AppKit views — `NSTableView`, `NSOutlineView`, `NSCollectionView`, `NSTextView` — give you the full lifecycle.

### `@FocusState` and `.focusable(_:)`

Works for: declaring focus state, moving focus between specific fields, gating actions on focused field. **`focusable(_:)` is macOS 12.0+.**

Does not work for:

- **The Spotlight pattern.** When a `TextField` has focus, it consumes character input including arrow keys for cursor movement. You can attach `onKeyPress(_:action:)` (macOS 14+ / iOS 17+) and return `.ignored` to bubble the event, but the TextField is still the first responder and the interaction model is fragile compared to AppKit's responder chain.
- **Modal key handling alongside text editing.** AppKit's `keyDown(with:)` overrides on subclassed views give you precise control; SwiftUI's `onKeyPress` is an overlay that interacts opaquely with focus.

If keyboard handling is central to the app — search bar with arrow nav through results, vim-style modes, chord shortcuts, modal key handling — host the window in AppKit.

### `onMoveCommand(perform:)`

Works for: arrow-key movement on macOS and tvOS.

Does not work for:

- **iPadOS or iOS.** Apple's documentation explicitly lists availability as "macOS 10.15+, tvOS 13.0+." iPad supports hardware keyboards but `onMoveCommand` does not. Cross-platform code needs `#if os(macOS) || os(tvOS)` for `onMoveCommand` and `onKeyPress` (iOS 17+ / macOS 14+) for the iPad path, with different semantics.

### `onKeyPress(_:action:)` and variants

Works for: hardware key handling on a focused view. **iOS 17.0+ / macOS 14.0+.** Returns `.handled` or `.ignored` so events can bubble.

Does not work for:

- **Pre-iOS 17 / pre-macOS 14 deployment targets.**
- **First-responder-aware behavior.** It runs only when the view is focused. There is no SwiftUI analogue to `NSResponder.keyDown(with:)` on a non-focused view, and no equivalent to `performKeyEquivalent(with:)` on the responder chain.

### `.help`, `.alternatingRowBackgrounds`, `.tableStyle`, `.searchable`, `.contentMargins`

These are uncontroversial. Use them. Note availability: `.alternatingRowBackgrounds(_:)` is macOS 14+; `.contentMargins` is iOS 17+ / macOS 14+. The others are macOS 11+ or earlier.

### Inactive-window appearance

`@Environment(\.appearsActive)` (macOS 10.15+, back-deployed) gives you the active/inactive flag for current Mac apps. The deprecated `controlActiveState` maps to it. `Color.accentColor`, `ShapeStyle.selection`, and selection in `List`/`Table` automatically desaturate when inactive.

For custom views, observe `\.appearsActive` and adjust styling. This is the one classic Mac affordance SwiftUI handles cleanly today.

### De-emphasized selection in custom rows

`@Environment(\.backgroundProminence)` (iOS 17+ / macOS 14+) communicates "this row is selected and currently emphasized" to children — but **only inside `List` and `Table`.** Apple's documentation states: "Views like `List` and `Table` … will automatically update the background prominence of foreground views."

If you build custom row layouts in `ScrollView` + `LazyVStack` because `List` doesn't allow the customization you need, `backgroundProminence` won't help and you're back to manual focus tracking through environment plumbing.

## Choosing the framework for the row container

| Need | Use |
| --- | --- |
| Plain rows, system look, selection, swipe actions | `List` |
| Tabular data, sortable columns, multi-select, column customization | `Table` |
| Custom row layouts that don't need precise selection-emphasis behavior | `ScrollView` + `LazyVStack` |
| Custom row layouts that **do** need selection emphasis, drag rearrangement, context-menu focus ring, or large data scale | bridge to `NSTableView` / `NSOutlineView` via `NSViewRepresentable` |

## When SwiftUI is not enough — concrete trigger signals

Bridge to AppKit (or build the shell in AppKit and host SwiftUI inside) when you hit any of these:

- You're reaching for `ScrollView` + `LazyVStack` because `List` won't let you customize selection, and now you've lost selection emphasis behavior
- You need `NSDraggingSource`'s `draggingSession(_:endedAt:operation:)` because something must happen when the drag is cancelled
- You need a context menu focus ring on the right-clicked row, or to know the menu is open
- You need a search field that lets arrow keys navigate the result list while the field has focus
- You need deterministic toolbar layout, allowed/default identifier lists, or the standard toolbar customization sheet
- You need rich text editing (attributed runs, custom layout, paragraph attributes) beyond `TextEditor`
- You need `NSTableView`/`NSOutlineView` performance for tens of thousands of rows with custom drawing
- You need detailed `NSWindow` control: custom title bar, accessory view controllers, tab groups, screensaver-class behavior

The bridge can go either direction. See `appkit-and-bridging.md`.

## Review checklist

- SwiftUI scene types match the app's real workflow (`Window` vs `WindowGroup` vs `DocumentGroup` vs `Settings` vs `MenuBarExtra`)
- Power-user affordances (selection emphasis, drag lifecycle, context-menu focus, keyboard nav with focused text) either work natively or have a deliberate AppKit bridge
- Toolbar items are simple enough that platform-variable placement is acceptable, **or** the toolbar is `NSToolbar`
- Observation and state lifetimes are clean; window-scoped state uses `@SceneStorage` where appropriate
- `@Observable` is used on modern targets
- Cross-platform code accounts for `onMoveCommand` not existing on iOS/iPadOS
- Bridging is introduced where SwiftUI demonstrably runs out of road, not as a hedge

## Pair this file with

- `appkit-and-bridging.md` for when and how to bridge to AppKit
- `windows-navigation.md` for window, toolbar, and navigation layout guidance, including the toolbar determinism caveat
- `menus-commands-input.md` for commands, shortcuts, menu structure, and drag-and-drop pitfalls
- `persistence-and-data.md` for SwiftData and document storage choices
- `official-sources.md` for verifying API availability before quoting modifiers in implementation guidance
