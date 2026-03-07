# macos-expert

An [Agent Skill](https://agentskills.io) for modern macOS development that is explicitly grounded in Apple’s Human Interface Guidelines and official Apple developer documentation.

The goal is not just “Swift on desktop.” The goal is Mac-native product and engineering guidance: windows, menus, toolbars, sidebars, file workflows, accessibility, SwiftUI, AppKit, bridging, persistence, sandboxing, menu bar apps, and shipping.

## Design goals

- Cover the major areas Apple emphasizes for macOS without the obvious gaps
- Prefer stable, official Apple guidance over trend-driven or speculative platform claims
- Keep the skill cohesive and self-contained
- Keep `SKILL.md` concise and push depth into focused reference files

## Source policy

This skill was built from Apple’s own macOS design and developer documentation first, then synthesized into practical reference modules for repeated use.

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

During authoring, the Dash MCP server was used to cross-check concrete Apple symbols and APIs. The skill files themselves intentionally refer only to official Apple documentation.

The following symbols or APIs were explicitly checked this way while building the skill:

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

Purpose:

- Make future updates verifiable instead of guess-driven

### `references/designing-for-macos.md`

Primary basis:

- `Designing for macOS`
- related HIG guidance on windows, menus, toolbars, sidebars, drag and drop, and full-screen behavior

Emphasis:

- a review lens that turns Apple’s HIG principles into practical macOS product heuristics

### `references/windows-navigation.md`

Primary basis:

- HIG pages for windows, toolbars, sidebars, and full-screen behavior
- SwiftUI scene and navigation APIs
- AppKit window and split-view APIs

Emphasis:

- standard Mac windowing and navigation patterns over version-fashionable design framing

### `references/menus-commands-input.md`

Primary basis:

- HIG guidance for menus and drag-and-drop
- standard macOS command and shortcut expectations
- SwiftUI command APIs and AppKit menu/responder-chain patterns

Emphasis:

- standard commands, shortcuts, menus, and drag-and-drop as first-class Mac UI

### `references/file-management-documents.md`

Primary basis:

- HIG file-management guidance
- Apple document-based app patterns
- SwiftUI file workflow APIs
- AppKit file panels, document architecture, and Quick Look integration

Emphasis:

- standard file and document workflows instead of custom file UX

### `references/accessibility.md`

Primary basis:

- Apple accessibility guidance for macOS
- VoiceOver and accessibility API documentation

Emphasis:

- stable accessibility guidance centered on VoiceOver, keyboard navigation, and visual accessibility

### `references/swiftui-macos.md`

Primary basis:

- SwiftUI scene, navigation, table, command, menu bar, file workflow, and focus APIs for macOS

Emphasis:

- SwiftUI patterns that feel native on macOS rather than generic cross-platform usage

### `references/appkit-and-bridging.md`

Primary basis:

- AppKit documentation
- `NSHostingView`
- standard representable bridging patterns

Emphasis:

- using AppKit deliberately and keeping the AppKit-SwiftUI bridge thin

### `references/persistence-and-data.md`

Primary basis:

- SwiftData documentation
- document-based app guidance
- Apple platform conventions for preferences vs documents vs relational app data

Emphasis:

- matching storage technology to the user’s mental model and app shape

### `references/platform-capabilities-distribution.md`

Primary basis:

- sandboxing and entitlement guidance
- ServiceManagement docs for login items
- extension and Quick Look documentation
- Apple distribution expectations for signed and notarized Mac apps

Emphasis:

- treating capabilities, entitlements, and distribution decisions as both UX and engineering concerns

## What I intentionally removed

During authoring, I discarded any concrete claims that I could not corroborate in Apple’s own documentation. That especially affected version-specific, newly announced, or overly specific platform assertions that named APIs or behaviors without clear support in Apple’s published materials.

## Install

```bash
npx skills add https://github.com/detailobsessed/agent-skills --skill macos-expert
```

## License

MIT
