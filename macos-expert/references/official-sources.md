# Official sources and verification workflow

Use Apple's own materials as the source of truth for this skill. The skill files codify patterns; Apple's docs codify APIs. When the two disagree, Apple wins and the skill file should be updated.

## Source hierarchy

1. **Apple Human Interface Guidelines**
   - `Designing for macOS`
   - Topic pages for windows, menus, toolbars, sidebars, file management, drag and drop, full-screen behavior
2. **Apple Developer API documentation**
   - SwiftUI
   - AppKit
   - Accessibility
   - SwiftData
   - ServiceManagement
   - Quick Look
   - Uniform Type Identifiers
   - Security-scoped bookmarks and sandbox-related docs
3. **Apple release notes and WWDC sessions**
   - For version-specific changes and new platform behavior
4. **WWDC sample code and the "Building a great Mac app with SwiftUI" sample**
   - For up-to-date Apple-blessed patterns

## Verification workflow

When recommending an API or modifier, verify it against Apple's current docs:

1. Search for the concrete symbol or topic
2. If a multi-word search fails, search the exact type or modifier name
3. Load the matching page before claiming the API exists or recommending its usage
4. **Read the "Available on" line carefully** — this is where most stale guidance fails. APIs that exist on macOS 14+ may not exist on macOS 13, and APIs that exist on macOS may not exist on iOS or vice versa
5. **Read the Discussion section** — Apple often documents constraints there that aren't visible from the signature alone (e.g. "this only works inside `List` and `Table`")
6. If you cannot find the API in Apple's current documentation, assume the name may be wrong, deprecated, or third-party and reframe the answer around verified APIs

## Platform availability — the most common stale-guidance bug

SwiftUI APIs are not uniformly available across platforms. Recurring traps:

- `onMoveCommand(perform:)` — macOS 10.15+ and tvOS 13.0+ only. **Not iOS or iPadOS.** Cross-platform code must guard with `#if`
- `onKeyPress(_:action:)` — iOS 17.0+ / macOS 14.0+. Doesn't exist on older targets
- `MenuBarExtra` — macOS 13.0+ only
- `Window` (singular scene) — macOS 13.0+ only; older code must use `WindowGroup`
- `.inspector(isPresented:content:)` — macOS 14.0+ / iOS 17.0+
- `appearsActive` — exists on iOS 18+ / macOS 15+ in declared form, back-deployed to macOS 10.15. Use the back-deployed shim where appropriate
- `backgroundProminence` — iOS 17+ / macOS 14+, **and only inside `List`/`Table`**
- `.contextMenu(forSelectionType:menu:primaryAction:)` — macOS 13.0+ / iOS 16.0+
- `.draggable(_:)` and `.draggable(_:preview:)` — macOS 13.0+ / iOS 16.0+

When deployment target matters, always check the "Available on" line.

## What must be verified

Verify in official docs whenever any of these appear in your guidance:

- New or unfamiliar SwiftUI modifiers
- Entitlements, Info.plist keys, or sandbox behavior
- Menu bar, background task, or extension APIs
- Availability by macOS version
- Any newly announced or rapidly changing platform claims (especially within 18 months of WWDC release)
- SwiftData behavior on the macOS version targeted (this surface has changed meaningfully release-to-release)
- CloudKit, ServiceManagement, and notarization tooling (`notarytool` vs `altool`)

## Topic-to-source map

- **Design and UX** → HIG pages
- **Framework and symbols** → Apple API reference documentation
- **Availability / modern platform changes** → API docs ("Available on" line), release notes, WWDC sessions
- **Distribution / signing / notarization** → Apple developer docs (`Distributing your app`, notarization, hardened runtime pages)
- **Sample code patterns** → official Apple sample projects, especially the SwiftUI Mac app sample

## Working rule

If any draft guidance disagrees with Apple's current documentation, prefer Apple and update the draft guidance. If guidance describes a *gap* in an API (something the API doesn't do), confirm the gap by reading the related-APIs section of Apple's doc — if Apple lists no API for the missing capability, the gap is real.

## When Apple's docs are silent

Some real platform behavior isn't documented (or is documented only in WWDC video transcripts). For those cases:

- Treat the WWDC transcript as a primary source
- Treat well-respected community write-ups (e.g. observations from Apple-experienced developers) as secondary signal, not authoritative
- Note explicitly when guidance is based on observation rather than Apple's published docs, so future updates can re-verify
- Prefer a verifiable, narrower claim over an unverifiable, broader one
