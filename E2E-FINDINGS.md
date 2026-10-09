# End-to-end findings: Zotero Desktop 10.0.6 against altero

Notes from a full prototype run (2026-10-09): altero was deployed from a
source checkout, exercised with protocol-level API probes, and then synced
with a real Zotero Desktop client under Xvfb. This file records what was
verified, the client redirect mechanics that make self-hosting work, and the
testing gotchas that cost time.

For the manual two-client test procedure, see
[testing-two-clients](docs/testing-two-clients.md).

## What was verified

| Surface | Result | Evidence |
|---|---|---|
| Downloads (server → client) | Works | Items, collections, and group items landed in a fresh client library |
| Item uploads (client → server) | Works | A book and a child attachment created in the client appeared server-side with correct versions |
| Attachment file upload | Works | `GET /users/1/items/{key}/file` returned a ZIP whose payload was byte-identical to the source file |
| Streaming notifications | Works | The client held a WebSocket to `ws://…/stream` and received keepalives |
| Suite | 242 tests pass | `uv run pytest` |

## Client redirect mechanics

No client rebuild is needed. Zotero Desktop reads two hidden preferences:

```text
extensions.zotero.api.url       http://127.0.0.1:8085/
extensions.zotero.streaming.url ws://127.0.0.1:8085/stream
```

In Zotero 10 the redirect is one getter
(`syncRunner.js:50`):
`options.baseURL || Zotero.Prefs.get('api.url') || ZOTERO_CONFIG.API_URL`.
Everything the sync runner does goes through it.

Two consequences worth knowing when developing altero:

- Plain HTTP works; TLS is not required by the client, only by exposure.
- Imported attachments upload as ZIP archives. The stored md5 is the
  archive's md5, not the raw file's — do not "fix" that mismatch in tests.

## API keys in a test rig

The desktop keyring is awkward headless (GNOME Keyring missing → modal
alerts). Two bypasses, both in-memory only:

```javascript
Zotero.Sync.Runner.backgroundSync = true;      // suppress keyring dialogs
Zotero.Sync.Runner.apiKey = '<key>';           // bypass login manager
```

Mint the key from the CLI instead of the client: `altero key add --groups
<username>`. A key without group scope cannot see group libraries; a
user-library upload needs a user-scoped key.

## Testing gotchas (each cost real time)

1. **Zotero is single-instance per profile and forwards CLI args.** A zombie
   `zotero-bin` owning port 23119 silently captures every later launch, and
   the eval/console session then talks to an instance with different prefs
   (symptom: requests to `https://api.zotero.org/keys/current` → 403 →
   "API key not set"). Always verify `pgrep -af zotero-bin` is empty before
   relaunching, and confirm identity in-console:
   `Zotero.Prefs.get('api.url')` plus the item count.
2. **`Attachments.importFromFile` with an invalid file** (e.g. a truncated
   fake PDF) leaves an attachment row with no file in
   `data/storage/<KEY>/`. The sync's upload phase then dies with
   `NS_ERROR_FAILURE [nsIAsyncStreamCopier2.init]` — a null file stream.
   Seed attachments with real files; any text file works.
3. **Browser Console automation**: `Escape` clears the console input, so
   scripted `Escape`-then-`Return` eats evals. Type with
   `xdotool type --delay 25 --file` and press plain Return. File writes from
   evals (`Zotero.File.putContentsAsync`) are the reliable result channel.
4. **`Zotero.Debug.get()` is async** in Zotero 10, and the debug store resets
   on every launch: call `Debug.setStore(true)` in the session under test,
   then dump the buffer before it exits.

## Known gaps observed

- Mobile apps and Overleaf hardcode zotero.org and cannot be redirected;
  desktop clients are the only full participant.
- Legacy `POST /keys`, `DELETE /removestoragefiles`, and
  `/retractions/list` are unimplemented; desktop sync did not need them.

## Reproducing the run

A helper lives at `tools/dev-e2e.sh`: it boots a scratch server, provisions
a user and keys, and can launch the lab client against it. The client used
was Zotero 10.0.6 Linux x64 with the two prefs above set in its profile.
