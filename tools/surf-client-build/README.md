# SURF patched-client build

`surf-client-build.yml` produces a Zotero Desktop build whose **default** sync
preferences point at the SURF national server instead of zotero.org, so a fresh
profile syncs with the national server out of the box. This is the "patched
full build" instrument from `docs/national-hosting-proposal.md`
(`## Connecting Zotero clients → Distributing a pre-configured client`); the
recommended lighter instrument is the companion extension, which does not
require building Zotero at all.

## What the workflow does

1. Checks out `zotero/zotero` at the `zotero_ref` input (pinned release tag)
   with submodules and LFS, plus this repository for the patch script.
2. Runs `tools/surf-client-build/patch_prefs.py`, which injects the two
   preferences from `docs/clients.md` into `defaults/preferences/zotero.js`:
   - `extensions.zotero.api.url` = `<server_url>` (trailing slash added if missing)
   - `extensions.zotero.streaming.url` = `<server_url>` with the scheme mapped
     `https→wss` and path `/stream`, e.g. `wss://zotero.surf.nl/stream`
3. Builds the client JS (`npm install`, `npm run build`) and packages the
   Linux x64 app with Zotero's own build script (`app/build.sh -p l -a x64`),
   which fetches the pinned Gecko runtime (Firefox 140.15.0esr at tag 10.0.5).
4. Uploads `app/dist/Zotero-10.0.5.SOURCE_linux-x86_64.tar.xz` (name follows
   the ref) together with the patched prefs file, and prints sha256 sums to
   the run log.

At tag 10.0.5 the upstream defaults file contains **neither** preference: both
`syncRunner.js` and `streamer.js` fall back to `ZOTERO_CONFIG.API_URL` /
`ZOTERO_CONFIG.STREAMING_URL` from `resource/config.mjs`, and prefer a set
preference over those constants. The script inserts the prefs (marked with a
comment); if a future upstream tag defines them, the same script replaces the
existing lines instead. It fails the workflow if the result does not contain
each preference exactly once with the expected value.

## Pinned ground truth (verified 2026-10-10)

| Fact | Value |
|---|---|
| Repository / tag | [zotero/zotero](https://github.com/zotero/zotero) tag `10.0.5` (newest release tag at verification time; matches `tools/compatibility/desktop.toml`) |
| Default prefs file | `defaults/preferences/zotero.js` (merged into the app defaults by `app/build.sh` lines 371–410) |
| Fallback constants | `resource/config.mjs` (`ZOTERO_CONFIG.API_URL`, `ZOTERO_CONFIG.STREAMING_URL`) |
| Pref consumers | `chrome/content/zotero/xpcom/sync/syncRunner.js`, `chrome/content/zotero/xpcom/streamer.js` |
| Build entry point | `app/build.sh -p l -a x64` (staging under `app/staging/`, packages under `app/dist/`) |
| Runtime fetch | `app/scripts/fetch_xulrunner` (invoked by `app/build.sh` when `app/xulrunner/` is absent) |
| Node | 18 (matches Zotero's own `.github/workflows/ci.yml`) |

## How to dispatch

```sh
gh workflow run surf-client-build.yml \
  -f zotero_ref=10.0.5 \
  -f server_url=https://zotero.surf.nl/
gh run watch   # or: gh run list --workflow=surf-client-build.yml
```

The default `server_url` (`https://zotero.surf.nl/`) is a **pre-production
placeholder**. Point it at the real national server before distributing
anything.

## Expected cost

Roughly 20–40 minutes on `ubuntu-latest`: a few minutes for checkout,
`npm install` and the JS build, one xulrunner download (~300 MB, cached by
Zotero's scripts only inside the job), and packaging. Peak disk use is
well under 10 GB (repo + submodules + `node_modules` + Gecko runtime +
staging), within the standard runner's free space. The artifact tarball is
about 100–150 MB. These figures are estimates from the script sizes; the
first real run is the measurement.

## Why Linux only

The matrix deliberately contains only `ubuntu-latest` / Linux x64:

- **macOS** needs Apple Developer ID code signing and notarization
  (`xcrun notarytool` / `stapler`; Zotero's `app/config.sh` wires these in)
  plus `macos-15` runners. Unsigned or unnotarized mac apps are quarantined
  by Gatekeeper on every install.
- **Windows** needs an EV code-signing certificate and Signtool, plus the
  NSIS installer toolchain (`app/config.sh` expects `NSIS_DIR` on a Windows
  runner path).
- Zotero's build only packages natively per OS (`MAC_NATIVE` / `WIN_NATIVE`
  checks in `app/build.sh`), so these cannot be cross-built from Linux.
- A first release on Linux, where package managers and tarballs tolerate
  unsigned builds, proves the pipeline without buying any of that.

Signing infrastructure is explicitly out of scope here; add macOS/Windows
jobs only together with certificates, runners and notarization secrets.

## Verifying an artifact

1. **Hash**: compare `sha256sum` output from the run log ("Summarize
   artifacts" step) with the hash of your download.
2. **Version**: `tar tJf` the artifact name (`Zotero-10.0.5.SOURCE_linux-x86_64.tar.xz`);
   after unpacking, `Zotero_linux-x86_64/zotero --version` (or the
   Help → About dialog) reports `10.0.5.SOURCE`. The `.SOURCE` suffix marks
   a self-built binary and cannot collide with an official release.
3. **Prefs**: the artifact also contains the patched
   `defaults/preferences/zotero.js`; confirm the two injected lines. In a
   running client, check Settings → Advanced → Config Editor for
   `extensions.zotero.api.url` / `extensions.zotero.streaming.url`, then sync
   against a test account on the server.
4. **Leak check**: with `api.url` pointing at the server, confirm no connection
   is attempted to `stream.zotero.org` (e.g. in the Error Console network log)
   — this is the fallback leak documented in `docs/clients.md`.

## Update-channel caveat

This build is not official Zotero and must not masquerade as one: a renamed
build cannot consume Zotero's official update channel, and upstream update
URLs in the patched tree still point at zotero.org infrastructure unless
changed. SURF must run its own update channel (an `app.update.url` on its own
infrastructure and a rebuild on every upstream security release) **or**
distribute without updates and rely on institutional redeployment. Until that
channel exists, treat these artifacts as pilot-only and track Zotero security
advisories manually.

## Trademark caveat

Per `docs/national-hosting-proposal.md`, a redistributed build must be
labelled clearly so the Zotero name and trademarks are respected: the
distribution needs its own branding/description ("Zotero, configured for the
SURF national server"), must not imply endorsement by the Zotero project, and
should state that Zotero is a trademark of its respective holder. The
artifact name above keeps the upstream version with a `.SOURCE` suffix,
which identifies it as a self-built distribution rather than an official
release.

## Not verified locally

The full Zotero build was **not** run on the developer machine (the Gecko
runtime download and packaging are too heavy for it); the workflow steps and
the pref transformation are verified against the real `defaults/preferences/
zotero.js` at tag `10.0.5` (see below), and the build commands follow
Zotero's own CI (`.github/workflows/ci.yml`) and `app/build.sh` usage text.
The first real CI run is what proves end-to-end that `npm run build` output
is accepted by `app/build.sh`, that `fetch_xulrunner` succeeds on the runner,
and that the packaged client starts and honours the injected preferences.
