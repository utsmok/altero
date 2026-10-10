# SURF Sync for Zotero

Companion Zotero plugin for the SURF-managed national sync server described in
[the national hosting proposal](../national-hosting-proposal.md) ("companion
extension" option). Installing it points an unmodified Zotero Desktop at the
SURF server instead of zotero.org; uninstalling it returns the client to stock
behavior.

## What it sets

On every startup it derives both client preferences from one server URL:

```text
extensions.zotero.api.url       = https://zotero.surf.nl/
extensions.zotero.streaming.url = wss://zotero.surf.nl/stream
```

- The trailing slash on `api.url` is mandatory (`docs/clients.md`); the plugin
  enforces it, whatever the configured server URL says.
- Streaming uses `wss://` behind TLS and `ws://` behind plain http, with
  `/stream` appended to the server's host and any base path.

Both preferences are needed because `api.url` does not redirect the streaming
connection. Per `docs/clients.md`:

> If `extensions.zotero.streaming.url` is left unchanged, Zotero falls back to
> its built-in `wss://stream.zotero.org` endpoint and may send the altero API
> key there. zotero.org rejects that key, but the key may appear in upstream
> logs.

Setting the API endpoint without also pointing streaming at the same server
would leak the user's API key to zotero.org's infrastructure.

## Configuration

The plugin owns its own preferences, settable in the Config Editor:

| Preference | Default | Meaning |
|---|---|---|
| `extensions.surfsync.serverUrl` | `https://zotero.surf.nl/` | Server to point the client at |
| `extensions.surfsync.enabled` | `true` | When `false`, the plugin never touches Zotero's preferences |
| `extensions.surfsync.captured` | — | Snapshot of the pre-plugin preference values, written on first run (internal) |

> **Warning:** `https://zotero.surf.nl/` is a **pre-production placeholder**.
> No national SURF host exists yet. Institutions must set
> `extensions.surfsync.serverUrl` to their real server before rollout.

Changing the server URL takes effect at the next Zotero startup; the plugin
re-asserts both preferences on every launch, which is what makes the setup
survive official Zotero client updates.

## Install

1. Build the XPI: `./build.sh` → `surf-sync.xpi` (requires Python 3; `zip(1)`
   is not needed).
2. In Zotero: Tools → Plugins → gear menu → *Install Plugin From File*, then
   pick `surf-sync.xpi`, and restart Zotero when prompted.
3. Institutional IT can instead drop the XPI into the profile's `extensions/`
   directory as `surf-sync@altero.invalid.xpi` (the compatibility harness
   installs it that way for acceptance runs).

## Uninstall

Remove the plugin through Tools → Plugins. On uninstall the plugin restores the
`api.url` and `streaming.url` values it captured the first time it ran, so the
client goes back to exactly the pre-plugin state (including "unset", i.e.
Zotero's own defaults, for a fresh profile). After that, restart Zotero.

## Compatibility

- Target baseline: Zotero Desktop **10.0.5**, the version pinned in
  `tools/compatibility/desktop.toml`.
- `manifest.json` uses `manifest_version: 2` with an `applications.zotero`
  block and strict bounds `strict_min_version: 10.0.5` …
  `strict_max_version: 10.*`, mirroring the field conventions of the
  harness's acceptance plugin (`tools/compatibility/desktop.py`). Zotero
  10 rejects manifests that omit `applications.zotero.update_url`, so the
  plugin declares one (`https://zotero.surf.nl/surf-sync-updates.json`,
  a placeholder alongside the server URL); keep update checks off in
  managed deployments (`extensions.update.enabled = false`) until a real
  update feed exists.
- Plugin ID: `surf-sync@altero.invalid`. The `.invalid` TLD is reserved
  (RFC 2606) and matches the harness plugin's convention
  (`acceptance@altero.invalid`); swap it for an SURF-owned identifier before
  any production distribution.
- No update URL is shipped: distribution goes through SURF/institutional
  channels, not an add-on update feed. The plugin is unsigned, like the
  harness XPI; Zotero does not enforce signatures.
