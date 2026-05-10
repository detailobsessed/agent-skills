# Accessibility on macOS

Accessibility is part of correctness on macOS, not an optional polish pass. The Mac platform's accessibility expectations are higher than iOS — VoiceOver and Full Keyboard Access users expect every action to be reachable without a pointer.

## Non-negotiables

- Every interactive element has a clear accessible name
- Keyboard-only navigation can complete the app's primary workflows
- Focus order is logical and visible
- Information is not conveyed by color alone
- Motion-heavy UI respects reduced-motion settings
- Custom controls expose the correct role and state, not a generic "button" fallback

## VoiceOver

- Prefer standard controls first; they carry strong semantics automatically
- Add labels, values, hints, and roles only where defaults are incomplete
- Combine child elements when a row or card should read as one unit (`.accessibilityElement(children: .combine)`)
- Hide decorative visuals from the accessibility tree (`.accessibilityHidden(true)`)
- For custom controls, provide the correct role, value, and adjustable/action semantics

## Keyboard and focus

- Support tab navigation through forms and primary controls (Full Keyboard Access)
- Make list, table, sidebar, and detail workflows practical from the keyboard
- Expose menu commands and shortcuts for core actions
- Keep focus stable during updates, inserts, and view transitions; don't yank focus mid-edit
- Test with Tab, Shift-Tab, arrow keys, Return, Space, and Esc in every primary flow

### Focus traps to watch for

- A `TextField` with focus consumes arrow keys for cursor movement. If the surrounding workflow expects arrow keys to navigate a result list while the field is focused (Spotlight pattern), SwiftUI alone won't deliver it cleanly. `onKeyPress(_:action:)` returning `.ignored` is partial — see `menus-commands-input.md` and `swiftui-macos.md` for the bridging signal
- Custom focus rings drawn over views may suppress the system focus ring; preserve the system one or replicate it pixel-accurately
- Modal sheets and popovers must restore focus to the previous control on dismissal

## Tables, lists, and data-dense UI

- Use `Table`, `List`, `NSTableView`, or `NSOutlineView` semantics instead of free-form grids when the content is tabular — these give VoiceOver row/column context for free
- Custom rows built in `ScrollView` + `LazyVStack` lose row semantics; you'll need explicit `.accessibilityElement(children:)`, row position via `.accessibilityValue`, and rotor support if the list is large
- Make row purpose, selection state, and activation behavior obvious to assistive tech
- Avoid custom list rows that look rich visually but read poorly with VoiceOver

## Visual accessibility

- Use semantic colors where possible (`Color.primary`, `.secondary`, `.accentColor`, `.red` only for genuinely red things)
- Meet at least WCAG AA contrast targets for text and critical UI
- Respect Increase Contrast and Differentiate Without Color settings (`@Environment(\.colorSchemeContrast)`, `@Environment(\.accessibilityDifferentiateWithoutColor)`)
- Ensure hover-only affordances have an always-visible fallback for keyboard or assistive-tech users
- Inactive-window styling should not push contrast below threshold

## Motion and animation

- Respect Reduce Motion (`@Environment(\.accessibilityReduceMotion)`)
- Prefer short, informative transitions over decorative motion
- Use non-motion alternatives like state changes, outlines, icons, or text when motion is reduced
- Auto-play behavior must be disabled when Reduce Motion is on

## SwiftUI tools

- `.accessibilityLabel`, `.accessibilityValue`, `.accessibilityHint`
- `.accessibilityElement(children:)`
- `.accessibilityAddTraits`, `.accessibilityRemoveTraits`
- `.accessibilityHidden`
- `.accessibilityAdjustableAction`, `.accessibilityAction`
- `.accessibilityRotor` for grouped navigation in long content
- `@FocusState`, `.focusable(_:)`, `.focused(_:)`
- `@Environment(\.accessibilityReduceMotion)`, `\.accessibilityDifferentiateWithoutColor`, `\.accessibilityReduceTransparency`, `\.accessibilityVoiceOverEnabled`

## AppKit tools

- `NSAccessibility` overrides and setters for custom views (`accessibilityRole`, `accessibilityLabel`, `accessibilityValue`, `accessibilityChildren`)
- `NSAccessibilityElement` for non-view accessibility nodes
- `nextKeyView` / `previousKeyView` to control tab order
- Menu validation and responder-chain actions for keyboard-driven command coverage
- Accessibility Inspector and VoiceOver testing

## Test like this

- Turn on VoiceOver and walk every primary workflow start-to-finish
- Test with keyboard only — disable mouse / trackpad mentally for a session
- Increase text size and contrast in System Settings
- Enable Reduce Motion and verify the app degrades gracefully
- Check empty, error, loading, and selection states with VoiceOver
- Use the Accessibility Inspector's audit feature to catch missing labels and contrast issues
- Test sidebar / timeline / detail patterns specifically — Mac users with Full Keyboard Access live here

## Review checklist

- Labels, values, hints, and roles are complete on custom controls
- Primary workflows are keyboard-complete with no dead ends
- Focus does not jump unpredictably or get trapped in `TextField`s
- Complex rows, custom controls, and tables remain understandable to VoiceOver
- Custom containers (`ScrollView` + `LazyVStack`) have explicit row semantics
- Contrast, motion, and transparency settings are respected
- AppKit views in a SwiftUI shell have explicit `NSAccessibility` setup
- Menu bar coverage gives every action a keyboard-reachable path

## Pair this file with

- `designing-for-macos.md` for macOS interaction expectations that affect accessibility
- `menus-commands-input.md` for keyboard shortcuts, command coverage, and the TextField focus-trap discussion
- `swiftui-macos.md` for SwiftUI accessibility modifiers and the focus/TextField gap
- `appkit-and-bridging.md` for AppKit accessibility overrides and bridging concerns
