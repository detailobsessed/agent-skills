# File management and document workflows

File handling is a core Mac experience. Prefer standard system flows over custom UI, and match the data model to how the user thinks about files.

## Start with the right model

- **Document-based architecture** when users primarily create, open, edit, save, duplicate, and compare files
- **App-managed storage** when documents are secondary and the app owns the data model (mail, RSS, IM, photo libraries)
- **Settings storage** only for preferences, not user content

If the user says "open" or "save" or thinks of their work as a discrete file in Finder, the workflow is document-shaped. If the user says "library" or "list" and thinks of items as living inside the app, it's app-managed.

## Preferred tools

### SwiftUI

- `DocumentGroup` — scene type for file-document apps
- `FileDocument` — value-typed documents with snapshot semantics (good for plain data)
- `ReferenceFileDocument` — class-typed documents when reference semantics are required
- `.fileImporter`, `.fileExporter`, `.fileMover` — system file panels in modal SwiftUI form
- `UTType` — uniform type identifiers for declared content types

### AppKit

- `NSDocument` and `NSDocumentController` — full document architecture with autosave, version browser, recents
- `NSOpenPanel`, `NSSavePanel` — system file panels with full delegate control
- `NSFilePromiseProvider` and `NSFilePromiseReceiver` — lazy file generation for drag-out scenarios (no SwiftUI equivalent)
- Quick Look integrations (`QLPreviewPanel`, `QLPreviewItem`) for custom file types

## Open, save, import, export

- Use system open/save panels instead of custom pickers — users expect Finder-shaped chooser UI
- Separate **import/export** from **open/save** when the user's mental model differs (export converts; save persists the working file)
- If the app works on user files, preserve their file names, types, and locations where possible
- If import is central, support file drag-and-drop alongside menu and toolbar entry points
- Multi-file workflows benefit from `NSOpenPanel.allowsMultipleSelection = true` and equivalent SwiftUI options

## Recent documents and multiwindow work

- Support multiple open documents or windows where comparison and parallel work are natural
- Preserve recent-document behavior automatically via `NSDocumentController` or `DocumentGroup`
- Let document frameworks handle autosave and version-oriented behavior when they fit the product
- For document tabs (`NSWindow.tabbingMode`), respect the system "Prefer Tabs" setting

## Finder-facing behavior

- Use meaningful file types declared via `UTType`
- Support Quick Look for custom formats when preview matters (`NSDocument.previewItemURL` or a Quick Look extension)
- Provide sensible icons, names, and exported metadata via Info.plist `UTExportedTypeDeclarations`
- Respect Finder conventions instead of inventing a parallel file browser unless the product truly needs one

## Sandboxed file access

- For external user-chosen files or folders, rely on system panels and security-scoped access — the panel grants the entitlement; you don't request paths arbitrarily
- Persist access with security-scoped bookmarks only when the workflow truly needs cross-launch access
- Always balance `startAccessingSecurityScopedResource()` with `stopAccessingSecurityScopedResource()` — leaks here cause subtle long-running bugs
- Bookmark resolution in a sandboxed app may return stale URLs; handle the resolution failure path

## Drag and drop for file workflows

- Accept dropped files via `.dropDestination(for: URL.self) { … }` (SwiftUI) or `NSDraggingDestination` (AppKit)
- For dragging files **out** to Finder with lazy generation, you need `NSFilePromiseProvider` — there is no SwiftUI equivalent. Bridge if drag-out-to-Finder is required
- For drag-source lifecycle (cancellation handling, drop-outside-window detection), bridge to `NSDraggingSource`. SwiftUI's `.draggable(_:)` has no session-end callback. See `menus-commands-input.md` for the full discussion

## Do not

- Store large user documents in `UserDefaults` — it's not the right tool, and large defaults slow login and sync
- Build custom fake "open" and "save" flows when Apple's panels fit
- Treat import/export as an afterthought in file-centric apps
- Assume sandboxed apps can read arbitrary paths without user consent or entitlements
- Use `Codable`+`UserDefaults` as a persistence layer for primary user data — that's what files or SwiftData are for

## Review checklist

- The app uses the correct document model for the workflow (document-based vs app-managed)
- Open/save/import/export are clearly separated and use system panels
- Drag-and-drop supports common file workflows; file promises bridge to AppKit when drag-out is required
- File access rules and sandbox implications are handled correctly, including bookmark balancing
- Custom file types are declared via `UTType` and previewable via Quick Look where it matters
- Recent documents and document tabs work the system way

## Pair this file with

- `menus-commands-input.md` for drag-and-drop, clipboard, and file-related commands plus drag-source lifecycle gaps
- `persistence-and-data.md` for choosing between file-based and database-backed storage
- `platform-capabilities-distribution.md` for sandboxing, entitlements, and security-scoped bookmarks
- `swiftui-macos.md` for SwiftUI file workflow APIs and known gaps
- `appkit-and-bridging.md` for `NSDocument`, `NSFilePromiseProvider`, and Quick Look integration
