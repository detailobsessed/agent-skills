# Accessibility on macOS

Accessibility is part of correctness on macOS, not an optional polish pass.

## Non-negotiables

- Every interactive element has a clear accessible name
- Keyboard-only navigation can complete the app’s primary workflows
- Focus order is logical and visible
- Information is not conveyed by color alone
- Motion-heavy UI respects reduced-motion settings

## VoiceOver

- Prefer standard controls first; they carry strong semantics automatically
- Add labels, values, hints, and roles only where the defaults are incomplete
- Combine child elements when a row or card should read as one unit
- Hide decorative visuals from the accessibility tree
- For custom controls, provide the correct role and adjustable/action semantics

## Keyboard and focus

- Support tab navigation through forms and primary controls
- Make list, table, sidebar, and detail workflows practical from the keyboard
- Expose menu commands and shortcuts for core actions
- Keep focus stable during updates, inserts, and view transitions

## Tables, lists, and data-dense UI

- Use `Table`, `List`, `NSTableView`, or `NSOutlineView` semantics instead of free-form grids when the content is tabular
- Make row purpose, selection state, and activation behavior obvious
- Avoid custom list rows that look rich visually but read poorly with assistive technology

## Visual accessibility

- Use semantic colors where possible
- Meet at least WCAG AA contrast targets for text and critical UI
- Respect increased-contrast and differentiate-without-color settings
- Ensure hover-only affordances have an always-visible fallback for keyboard or assistive-tech users

## Motion and animation

- Respect reduce-motion preferences
- Prefer short, informative transitions over decorative motion
- Use non-motion alternatives like state, outline, icon, or text changes when necessary

## SwiftUI tools

- `.accessibilityLabel`, `.accessibilityValue`, `.accessibilityHint`
- `.accessibilityElement(children:)`
- `.accessibilityAddTraits`
- `.accessibilityHidden`
- `.accessibilityAdjustableAction`
- `@FocusState`

## AppKit tools

- `NSAccessibility` overrides and setters
- `nextKeyView`
- menu validation and responder-chain actions
- Accessibility Inspector and VoiceOver testing

## Test like this

- Turn on VoiceOver and walk the primary workflows
- Test the app with keyboard only
- Increase text size and contrast settings
- Check common empty, error, loading, and selection states

## Review checklist

- Labels, values, hints, and roles are complete
- Primary workflows are keyboard-complete
- Focus does not jump unpredictably
- Complex rows, custom controls, and tables remain understandable to VoiceOver
- Contrast and motion settings are respected

## Pair this file with

- `designing-for-macos.md` for macOS interaction expectations that affect accessibility
- `menus-commands-input.md` for keyboard shortcuts and command coverage
- `swiftui-macos.md` for SwiftUI accessibility modifiers and focus APIs
- `appkit-and-bridging.md` for AppKit accessibility overrides and bridging concerns
