# Platform capabilities and distribution

Mac-specific features often have UX, entitlement, and shipping implications at the same time. Address all three.

## Sandboxing

- Request the smallest entitlement set that satisfies the workflow
- Use user intent plus system panels for external file access
- Use security-scoped bookmarks only for persistent access that users expect
- Treat sandboxing as part of product design, not just release configuration

## Menu bar and background utilities

- Use `MenuBarExtra` for modern SwiftUI menu bar apps
- Use `NSStatusItem` when AppKit-level control is required
- Keep menu bar apps focused and lightweight
- If the app launches at login, use `SMAppService` and surface status clearly to the user

## Extensions and integrations

Reach for extensions or separate processes when the product truly needs them:

- Share extensions
- Finder Sync
- Quick Look preview or thumbnail support
- XPC services for isolation or separation of privilege

Do not add an extension target just to mirror functionality that belongs in the main app.

## Privacy and user trust

- Keep permission requests tightly connected to user intent
- Ensure Info.plist usage descriptions are clear and specific
- Explain why background behavior, file access, or device access exists when it may surprise the user

## Distribution

- **Mac App Store**: sandboxing and review requirements shape the implementation
- **Direct distribution**: plan for Developer ID signing, Hardened Runtime, and notarization as part of the product’s normal shipping path
- Be explicit about what differs between store and direct builds if the feature set changes

## Shipping checklist

- entitlements are minimal and justified
- background or login-item behavior is user-visible and reversible
- extension boundaries are appropriate
- privacy descriptions are accurate
- signing, notarization, and distribution paths are planned early enough to avoid late surprises
