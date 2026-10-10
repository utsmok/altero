// "Zotero from SURF" companion plugin (docs/national-hosting-proposal.md,
// companion-extension option): points an unmodified Zotero Desktop at a
// SURF-managed altero server by setting the two client preferences
// documented in docs/clients.md. Bootstrap plugin (manifest_version 2),
// modelled on tools/compatibility/desktop_bootstrap.js, which the
// compatibility harness installs in every real test profile.

var serverPref = "extensions.surfsync.serverUrl";
var enabledPref = "extensions.surfsync.enabled";
var capturedPref = "extensions.surfsync.captured";
var apiPref = "extensions.zotero.api.url";
var streamingPref = "extensions.zotero.streaming.url";

// Pre-production placeholder until SURF names the real national host; see
// README.md. Change it per institution via extensions.surfsync.serverUrl.
var defaultServer = "https://zotero.surf.nl/";

function install() {}

function uninstall() {
  // Restore what the client had before the plugin first ran, so removal
  // returns it to stock behavior (the proposal's documented exit path).
  var raw = Services.prefs.getStringPref(capturedPref, "");
  if (!raw) return;
  Services.prefs.clearUserPref(capturedPref);
  var captured;
  try {
    captured = JSON.parse(raw);
  } catch (error) {
    return; // corrupt snapshot: nothing safe to restore
  }
  setOrClear(apiPref, captured.apiUrl);
  setOrClear(streamingPref, captured.streamingUrl);
}

function shutdown() {}

function startup() {
  if (!Services.prefs.getBoolPref(enabledPref, true)) {
    return; // disabled: never touch Zotero's own preferences
  }
  if (!Services.prefs.getStringPref(capturedPref, "")) {
    // Capture once, on the plugin's first run, before overwriting anything,
    // so a later uninstall restores the pre-plugin values rather than ours.
    Services.prefs.setStringPref(
      capturedPref,
      JSON.stringify({
        apiUrl: prefValue(apiPref),
        streamingUrl: prefValue(streamingPref),
      })
    );
  }
  // Re-assert on every startup, so client updates (or manual edits) cannot
  // drift the client back to zotero.org.
  var urls;
  try {
    urls = deriveUrls(Services.prefs.getStringPref(serverPref, defaultServer));
  } catch (error) {
    Zotero.logError(error);
    return;
  }
  if (!urls) {
    Zotero.logError(
      new Error(
        "surfsync: server URL must use http or https, got " +
          Services.prefs.getStringPref(serverPref, defaultServer)
      )
    );
    return;
  }
  Services.prefs.setStringPref(apiPref, urls.api);
  Services.prefs.setStringPref(streamingPref, urls.streaming);
}

function deriveUrls(server) {
  var url = new URL(server);
  var secure = url.protocol === "https:";
  if (!secure && url.protocol !== "http:") return null;
  var base = url.pathname.replace(/\/+$/, "");
  return {
    api: url.protocol + "//" + url.host + base + "/",
    streaming: (secure ? "wss://" : "ws://") + url.host + base + "/stream",
  };
}

function prefValue(pref) {
  return Services.prefs.prefHasUserValue(pref)
    ? Services.prefs.getStringPref(pref)
    : null;
}

function setOrClear(pref, value) {
  if (value === null || value === undefined) Services.prefs.clearUserPref(pref);
  else Services.prefs.setStringPref(pref, value);
}
