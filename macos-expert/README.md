# macos-expert

An [Agent Skill](https://agentskills.io) for modern macOS development that is explicitly grounded in Apple’s Human Interface Guidelines and official Apple developer documentation.

The goal is not just “Swift on desktop.” The goal is Mac-native product and engineering guidance: windows, menus, toolbars, sidebars, file workflows, accessibility, SwiftUI, AppKit, bridging, persistence, sandboxing, menu bar apps, and shipping.

## Design goals

- Cover the major areas Apple emphasizes for macOS without the obvious gaps
- Prefer stable, official Apple guidance over trend-driven or speculative platform claims
- Reuse already-strong local material where it was genuinely useful
- Keep `SKILL.md` concise and push depth into focused reference files

## Source policy

This skill was built from three source classes, in this order:

1. **Apple Human Interface Guidelines**
2. **Apple Developer API documentation**, verified through the Dash Apple docset where practical
3. **Existing local `macos-development` skill content**, but only when it was already strong and not speculative

If a local note conflicted with Apple’s current guidance, Apple won.

## Primary Apple HIG pages used

- `https://developer.apple.com/design/human-interface-guidelines/designing-for-macos`
- `https://developer.apple.com/design/human-interface-guidelines/windows`
- `https://developer.apple.com/design/human-interface-guidelines/toolbars`
- `https://developer.apple.com/design/human-interface-guidelines/sidebars`
- `https://developer.apple.com/design/human-interface-guidelines/menus`
- `https://developer.apple.com/design/human-interface-guidelines/file-management`
- `https://developer.apple.com/design/human-interface-guidelines/drag-and-drop`
- `https://developer.apple.com/design/human-interface-guidelines/going-full-screen`

## Primary Apple API documentation families used

- AppKit
- SwiftUI
- SwiftData
- Accessibility on macOS
- ServiceManagement
- Quick Look
- Uniform Type Identifiers

## Dash verification notes

The following symbols or APIs were explicitly checked in the Dash Apple docset while building this skill:

- `DocumentGroup`
- `MenuBarExtra`
- `ModelActor`
- `fileImporter`
- `NSHostingView`
- `SMAppService`

## Module-by-module source map

### `SKILL.md`

Synthesized from the Apple sources below plus the repo’s existing skill structure conventions.

### `references/official-sources.md`

Primary basis:

- Apple HIG as the design source of truth
- Apple Developer docs as the API source of truth
- Dash workflow established during creation of this skill

Purpose:

- Make future updates verifiable instead of guess-driven

### `references/designing-for-macos.md`

Primary basis:

- `Designing for macOS`
- related HIG guidance on windows, menus, toolbars, sidebars, drag and drop, and full-screen behavior

Adapted local material:

- the review framing from the previous local `macos-development` skill

### `references/windows-navigation.md`

Primary basis:

- HIG pages for windows, toolbars, sidebars, and full-screen behavior
- SwiftUI scene and navigation APIs
- AppKit window and split-view APIs

Adapted local material:

- selected structure from the old `macos-tahoe-hig.md` and window-related AppKit notes, rewritten to remove Tahoe-specific assumptions

### `references/menus-commands-input.md`

Primary basis:

- HIG guidance for menus and drag-and-drop
- standard macOS command and shortcut expectations
- SwiftUI command APIs and AppKit menu/responder-chain patterns

Adapted local material:

- small portions of the prior SwiftUI/AppKit review notes where they already matched stable Mac conventions

### `references/file-management-documents.md`

Primary basis:

- HIG file-management guidance
- Apple document-based app patterns
- SwiftUI file workflow APIs
- AppKit file panels, document architecture, and Quick Look integration

Adapted local material:

- sandbox and Quick Look notes from the previous local `macos-development` skill, tightened around standard file/document workflows

### `references/accessibility.md`

Primary basis:

- Apple accessibility guidance for macOS
- VoiceOver and accessibility API documentation

Adapted local material:

- significant reuse of the previous local accessibility module because it was already one of the strongest parts of that skill, with the content shortened and normalized around stable macOS guidance

### `references/swiftui-macos.md`

Primary basis:

- SwiftUI scene, navigation, table, command, menu bar, file workflow, and focus APIs for macOS

Adapted local material:

- selected patterns from the previous `swiftui-macos.md`, with the Tahoe-specific bug and design-system sections removed

### `references/appkit-and-bridging.md`

Primary basis:

- AppKit documentation
- `NSHostingView`
- standard representable bridging patterns

Adapted local material:

- substantial reuse of the previous AppKit/SwiftUI bridge content because it was practical and strong, but rewritten to emphasize stable patterns instead of version-fashionable framing

### `references/persistence-and-data.md`

Primary basis:

- SwiftData documentation
- document-based app guidance
- Apple platform conventions for preferences vs documents vs relational app data

Adapted local material:

- selected SwiftData and data-persistence notes from the previous local skill, condensed and reframed around storage-choice decision making

### `references/platform-capabilities-distribution.md`

Primary basis:

- sandboxing and entitlement guidance
- ServiceManagement docs for login items
- extension and Quick Look documentation
- Apple distribution expectations for signed and notarized Mac apps

Adapted local material:

- the strongest parts of the previous sandboxing, menu bar, background, and extension notes, rewritten to stay source-backed and avoid speculative platform claims

## What I intentionally removed

The previous local skill contained several Tahoe-era and Apple Intelligence sections that looked too speculative or too weakly sourced to keep as authoritative guidance. This skill intentionally avoids treating those claims as facts unless they are re-verified against official Apple documentation.

## Install

```bash
npx skills add https://github.com/detailobsessed/agent-skills --skill macos-expert
```

## License

MIT
