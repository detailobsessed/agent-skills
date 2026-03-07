---
name: macos-expert
description: Comprehensive modern macOS app development guidance grounded in Apple’s Human Interface Guidelines and official Apple developer documentation. Use when building, reviewing, or refactoring macOS software with SwiftUI, AppKit, AppKit-SwiftUI bridging, SwiftData, accessibility, menus, windows, toolbars, sidebars, document and file workflows, drag and drop, sandboxing, distribution, or other Mac-specific platform behavior.
---

# macos-expert

Use this skill to keep macOS work native, modern, and source-backed.

## Source priority

Use sources in this order:

1. Apple Human Interface Guidelines and Apple Developer documentation
2. Dash Apple docsets for API verification
3. Reference files in this skill

If a named API, symbol, modifier, entitlement, or platform behavior is uncertain, verify it in Dash before presenting it as fact.

Start with `references/official-sources.md` if you need the verification workflow or the canonical Apple source map.

## Load the right references

- Read `references/designing-for-macos.md` for macOS-first product and UX decisions
- Read `references/windows-navigation.md` for windows, toolbars, sidebars, sheets, popovers, inspectors, and full-screen behavior
- Read `references/menus-commands-input.md` for menu bar structure, commands, shortcuts, undo/redo, clipboard, pointer, keyboard, and drag-and-drop expectations
- Read `references/file-management-documents.md` for open/save/import/export, document workflows, file access, Quick Look, and Finder-facing behavior
- Read `references/accessibility.md` for VoiceOver, keyboard navigation, focus, contrast, motion, and testing
- Read `references/swiftui-macos.md` for modern SwiftUI patterns specific to macOS
- Read `references/appkit-and-bridging.md` for AppKit-heavy work and AppKit-SwiftUI integration
- Read `references/persistence-and-data.md` for SwiftData, Core Data, document data, settings, and migration choices
- Read `references/platform-capabilities-distribution.md` for sandboxing, bookmarks, extensions, menu bar apps, login items, signing, notarization, and distribution

## Core workflow

1. Classify the task: design review, implementation, migration, bug fix, architecture, or distribution
2. Identify the minimum macOS version, primary UI framework, and whether the app is document-based, window-based, or menu-bar-first
3. Load the reference files that match the task instead of reading everything
4. Prefer standard macOS behaviors before inventing custom UI or app flow
5. Call out version constraints, fallback paths, and trade-offs explicitly
6. Distinguish design guidance from API guidance

## Non-negotiables

- Prefer Apple-standard windows, toolbars, menus, commands, shortcuts, dialogs, and file flows
- Do not import iOS interaction patterns onto macOS without a clear Mac-specific reason
- Treat accessibility as a default requirement, not a polish pass
- Treat keyboard support, context menus, drag and drop, and undo/redo as core Mac affordances
- If custom UI replaces a standard control, preserve discoverability, keyboard support, and accessibility semantics
- Avoid speculative Tahoe-era or Apple Intelligence claims unless verified against current official docs

## Response expectations

- For reviews, explain what is non-native, why it matters on macOS, and the simplest native fix
- For implementation guidance, prefer native Apple APIs over third-party abstractions unless there is a strong reason not to
- For architecture questions, keep the answer proportional to app size and deployment target
- For file and sandbox questions, address both user experience and entitlement/security implications
