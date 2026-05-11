# Persistence and data choices

Choose storage by the user's mental model and the app's data shape, not by habit. The wrong choice is hard to undo because it leaks into the UI, the sync model, and the migration plan.

## Pick the right storage model

- **User preferences** → `UserDefaults` / `@AppStorage`
- **Per-window or per-scene state restoration** → `@SceneStorage` (don't put this in `UserDefaults`)
- **User-owned documents** → file-based documents with `DocumentGroup`, `FileDocument`, `ReferenceFileDocument`, or `NSDocument`
- **Relational app data for modern targets** → SwiftData
- **Legacy or advanced persistence needs** → Core Data
- **Shared app/extension data** → App Group container plus the appropriate store type
- **Cross-device sync of app data** → CloudKit (directly, or via SwiftData/Core Data CloudKit integration) — see `platform-capabilities-distribution.md`

## SwiftData guidance

- Use SwiftData for modern macOS targets when the app owns structured relational data — but check current Apple docs for known issues on the macOS version you're targeting; SwiftData on Mac has had real friction in recent releases
- Use `@Query` in simple SwiftUI views with bounded result sets
- Use `FetchDescriptor`, `fetchCount`, and background workers for service-layer or high-volume operations
- Use `@ModelActor` / `ModelActor` for background writes and bulk work — don't do bulk inserts on the main `ModelContext`
- Set fetch limits for bounded UI; don't `@Query` an unbounded table into a list
- Plan migrations for schema changes; lightweight migration is not free, and unique-constraint changes can require a custom migration plan
- Test with realistic data volume before assuming SwiftData performance will hold

If you're hitting performance walls, lifecycle weirdness, or migration complexity that SwiftData doesn't expose, Core Data is still a valid call. Don't migrate from working Core Data to SwiftData just for fashion.

## Core Data guidance

- Still the right tool for: complex relationships with custom fetched properties, fine-grained NSManagedObject subclass behavior, mature CloudKit sync (`NSPersistentCloudKitContainer`), or large-scale apps already invested in it
- Use `NSPersistentContainer` and per-context concurrency types (`mainContext` vs `newBackgroundContext`)
- Save merge policies explicitly; default policy on conflict can silently drop changes
- Use `NSFetchedResultsController` for AppKit-bound UI, or `@FetchRequest` / `@SectionedFetchRequest` in SwiftUI views, when the UI must reflect store changes live and you're not on SwiftData

## File-based documents

If the user thinks in files, make the data model file-shaped:

- Opening and saving operate on real files
- Import/export are explicit when format conversion is involved
- Document windows reflect document lifecycle and state (modified indicator, tab grouping, version browser)
- Use `FileDocument` for simple value semantics, `ReferenceFileDocument` when you need class semantics or undo grouping
- For complex document apps with versioning, autosave, and tabs, `NSDocument` is still the most complete tool

Do not force a database-shaped UX onto a document-shaped product, and vice versa.

## Preferences and lightweight settings

- `UserDefaults` for preferences, flags, window choices, and small structured settings
- `@AppStorage` is the SwiftUI bridge — fine for primitives and small `Codable` values
- Don't put large blobs, primary records, or user documents in `UserDefaults`
- Don't put security-sensitive values in `UserDefaults` — Keychain (`kSecClass…`) is the right tool

## Window-scoped state

- `@SceneStorage` for per-scene restoration (sidebar visibility, selection, scroll position)
- AppKit equivalents: `NSWindow.restorationClass` and the `NSResponder` `encodeRestorableState`/`restoreState` plumbing
- Don't conflate per-scene UI state with app-global preferences

## Data integrity rules

- Keep heavy persistence work off the main thread
- Distinguish read models from write paths where complexity demands it
- Treat migrations, uniqueness constraints, and deletion rules as product behavior, not just schema details
- Test realistic data volume, not only toy datasets — performance regressions show up at the 10k–100k record threshold for most stores
- For CloudKit-backed stores, plan for conflict resolution explicitly; "last writer wins" is rarely what users expect

## Review checklist

- Storage choice matches the user's mental model
- SwiftData is used where it helps, not as a reflex; Core Data is a valid choice when SwiftData doesn't fit
- File / document workflows are file-native when the user thinks in files
- Preferences are separated from user content; sensitive values are in Keychain
- Per-scene state uses `@SceneStorage` or AppKit restoration, not `UserDefaults`
- Background work, fetch size, and migration risks are considered before shipping
- Cross-device sync (if any) has explicit conflict and offline behavior

## Pair this file with

- `file-management-documents.md` for document-based app workflows and file storage
- `swiftui-macos.md` for SwiftUI data flow, observation, and `@SceneStorage` patterns
- `platform-capabilities-distribution.md` for App Groups, sandboxing, shared containers, and CloudKit
- `official-sources.md` for verifying SwiftData and CloudKit availability and behavior on the macOS version you target
