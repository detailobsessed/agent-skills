# File management and document workflows

File handling is a core Mac experience. Prefer standard system flows over custom UI.

## Start with the right model

- Use **document-based architecture** when users primarily create, open, edit, save, duplicate, and compare files
- Use **app-managed storage** when documents are secondary and the app owns the data model
- Use **settings storage** only for preferences, not user content

## Preferred tools

### SwiftUI

- `DocumentGroup`
- `FileDocument` or `ReferenceFileDocument`
- `.fileImporter`
- `.fileExporter`
- `.fileMover`
- `UTType`

### AppKit

- `NSDocument`
- `NSOpenPanel`
- `NSSavePanel`
- `NSFilePromiseProvider` where exported files are created lazily
- Quick Look integrations when custom file types need previews

## Open, save, import, export

- Use system open/save panels instead of custom pickers
- Separate **import/export** from **open/save** when the user’s model actually differs
- If the app works on user files, preserve their file names, types, and locations where possible
- If import is central, support file drag-and-drop as well as menu and toolbar entry points

## Recent documents and multiwindow work

- Support multiple open documents or windows where comparison and parallel work are natural
- Preserve recent-document behavior if you build on document frameworks
- Let document frameworks handle autosave and version-oriented behavior when they fit the product

## Finder-facing behavior

- Use meaningful file types and `UTType` declarations
- Support Quick Look for custom formats when preview matters
- Provide sensible icons, names, and exported metadata
- Respect Finder conventions instead of inventing a parallel file browser unless the product truly needs one

## Sandboxed file access

- For external user-chosen files or folders, rely on system panels and security-scoped access
- Persist access with security-scoped bookmarks only when the workflow truly needs cross-launch access
- Always balance `startAccessingSecurityScopedResource()` with `stopAccessingSecurityScopedResource()`

## Do not

- Store large user documents in `UserDefaults`
- Build custom fake “open” and “save” flows when Apple’s panels fit
- Treat import/export as an afterthought in file-centric apps
- Assume sandboxed apps can read arbitrary paths without user consent or entitlements

## Review checklist

- The app uses the correct document model for the workflow
- Open/save/import/export are clearly separated and use standard UI
- Drag-and-drop supports common file workflows
- File access rules and sandbox implications are handled correctly
- Custom file types are previewable and well-integrated where appropriate
