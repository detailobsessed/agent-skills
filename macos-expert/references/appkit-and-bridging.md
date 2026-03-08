# AppKit and AppKit-SwiftUI bridging

AppKit is still the right answer for some macOS problems. Use it deliberately, and keep the bridge thin.

## Prefer AppKit when

- text editing goes beyond basic text fields or plain text editors
- tables, outlines, or collection views need mature desktop behavior or high scale
- you need detailed window, responder-chain, or menu control
- you are migrating an existing AppKit app incrementally
- SwiftUI lacks a native capability or imposes unacceptable performance or lifecycle trade-offs

## Bridge directions

### AppKit hosting SwiftUI

Use:

- `NSHostingView`
- `NSHostingController`

This is the best default for incrementally adopting SwiftUI inside an AppKit app.

### SwiftUI hosting AppKit

Use:

- `NSViewRepresentable`
- `NSViewControllerRepresentable`

This is the best default when SwiftUI is the shell but specific controls still need AppKit.

## Bridging rules

- Keep the bridge boundary narrow; do not hide an entire architecture problem inside representables
- Put durable mutable state in observable models or controllers, not in transient view structs
- Update coordinators carefully so they do not hold stale references
- Clean up observers, delegates, tasks, and notifications in dismantle paths
- Let SwiftUI manage layout where possible instead of hard-coding frames from AppKit setup code

## AppKit-native guidance

- Use `NSToolbar`, `NSSplitViewController`, `NSTableView`, `NSOutlineView`, `NSVisualEffectView`, `NSOpenPanel`, and `NSSavePanel` before building custom replacements
- Use the responder chain and menu validation for command behavior
- Preserve standard selection, editing, and keyboard behaviors

## Review checklist

- AppKit is used for a concrete reason, not just habit
- Hosted SwiftUI and wrapped AppKit views have clear ownership and state flow
- Coordinators, delegates, and notifications are cleaned up correctly
- Layout and resizing remain stable
- Standard AppKit controls are preferred over unnecessary custom widgets
