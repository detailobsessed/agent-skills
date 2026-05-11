# Platform capabilities and distribution

Mac-specific features often have UX, entitlement, and shipping implications at the same time. Address all three together — entitlements drive what the app can do, sandbox configuration drives what it can read and write, and distribution channel drives both.

## Sandboxing

- Request the smallest entitlement set that satisfies the workflow
- Use user intent plus system panels (`NSOpenPanel`, `.fileImporter`) for external file access — the panel grants the entitlement, you don't claim arbitrary paths
- Use security-scoped bookmarks only for persistent access that users expect to survive launches
- Treat sandboxing as part of product design, not just release configuration — workflows that require home-folder traversal need different UX than workflows that operate on a chosen file
- Always balance `startAccessingSecurityScopedResource()` with `stopAccessingSecurityScopedResource()`; leaks here cause subtle long-running issues
- Mac App Store distribution **requires** sandboxing; Developer ID distribution does not, but Hardened Runtime is required regardless for notarization

## Common entitlements

- `com.apple.security.app-sandbox` — sandbox itself
- `com.apple.security.files.user-selected.read-only` / `.read-write` — granted by file panels
- `com.apple.security.files.bookmarks.app-scope` — security-scoped bookmark resolution
- `com.apple.security.network.client` / `.server` — outgoing / incoming network
- `com.apple.security.device.audio-input` / `.camera` — capture entitlements (also need usage descriptions in Info.plist)
- `com.apple.security.application-groups` — App Group container access
- `com.apple.security.cs.allow-jit` and friends — JIT and code-signing relaxations (rare; document the reason)

Verify exact entitlement keys against current Apple documentation; the list evolves, and the wrong key produces silent failures rather than build errors.

## Menu bar and background utilities

- Use `MenuBarExtra` for modern SwiftUI menu bar apps (macOS 13.0+)
- Use `NSStatusItem` when you need AppKit-level control: custom views, manual click-handling, modifier-aware menus
- Pair menu-bar-only apps with `LSUIElement = true` in Info.plist to suppress Dock and app switcher presence
- Keep menu bar apps focused and lightweight — users will remove the icon if it's busy or buggy
- If the app launches at login, use `SMAppService` (macOS 13+) — the modern replacement for `SMLoginItemSetEnabled`. Surface launch-at-login state clearly to the user with a settings toggle

## Extensions and integrations

Reach for extensions or separate processes when the product truly needs them:

- **Share extensions** — for "share to your app" from other apps
- **Action extensions** — for service-style transformations
- **Finder Sync extensions** — for cloud-storage badge overlays and Finder context menu items
- **Quick Look preview / thumbnail extensions** — for custom file types
- **XPC services** — for isolation, separation of privilege, or running long-lived work outside the main process
- **Network extensions** — VPN, content filters, DNS proxies; require special entitlements

Don't add an extension target just to mirror functionality that belongs in the main app. Extension overhead (separate bundle, separate signing, separate sandbox) only pays off when the extension reaches a context the main app can't.

## Privacy and user trust

- Permission requests should be tightly connected to user intent — request the camera when the user clicks "Start camera", not at launch
- Info.plist usage descriptions (`NSCameraUsageDescription`, `NSMicrophoneUsageDescription`, `NSDesktopFolderUsageDescription`, etc.) must be specific and honest — Apple may reject vague descriptions
- Explain why background behavior, file access, or device access exists when it may surprise the user
- Telemetry and crash reporting need explicit user-visible disclosure on macOS

## Distribution

- **Mac App Store** — sandboxing is mandatory, review process applies, in-app purchase via StoreKit
- **Developer ID (direct distribution)** — Hardened Runtime required for notarization, signing with a Developer ID Application certificate, notarization via `notarytool`, stapling the ticket onto the artifact
- **Hybrid** — many apps ship both. Plan for entitlement and feature differences explicitly; some entitlements (like network extensions) require approvals that differ between channels

## Code signing and notarization workflow

- Signing identity: Developer ID Application certificate for direct distribution; Apple Distribution for the App Store
- Hardened Runtime is required for notarization; enable it in build settings
- Use `notarytool submit … --wait` (the modern tool; `altool` is deprecated)
- Staple after notarization with `xcrun stapler staple <artifact>`
- Verify with `spctl --assess --verbose <artifact>` before shipping
- Plan signing and notarization into CI early — late surprises here block releases

## Universal binaries

- Build for `arm64` and `x86_64` if you support Macs older than Apple Silicon-only deployment
- If you depend on Intel-only or arm64-only third-party binaries, verify both arches at link time
- Test under Rosetta 2 only if you actually ship to Intel-equipped users

## Shipping checklist

- Entitlements are minimal and justified; each one is needed by a real workflow
- Sandbox-required workflows have user-intent-driven panel UX, not magic path access
- Background or login-item behavior is user-visible and reversible
- Extension boundaries are appropriate; no "extension because we wanted a target" anti-pattern
- Privacy descriptions are accurate and specific
- Signing, notarization, and distribution paths are wired into CI early
- Universal binary status is correct for the deployment plan
- Hybrid distribution differences (App Store vs Developer ID) are documented if the feature set differs

## Pair this file with

- `file-management-documents.md` for sandboxed file access and security-scoped bookmarks
- `persistence-and-data.md` for App Group containers and shared storage
- `swiftui-macos.md` for `MenuBarExtra` and SwiftUI scene types
- `appkit-and-bridging.md` for `NSStatusItem` and `NSApplicationDelegate` plumbing
- `official-sources.md` for verifying entitlements, Info.plist keys, and distribution requirements
