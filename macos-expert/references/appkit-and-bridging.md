# AppKit and AppKit-SwiftUI bridging

AppKit is alive, supported, and still the right answer for some macOS app shapes. Use it deliberately. Keep the bridge thin.

This file covers (1) when AppKit beats SwiftUI on Mac, (2) how to bridge in either direction, and (3) the responder-chain and menu-validation patterns SwiftUI doesn't replicate.

## Prefer AppKit when — concrete trigger signals

Reach for AppKit (either as the app shell or for specific subsystems) when any of these are true. These are the signals SwiftUI's primitives don't reach.

### List/outline behavior

- You need a context menu focus ring on the right-clicked row even when it isn't selected — `NSTableView` and `NSOutlineView` do this automatically; SwiftUI's `List` does it but you can't customize, and `ScrollView`/`LazyVStack` don't do it at all
- You need de-emphasized selection styling in **custom row layouts** (not `List`/`Table`) — `NSTableRowView.isEmphasized` and `NSView.BackgroundStyle` give you this; SwiftUI's `\.backgroundProminence` only fires inside `List`/`Table`
- You need multi-row drag rearrangement with live drop indicators
- You need outline disclosure with custom expand/collapse animation or styling
- Row count is large (tens of thousands+) and `Table` performance is unacceptable
- You need column customization persisted via standard menus, with view-based tracking separators

### Drag and drop

- You need `draggingSession(_:endedAt:operation:)` to react to cancellation, drop-outside-window, or final operation result
- You need `draggingSession(_:movedTo:)` to update UI during the drag
- You need `NSFilePromiseProvider` for lazy file generation on drop
- You need per-item drag images that differ from the source view rendering
- You need `NSDraggingItem.imageComponentsProvider` for multi-component drag previews

### Keyboard and responder chain

- You need a focused text field to coexist with arrow-key navigation through results (Spotlight pattern)
- You need `performKeyEquivalent(with:)` participation through the responder chain
- You need menu validation via `NSMenuItemValidation` / `validateUserInterfaceItem(_:)` so menu state reflects responder context
- You need precise key-event interception on non-focused views via `NSResponder.keyDown(with:)` overrides
- You need vim-style modal key handling, chord shortcuts, or other custom key models

### Toolbar

- You need deterministic placement, an explicit allowed/default identifier list (`NSToolbarDelegate.toolbarAllowedItemIdentifiers`, `toolbarDefaultItemIdentifiers`), and the standard toolbar customization sheet
- You need a toolbar tracking separator anchored to a split view divider
- You need search-field, segmented-control, or other specialized toolbar item identifiers without the SwiftUI ones
- You need `NSToolbarItemGroup` with subitem behaviors

### Windows

- You need custom title bar accessory view controllers
- You need a transparent or custom-shaped window
- You need precise window resize behavior, content-aspect-ratio constraints, or `NSWindow.collectionBehavior` flags SwiftUI doesn't expose
- You need to participate in the window-tabs system explicitly
- You need `NSPanel` semantics for utility windows
- You need to drive multiple windows from a single controller with shared state, fully

### Text editing

- You need attributed-run editing, custom layout managers, paragraph attributes, find/replace UI integration, ruler bars, or any of `NSTextView`'s editing surface beyond plain text
- You need to drive `NSTextStorage` for syntax highlighting or LSP integration

### Document architecture

- You're migrating from an existing `NSDocument`-based app
- You need autosave, version browser, document tabs, or `NSDocumentController` behavior `DocumentGroup` doesn't expose

If none of these apply, SwiftUI is probably fine. See `swiftui-macos.md`.

## Bridge directions

### AppKit hosting SwiftUI (recommended for Mac-assed apps)

Use:

- `NSHostingView` to embed a SwiftUI view inside an AppKit view hierarchy
- `NSHostingController` when you want a view controller wrapping a SwiftUI root

This is the right default for:

- Existing AppKit apps adopting SwiftUI incrementally
- New apps where the shell is AppKit (windows, toolbars, sidebar/timeline/detail) and panes inside the shell are SwiftUI (forms, settings, mostly-static content)

The NetNewsWire pattern: AppKit `NSWindowController`, `NSToolbar`, `NSOutlineView`, `NSTableView` for the main window; SwiftUI views hosted inside the accounts pane and similar leaf surfaces.

### SwiftUI hosting AppKit

Use:

- `NSViewRepresentable` to wrap a single AppKit view
- `NSViewControllerRepresentable` to wrap a controller-backed view

This is the right default for:

- Cross-platform apps that are SwiftUI-first but need a specific AppKit control (rich text editor, web view, professional table)
- Embedding AppKit-only system views (`NSPathControl`, `NSColorWell` historically, `NSVisualEffectView`)

Watch the seams: `Coordinator` is where most bugs live. Make it a class with explicit lifecycle, hold weak references where the AppKit view is the strong owner, and clean up observers, delegates, and Combine subscriptions in `dismantleNSView` / `dismantleNSViewController`.

## Bridging rules

- Keep the bridge boundary narrow. Do not hide an architectural decision inside a representable
- Put durable mutable state in observable models or controllers, not in transient view structs
- Update coordinators on `updateNSView(_:context:)` carefully; don't reapply state that hasn't changed
- Clean up observers, KVO, delegates, tasks, and notifications in dismantle paths
- Let SwiftUI manage layout where possible; avoid hard-coding frames inside AppKit setup code
- Don't bridge for the sake of it. If the SwiftUI view in question fits SwiftUI cleanly, ship it; if the AppKit view fits AppKit cleanly, ship it; bridge only at the seam

## Responder chain and menu validation

This is a SwiftUI gap that's easy to miss. AppKit's responder chain is how Mac apps deliver commands to the right object based on focus, and it's how menu items know when to enable, disable, change title, or show a checkmark.

- First responder receives the action; if it doesn't handle, the action walks up the chain through superviews, view controllers, the window, the window controller, the app delegate, the application
- `NSMenuItem.isEnabled` is driven by `NSMenuItemValidation.validateMenuItem(_:)` or `NSUserInterfaceValidations.validateUserInterfaceItem(_:)` on whichever responder claims it
- Standard items (Cut/Copy/Paste, Undo/Redo, Find, etc.) walk the chain so the focused control gets first crack

In SwiftUI, `.commands` plus `Button(action:)` partially substitutes, but commands are global to the scene rather than focus-aware. If menu state must reflect the focused view, AppKit's responder chain is the right primitive.

## AppKit-native guidance

Prefer the standard AppKit primitives before building custom replacements:

- `NSToolbar` and `NSToolbarItem` (including `NSSearchToolbarItem`, `NSSharingServicePickerToolbarItem`, `NSTrackingSeparatorToolbarItem`) over custom toolbars
- `NSSplitViewController` over hand-rolled split views
- `NSTableView` and `NSOutlineView` over custom row containers
- `NSCollectionView` for grid/icon layouts
- `NSVisualEffectView` for vibrancy
- `NSOpenPanel` and `NSSavePanel` for file dialogs
- `NSAlert` for alerts; `NSPanel` for utility windows
- `NSPasteboard`, `NSPasteboardItem`, `NSPasteboardWriting`, `NSPasteboardReading` for clipboard and drag payloads

Preserve standard selection, editing, and keyboard behaviors — Mac users notice when these don't work the system way.

## Common AppKit pitfalls

- Forgetting to set `delegate` and `dataSource` after waking from a nib or programmatic init
- KVO observers not removed before deallocation
- `NSWindowController` retained nowhere — windows can vanish under you
- Auto layout fights with `setFrame:`/`autoresizingMask`-based sizing; pick one model per view
- `NSTableCellView` reuse races: configure cells defensively in `tableView(_:viewFor:row:)`
- Forgetting `automaticallyManagesSubscriptions` semantics on Combine bridges
- Hosting a SwiftUI view inside AppKit and assuming it'll resize correctly without an `NSHostingView` sizing pass

## Review checklist

- AppKit is used for a concrete trigger signal, not because of habit or aesthetic preference
- Hosted SwiftUI and wrapped AppKit views have clear ownership and explicit state flow
- Coordinators, delegates, KVO, and notifications are cleaned up in dismantle paths
- Layout and resizing are stable across resize and full-screen
- Standard AppKit controls are preferred over custom widgets
- Responder chain and menu validation are used where focus-aware command behavior matters

## Pair this file with

- `swiftui-macos.md` for SwiftUI-first patterns, what works, and the documented gaps
- `windows-navigation.md` for AppKit window, toolbar, and split-view details
- `menus-commands-input.md` for responder chain, menu validation, and drag-and-drop
- `accessibility.md` for AppKit accessibility overrides and testing
