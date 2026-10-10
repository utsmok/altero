# SURFconext SSO for a national altero deployment

Research question: can altero, hosted by SURF for all Dutch universities and
hogescholen, let users sign in through their own institution via SURF's SSO
service (SURFconext)?

**Verdict: yes, with no new protocol code.** altero already implements
everything SURF requires of a service provider — an OpenID Connect relying
party doing authorization code with PKCE as a confidential client — and the
Zotero desktop client's login handshake is browser-based, so institutional
single sign-on slots in at the browser step. The work is one provider row of
configuration plus SURF's registration procedure.

## 1. What SURF offers

SURFconext is a hub (an OpenID Provider in OIDC terms): it never authenticates
anyone itself, but proxies to the institutional IdP of whoever is signing in.
One registration makes the service available to every connected institution,
which is all Dutch universities and hogescholen; a per-institution whitelist
can narrow that. Key facts from the SURF documentation:

- OIDC is the recommended protocol (SAML also works). Discovery:
  `https://connect.surfconext.nl/.well-known/openid-configuration`;
  independent test environment at `connect.test.surfconext.nl` with a
  playground and test IdPs. Registration and testing are self-service.
- SURF enforces a data-minimisation policy: claims must be motivated and are
  reviewed before production.
- `sub` is persistent and specific to the relying party (generated from the
  user's uid, `schacHomeOrganization`, and the client id). SURF warns it
  changes if the client id or those source claims change — keep the client id
  stable for the life of the service.
- eduID is available as a connected IdP for guests and alumni.
- OIDC is not yet available via eduGAIN interfederation; for a Dutch-only
  service that is irrelevant.

Sources: [OpenID Connect reference](https://servicedesk.surf.nl/wiki/spaces/IAM/pages/128909841/),
[OIDC claims](https://servicedesk.surf.nl/wiki/spaces/IAM/pages/128910043/),
[Connect in 5 Steps](https://servicedesk.surf.nl/wiki/spaces/IAM/pages/128910038/),
[Configure OIDC entities](https://servicedesk.surf.nl/wiki/spaces/IAM/pages/128910155/).

## 2. Why SSO fits the desktop client

The Zotero client (verified against `zotero/zotero@main`) links an account like
this — `preferences_account.jsx::linkAccount`, `syncAPIClient.js`:

1. `POST {server}/keys/sessions` → `{sessionToken, loginURL}`; the client
   opens `loginURL` in the system browser and polls
   `GET {server}/keys/sessions/{token}` (DELETE to cancel). Every URL is
   relative to the configured server base URL, so it works against altero.
2. altero (`src/altero/api/routes/keys.py:85-133`) points `loginURL` at its SPA
   approval page `/app/link?token=…`.
3. The user signs in to the web app — password, passkey, or an institution via
   SURFconext — and approves the link.
4. altero mints an API key and attaches it to the session; the client's next
   poll returns it. No password ever reaches altero, and sync requests carry
   only the API key, exactly as today.

Sign-in is federated by `GET /web/auth/sso/{slug}/start` and `/callback`
(`src/altero/api/routes/webidentity.py:168-305`): an `AuthRequest` row is the
state, the callback exchanges the code with PKCE and verifies issuer, audience,
nonce, and expiry (`src/altero/services/oidc.py`), and
`src/altero/services/federation.py` turns the assertion into a session.

## 3. Configuration: the provider row

`IdentityProvider` (`src/altero/models/identity.py:31-103`) is created through
the admin screen or `POST /web/admin/providers`. For SURFconext:

| Field | Value | Why |
|---|---|---|
| `slug` | `surfconext` | Appears in the callback URL. |
| `kind` | `oidc` | |
| `issuer` | `https://connect.surfconext.nl` | Discovery endpoints are fetched and cached automatically. |
| `client_id` / `client_secret` | from the SP Dashboard | Confidential client; the secret is write-only. |
| `scopes` | `openid profile email` | Keep minimal; SURF reviews. |
| `username_claim` | `eduperson_principal_name` | Must be a single string (`_text`, oidc.py:224-232). SURF's `uids` is a list and would fall back to `sub`; `preferred_username` on SURF is a display name like "Prof.dr. Jane Doe". |
| `name_claim` / `email_claim` | `name` / `email` | Email release must be motivated; if withheld, accounts simply have no address. |
| `create_accounts` | `true` | Just-in-time accounts for anyone at any connected institution (`_provision` goes through `admin.create_user`, so IDs and libraries are normal; asserted email is stored unconfirmed). |
| `required_claim` / `required_value` | empty, or `schac_home_organization` = a domain | Empty admits every institution; set it to gate per institution. `eduperson_scoped_affiliation` also works — the check is list-aware (oidc.py:248-265). |
| `revoke_keys_on_loss` | `false` | Deprovisioning already suspends the account, refusing both the API key and browser sessions while keeping data and reinstatement cheap (`_deprovision`). |

Identity is the SURF `sub` alone (`FederatedIdentity.subject`, unique per
provider); email is never an identity. Losing the required claim suspends on
the next sign-in.

## 4. SURF registration (their five steps)

1. Contact SURF for an introduction meeting; contract requirements depend on
   the customer — for a SURF-hosted service this is largely SURF-internal, but
   confirm.
2. In the SP Dashboard (`sp.surfconext.nl`) add an **OpenID Connect client**
   entity on the test environment; set the redirect URI
   `https://<public host>/web/auth/sso/surfconext/callback` (the admin screen
   shows exactly this value), motivate the requested claims, publish, and test
   against `connect.test.surfconext.nl` — the whole desktop flow can be
   exercised before any production commitment.
3. Settle the contract and fill in the GDPR/AVG questions in the dashboard.
4. Promote to production: technical checks, **SSL Labs A rating required**,
   functional contact addresses, and contacts at the institutions to connect.
5. SURF connects each requested institution; data processing is limited to
   name, email, username — consistent with minimisation.

## 5. Deployment notes

- `ALTERO_PUBLIC_URL` must be set on the public HTTPS host; the callback and
  ACS URLs are built from it and must match the SP Dashboard registration
  byte-for-byte (`redirect_uri`, webidentity.py:95-109).
- Zotero clients point at the server via `extensions.zotero.api.url` and
  `extensions.zotero.streaming.url` (use `wss://` behind TLS); see
  `E2E-FINDINGS.md` for the verified client setup.
- Only the desktop client is verified against custom servers; Zotero's mobile
  clients are unverified and out of scope here.

## 6. Gaps and open questions

- Provisioned usernames are cosmetic: `jan.doe@uni.nl` becomes `jan.doeuni.nl`
  (`_unique_username` strips `@`); the subject, not the name, is the identity.
  A one-line patch could keep the address verbatim if wanted.
- A SURF-side change to the client id, uid, or `schacHomeOrganization`
  regenerates `sub` for everyone and unlinks accounts; SURF notifies RPs. Keep
  the client id immutable.
- Costs and contract shape for national hosting are not published; ask SURF.
- Per-institution policy differences (e.g. staff-only libraries) would need
  affiliation-based rules, which the single `required_claim` field does not
  express — fine for a national open-to-all service, a design question if not.
