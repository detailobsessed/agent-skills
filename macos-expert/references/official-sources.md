# Official sources and verification workflow

Use Apple’s own materials as the source of truth for this skill.

## Source hierarchy

1. **Apple Human Interface Guidelines**
   - `Designing for macOS`
   - topic pages for windows, menus, toolbars, sidebars, file management, drag and drop, and full-screen behavior
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
   - Use for version-specific changes and new platform behavior

## Verification workflow

Use current official Apple documentation to verify APIs and behavior:

1. Search for the concrete symbol or topic
2. If a search for several words fails, search smaller pieces like the exact type or modifier name
3. Load the matching page before claiming the API exists or recommending its usage
4. If you cannot find the API in Apple’s current documentation, assume the name may be wrong or outdated and reframe the answer around verified APIs

## What must be verified

Verify in official docs when any of these appear:

- New or unfamiliar SwiftUI modifiers
- Entitlements, Info.plist keys, or sandbox behavior
- New menu bar, background task, or extension APIs
- Availability by macOS version
- Any newly announced or rapidly changing platform claims

## Topic-to-source map

- **Design and UX** → HIG pages
- **Framework and symbols** → Apple API reference documentation
- **Availability / modern platform changes** → API docs, release notes, WWDC
- **Distribution / signing / notarization** → Apple developer docs

## Working rule

If any draft guidance disagrees with Apple’s current documentation, prefer Apple and update the draft guidance.
