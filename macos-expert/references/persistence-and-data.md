# Persistence and data choices

Choose storage by the user’s mental model and the app’s data shape, not by habit.

## Pick the right storage model

- **User preferences** → `UserDefaults` / `@AppStorage`
- **User-owned documents** → file-based documents with `DocumentGroup`, `FileDocument`, `ReferenceFileDocument`, or `NSDocument`
- **Relational app data for modern targets** → SwiftData
- **Legacy or advanced persistence needs** → Core Data
- **Shared app/extension data** → App Group container plus the appropriate store type

## SwiftData guidance

- Use SwiftData for modern macOS targets when the app owns structured relational data
- Use `@Query` in simple SwiftUI views
- Use `FetchDescriptor`, `fetchCount`, and background workers for service-layer or high-volume operations
- Use `@ModelActor` / `ModelActor` for background writes and bulk work
- Set fetch limits for bounded UI
- Plan migrations for schema changes instead of assuming they are free

## File-based documents

If the user thinks in files, make the data model file-shaped:

- opening and saving should operate on real files
- import/export should be explicit when conversion is involved
- document windows should reflect document lifecycle and state

Do not force a database-shaped UX onto a document-shaped product.

## Preferences and lightweight settings

- Keep `UserDefaults` for preferences, flags, window choices, and small settings
- Do not put large blobs, primary records, or user documents in `UserDefaults`

## Data integrity rules

- Keep persistence APIs off the main thread for heavy work
- Distinguish read models from write paths where complexity demands it
- Treat migrations, uniqueness, and deletion rules as product behavior, not just schema details
- Test realistic data volume, not only toy datasets

## Review checklist

- Storage choice matches the user’s mental model
- SwiftData is used where it helps, not as a reflex
- File/document workflows are file-native when appropriate
- Preferences are separated from user content
- Background work, fetch size, and migration risks are considered
