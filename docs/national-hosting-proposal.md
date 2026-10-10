# Proposal: a SURF-managed national Zotero server for Dutch higher education

Samuel Mok, information specialist, Universiteit Twente
([s.mok@utwente.nl](mailto:s.mok@utwente.nl)), October 10, 2026.

Draft proposal for SURF, universities and hogescholen. This document is
fork-local research material and is not part of the altero documentation set.
The technical SSO analysis it builds on is in [sso-surf.md](sso-surf.md).

## Summary

The proposal is that SURF operates one shared altero server for all Dutch
universities and hogescholen. Users keep the Zotero Desktop application they
already use, sign in through their own institution via SURFconext, and keep
their library data on Dutch infrastructure. altero is free software under the
AGPL-3.0 license, so there are no license fees. The realistic costs are one
small server environment and 0.1 to 0.4 FTE of staff time, depending on scale,
and a few terabytes of attachment storage even at national size.
A pilot with one or two institutions can start after a short technical
preparation, and the SURFconext connection is configuration work because
altero already implements it.

## What is proposed

A sync server is the service that copies a reference library between a
researcher's devices and their group's shared library. Zotero is a widely used,
free, open source reference manager. Its desktop application is open source and
runs on Windows, macOS and Linux. By default it synchronizes with a service
at zotero.org in the United States.

altero is an open source server that implements the same synchronization protocol.
An unmodified Zotero Desktop application synchronizes with it, including
attachments, notes, annotations, full-text search and group libraries. One
server can serve all institutions, because users sign in through SURFconext and
altero already supports that sign-in method.

## The case for and against

### The case for

- **Privacy and the GDPR.** Library data, including PDFs and notes, stays on
  infrastructure in the Netherlands under EU law. Sign-in releases the minimum
  set of attributes, the server does no profiling, and the administrator role
  is designed so that operating the service does not mean reading everyone's
  library.
- **Autonomy.** Institutions stop depending on one American service's storage
  quotas, pricing and terms. A group library no longer draws on the personal
  quota of whichever member owns the group.
- **The market is churning anyway.** The Dutch university RefWorks licensees
  below have all left the product. Institutional Mendeley licenses ended
  at several universities in 2024, and Twente has dropped two reference
  managers in two years. Twente's EndNote agreement ended in December 2025.
  Every one
  of those migrations is already being paid for. This proposal changes
  where they land, not whether they happen.
- **Open source.** The server is AGPL-3.0, the client is open source, and
  export is a core feature, so users and institutions are never locked
  in. Institutions can fix or extend the software instead of requesting
  features from a vendor.
- **Cost.** There are no per-seat licenses. The cost is a fraction of one FTE
  of staff time and one small server environment, with infrastructure between
  10,000 and 20,000 euro per year at national scale.
- **Continuity.** The desktop application keeps a complete local copy of every
  library, so users are protected even if the service stops. The service can
  be moved between infrastructures because both the client and the server are
  open source.

### The devil's advocate case

The list below gives the honest arguments against, with a response where one
exists. Where no response exists, the argument is left standing.

1. **zotero.org already does this job.** It is free below 300 MB and run by
   a nonprofit, and its unlimited institution subscription is affordable.
   Twente's costs about 5,000 euro per year. If an institution
   does not care where its data lives or who can suspend accounts, zotero.org
   is the cheaper and less risky choice, and this proposal duplicates it.
   *Response:* the argument rests on residency, group libraries with files,
   sign-in integration and account lifecycle; institutions indifferent to all
   four should indeed stay where they are.
2. **The configuration surface is unsupported.** The Zotero project does not
   support third-party sync servers. The two preferences that redirect a
   desktop client work today, but they are not a documented integration
   surface. A desktop release could change their behavior. The streaming
   preference has a real trap. If it is not set, the client keeps talking to
   zotero.org's streaming endpoint and may send the altero API key there.
   *Response:* the compatibility matrix pins desktop releases and runs
   acceptance scenarios with real client profiles before any deployment.
   The client package SURF distributes, described below, would set both
   preferences so the trap never fires, reducing the risk to small. The
   risk does not reach zero, and the remaining risk is the strongest
   technical argument against the project.
3. **Official mobile apps cannot connect at all.** The iOS and Android
   applications compile the zotero.org hosts into the binary and have no
   setting for another server, so connecting them means patched builds that
   nobody official publishes. Until such builds exist, mobile users are
   second-class on the national server. *The objection stands today.*
4. **Key-person and project risk.** altero is a young project at release
   1.0.0-beta.2 with a small team, and a national service would make it
   critical infrastructure. *Response:* the AGPL license means SURF can
   take over the code without permission, and operating it is estimated at a
   fraction of one FTE, but the governance question is real and is SURF's to
   answer, not the software's.
5. **Migration is not free.** A desktop profile that has synced with
   zotero.org carries its old numeric account id, and the server refuses to
   hand it a key for a different account. An account with that id must be
   created on the server, and attachments move off institutional WebDAV only
   through a deliberate full re-upload step. Users who keep
   both a zotero.org account and a new one risk split libraries. *Response:*
   tooling and a documented procedure exist, and onboarding happens
   institution by institution, not all at once.
6. **Nothing has run at national scale.** The desktop evidence covers
   594 acceptance phases across 47 scenario and database combinations, on
   pilot-sized libraries. No load test
   has exercised 25,000 or 100,000 concurrent users, and the sizing in this
   document is arithmetic, not measurement. *Response:* the pilot phase
   exists to replace arithmetic with evidence before any national
   commitment.
7. **Governance is the hard part.** A sector service needs retention policy,
   an uptime commitment, incident response and multi-year funding. Those
   decisions, not the software, determine whether this service earns trust,
   and open source does not write policy. *The objection stands, and it is
   the part SURF actually signs up for.*

### How the alternatives compare

| | zotero.org free | zotero.org paid | EndNote | Mendeley | Shared altero server |
|---|---|---|---|---|---|
| Software | Open source client | Open source client | Commercial | Closed, owned by Elsevier | Open source client and server |
| Where the data lives | United States | United States | United States (Clarivate) | United States (Elsevier) | Netherlands |
| Institutional sign-in | No | No | No | No | Yes, via SURFconext |
| Free storage | 300 MB | Unlimited on institution plans | Online storage included with the license | 2 GB personal and 100 MB shared | Sized by the institutions |
| Group libraries | Draw on the owner's quota | Unlimited | Limited collaboration features | Private groups are capped and share 100 MB | Full group libraries, no quota |
| Cost model | Free | Individual plans at $20 to $120 per user per year, or an institution plan, about 5,000 euro per year for a university with 15,000 students and staff | About $110 per seat per year in one public university program, campus-wide quotes on request | Free; several universities ended their institutional licenses in 2024 | Staff time plus a small server environment |
| Self-hosting | Files only, through WebDAV, and group libraries not at all | Same | No | No | The whole service |

For fairness, zotero.org is run by a nonprofit, and its storage subscriptions
fund Zotero's development. A national server does not remove the case for
supporting Zotero itself, and the pilot budget should include a contribution
to the Zotero project. Also, altero exists because a self-hosted option was
missing, not because zotero.org serves users badly.

EndNote and Mendeley show the two other models. EndNote is licensed per
seat. One public university's site license program charges $110 per seat per
year, and a campus-wide agreement is quoted individually by Clarivate.
Mendeley shows what a closed institutional arrangement can cost later.
Institutional
Mendeley licenses ended at several universities in 2024,
including the University of Twente's, which dropped users there to 2 GB of
personal storage and 100 MB of shared storage. A service built on open source
software has no equivalent risk, because the institutions hold the source code
and can always move the data.

### The wider field

The table below makes the same comparison across the rest of the market.
Prices are quoted individually where no public figure exists.

| Tool | Institutional price | Data location | Openness | Autonomy and exit |
|---|---|---|---|---|
| RefWorks (Clarivate) | Campus subscription, quote-based | United States | Closed | Being retired; Clarivate purges accounts 120 days after a license ends, and steers users to EndNote Fusion |
| EndNote and EndNote Fusion (Clarivate) | About $110 per seat per year in one public program, campus quotes otherwise | United States | Closed | Proprietary library format; Fusion adds sign-on, analytics and AI under Clarivate's cloud |
| Citavi (Lumivero) | Campus license, quote-based | Provider cloud, run by Lumivero | Closed | At least one German university forbids storing personal or confidential project data in the Citavi cloud |
| Paperpile | From roughly $50 per user per year at list price, half that with the academic discount; site licenses quoted | The user's own Google Drive | Closed | Requires Google accounts; export through open formats |
| Lean Library Workspace, formerly Sciwheel | Institutional, quoted | Provider cloud, run by Technology from Sage | Closed | Changed hands and name; users were moved to the renamed Lean Library extension in 2025 |
| ReadCube and Papers (Digital Science) | Individual and institutional | United States | Closed | Niche in the Netherlands |
| JabRef | Free | No central service | Open source | BibTeX-centered, no managed group synchronization, so it solves a different problem |

### Functionality overview

The tables below compare the same products on the two sides that matter for
this decision: what the user runs, and what the institution runs. The client
differences are mostly a matter of taste. The hosting differences are more
important.

What the user runs:

| Product | Desktop app | Browser connector | Word processor plugins | PDF reader with annotations | Mobile apps | Open source |
|---|---|---|---|---|---|---|
| Zotero Desktop | Windows, macOS, Linux | Yes, all major browsers | Word, LibreOffice, Google Docs | Yes | iOS and Android | Yes |
| EndNote 2025 and Fusion | Windows, macOS | Yes | Word, plus LibreOffice and OpenOffice on Windows; Google Docs through EndNote Web | Yes | iOS only, iPhone and iPad | No |
| Mendeley Reference Manager | Windows, macOS, Linux | Yes | Word | Yes | None; the old apps were retired in 2021 | No |
| Citavi | Windows, plus a web app | Yes, the Citavi Picker | Word | Yes | None; web only | No |
| Paperpile | None, it is a web app | Yes | Word and Google Docs | Yes | iOS and Android | No |
| Lean Library Workspace | None, web app | Yes | Word and Google Docs | Yes | None | No |
| ReadCube and Papers | Windows, macOS | Yes | Word | Yes | iOS and Android | No |
| JabRef | Windows, macOS, Linux (Java) | Yes, BibTeX capture | LibreOffice native, Word via add-ons | Basic | None | Yes, MIT |
| RefWorks, being retired | None, web app | Yes | Word and Google Docs through RefWorks Citation Manager | Basic | None | No |

What the institution runs:

| Product | Hosting options | Group libraries | Institutional sign-in | Account administration | API for other tools |
|---|---|---|---|---|---|
| zotero.org | Managed only, nonprofit, United States | Yes, files draw on the owner's quota | No | None, self-service accounts | Yes, Web API v3 |
| altero, the proposed national server | Managed by SURF, or self-hosted | Yes, full group libraries with shared storage | Yes, SURFconext through OIDC or SAML | Yes: accounts created at first sign-in, attribute-based suspension, retention settings | Yes, Web API v3 plus an OAuth 2.0 server |
| Zotero dataserver, self-hosted | Self-hosted only, no supported installation | Yes | No | None, no admin interface | Yes, Web API v3 |
| Zotero with WebDAV | Any WebDAV server, attachment files only | No, personal library files only | No | No | No, metadata stays on zotero.org |
| EndNote and Fusion | Managed only, Clarivate | Yes, shared groups and projects | Fusion: yes | Fusion: admin console with analytics | No |
| Mendeley | Managed only, Elsevier | Limited: 5 groups of up to 25 members and 100 MB shared storage on the free tier | No | None | Limited, closed program |
| Citavi | Lumivero cloud, or Citavi DB Server on a local Windows server for shared projects | Shared projects, yes | No | License management only | No |
| Paperpile | Managed only, on Google infrastructure | Yes, shared libraries | Google accounts, or SAML SSO on institutional plans | Site license console | Limited, export through Google Drive |
| Lean Library Workspace | Managed only | Yes, shared projects | Not verified | Not verified | No |
| ReadCube and Papers | Managed only | Shared collections | Not verified | Not verified | No |
| JabRef | No server; share files or a Git repository | No | No | No | No |
| RefWorks | Managed only, being retired | Yes | Yes, institutional login | Institutional admin console | No |

### Known use in Dutch institutions

The table below shows where each product is already used in the Netherlands,
and who to ask for first-hand experience and prices. The Dutch university
RefWorks licensees below have all left the product, and Twente has now
dropped two reference managers in two years. The replacements are Zotero,
Mendeley or Clarivate products.

| Product | Known use in the Netherlands | Where to get more detail |
|---|---|---|
| Zotero, client | Guides and support at nearly every university library, including Utrecht, Leiden, Amsterdam and Twente | The libraries' information specialists |
| Zotero, institution storage | The University of Twente, the originator of this proposal: a Zotero Institution subscription at about 5,000 euro per year covering roughly 5,000 FTE and 10,000 students, and a campus-wide license running since September 2025 with unlimited storage for @utwente.nl addresses | zotero.org storage contact; Twente's library |
| EndNote | Campus licenses at Leiden, Radboud, Maastricht and Utrecht; Radboud's version is distributed through SURFspot. Twente ended its license on December 31, 2025 | The libraries; SURFspot for member pricing; Clarivate sales |
| EndNote Fusion | Erasmus University Rotterdam moved its RefWorks users to Fusion in October 2026 | The EUR library; Clarivate sales |
| Mendeley | Twente's institutional license ended in December 2024. Avans moved its users from RefWorks to Mendeley | Twente's library; Avans Xplora; Elsevier support |
| RefWorks | Groningen ended it in December 2025, Utrecht required data export before January, Amsterdam ended access on June 30, 2025, and Erasmus moved to Fusion | The four libraries; Clarivate |
| Citavi | No public Dutch campus license found; the published adoption list covers German institutions | Lumivero or its reseller Alfasoft |
| Paperpile | No public Dutch institutional licensees found | Paperpile sales |
| Lean Library Workspace, formerly Sciwheel | No public Dutch licensees found | Technology from Sage |
| ReadCube and Papers | No public Dutch licensees found | Digital Science |
| JabRef, self-hosted dataserver, altero | No known institutional deployments in the Netherlands. altero has no production deployments anywhere yet, so a pilot would be the first | altero's GitHub discussions |

The comparison above does not change the recommendation. First, there is
interoperability. Zotero Desktop, its browser connector, its word processor
plugins and its catalog of citation styles form one ecosystem, and only
zotero.org and altero serve that client. Choosing another manager means
choosing a different client and migrating every library. Second, product
turnover is the autonomy argument in practice. RefWorks is being retired,
and institutional Mendeley licenses ended at several universities in 2024.
Sciwheel users were moved to a renamed product. A hosted service always
carries the risk that the product around the data changes or disappears.
Self-hosting the server does not prevent that, but it keeps the data, the
client and the exit path under the institutions' control.

For completeness, Zotero's own dataserver
is open source, so a technical team can run it. Nobody maintains self-hosting
as a product, though. The project documents no supported installation, and
the community Docker and LXC projects are one-person efforts that have
stalled. A national service on the dataserver would mean operating a legacy
MySQL stack with a search cluster, no web interface, no account administration
and no SURFconext integration. altero is the maintained product for the
operating model this proposal describes.

## What it takes to set up

The deployment is small: one application, one PostgreSQL database
and one directory of attachment files, with a TLS endpoint in front for
encrypted HTTPS access. There is no search cluster, message queue or object
store to run. The published Docker
image needs no build, so the setup is:

1. Order a small virtual machine or container platform at SURF, mount an
   attachment volume on block storage, and point an SMTP relay at the server.
2. Deploy the Docker Compose stack, set the public URL, the database password
   and the reverse proxy, and confirm a Zotero Desktop client can synchronize.
3. Register the service in the SURFconext SP Dashboard test environment and add
   the SURFconext sign-in provider in the administration screen. The whole
   desktop sign-in flow can be tested before production.
4. Test the backup and restore procedure, because a pilot institution will
   ask about it first.

The engineering work is three to five working days. The calendar time is
dominated by the SURFconext registration and the agreements around it, which
SURF handles as part of its normal connection process.

## What it takes to run

Tier 1 support stays with local libraries and IT helpdesks, because questions
about using Zotero are the same as today. The central team
handles everything server-side:

| Phase | Scale | Staff | Main tasks |
|---|---|---|---|
| Pilot | 1 to 2 institutions, hundreds to a few thousand users | 0.1 to 0.15 FTE | Monitoring, monthly updates, backup checks, close contact with pilot users, feedback to the altero project |
| Early production | 5 to 20 institutions, tens of thousands of users | 0.15 to 0.25 FTE | The same, plus onboarding institutions through SURF and capacity management |
| National service | Most of the sector, 50,000 or more users | 0.25 to 0.4 FTE | The same, plus tier 2 support coordination and longer-term capacity planning |

Onboarding an institution is mostly automatic. SURF connects its identity
provider, and users sign in and get an account on first use, once automatic
account creation is turned on for the provider. When someone leaves an
institution, the server notices on their next sign-in, if the provider is
configured to require an institutional claim, and suspends the account. The
suspension also blocks the desktop client. The data is kept for
reinstatement or removal under the retention policy. Someone who never
signs in again is not caught automatically. An administrator handles that
case instead.

## Connecting Zotero clients

Each user connects an unmodified Zotero Desktop installation once. The
pilot needs no build, no fork and no client patch:

1. In **Settings, Advanced, Config Editor**, set two preferences:
   `extensions.zotero.api.url = https://<server>/` (the trailing slash
   matters) and `extensions.zotero.streaming.url = wss://<server>/stream`,
   then restart Zotero. Both are needed unless streaming is disabled
   outright. The API preference does not redirect the streaming connection,
   and a client that keeps the built-in zotero.org streaming endpoint may
   send the altero API key to zotero.org, which rejects it but may log it. A
   distributed package that sets both preferences,
   described below, closes this trap.
2. In **Settings, Sync, Link Account**, the client asks the server for a
   login session, opens the server's browser page, and the user signs in
   through their own institution via SURFconext and approves the
   client. Approval always asks for a fresh proof of identity, so an
   institutional sign-in gets a "confirm with provider" step rather than
   reusing an existing browser session. The client receives an API key that
   stays valid until it is revoked.

A desktop profile that has synced with zotero.org carries its old numeric
account id and will not silently link to a different account. Linking is
refused and the message names the id. An administrator then creates the
account under that id with one command in the server shell, which is also
the documented path for moving a personal library from zotero.org.
Attachment files can stay on an institutional WebDAV server, which stores
files using the WebDAV web standard, or be moved into the national server.
Group libraries always carry their files through the server. The official
iOS and Android applications compile the zotero.org hosts into the binary
and cannot be redirected by settings, so they need a patched build, as
discussed below. The pilot is desktop-first.

### Distributing a pre-configured client

The manual steps above are one-time, but a sector service should not ask
100,000 people to edit a config editor. The table below compares the two
ways to remove them:

| | Companion extension | Patched full build |
|---|---|---|
| What SURF ships | Official Zotero installer plus a small plugin, or the plugin alone pushed by institutions | Installers built from the official client repository with a preferences patch |
| User steps | Install Zotero, install or receive the plugin | Install one download |
| Survives official client updates | Yes; the plugin re-asserts the preferences at startup | No; each client release needs a rebuild and its own update channel |
| Build effort | Small: one plugin, tested against each pinned desktop release | Large: per-platform build, macOS notarization, Windows code signing, update infrastructure |
| Mobile apps | No | Yes, with the same pipeline applied to the mobile apps |
| Exit path | Uninstalling the plugin restores stock behavior | Users switch back to official downloads |

The companion extension is the recommended first step, and a working
version exists in this repository at `tools/surf-sync-plugin/`. Zotero loads
bootstrap plugins, which are add-on programs that start with the client. The
compatibility harness itself installs one in every test profile. The plugin
captures the client's current preferences on first run, sets both
preferences as the sign-in flow expects, re-asserts them after client
updates, restores the originals when uninstalled, and writes nothing while
disabled. It was verified against the pinned Zotero 10.0.5 desktop release:
installation sets exactly the two expected preferences, uninstalling
through the add-on manager restores the prior state, and one undocumented
client requirement surfaced during testing — Zotero 10 rejects any plugin
manifest without an `update_url` entry, which the plugin's manifest now
carries and its README explains. "Zotero from SURF"
can then mean the official
installer plus one plugin file, distributed from a SURF download page or
pushed by institutional IT the way managed browser extensions already are.

The patched full build is the heavier option, and a working pipeline
skeleton exists at `tools/surf-client-build/` with a CI workflow in
`.github/workflows/surf-client-build.yml`. SURF's build system checks
out the official client repository at a pinned release tag, applies a patch
that defaults both preferences to the national server, and publishes signed
installers. It gives users an out-of-the-box client, and the same pipeline
applied to the mobile repositories is the only route to official mobile
apps on the national server. Its costs are operational, not technical. SURF
must rebuild on every client security release, run an update channel
because a renamed build cannot use Zotero's official updates, and label the
distribution clearly so the Zotero name and trademarks are respected. The
pilot should run on the extension. The case for full builds, desktop first
and mobile second, is a decision the pilot evidence should inform.

## What it needs

Planning figures: Dutch higher education has about one million students and
roughly 100,000 to 150,000 staff. Confirm the exact numbers with UNL, the
Vereniging Hogescholen and SURF when drafting the final proposal. Most of those
people never need the server. By rough estimate, half of all students never
upload an attachment and a quarter only use group libraries, and the FTE and
student counts include many support staff and researchers who hardly use
reference management. The scenarios below therefore assume 50 MB of attachments per
active user on average, treated as an upper limit for the first estimate, and
adjusted from pilot usage data once real numbers exist. Deduplication
reinforces the estimate. The server stores each file once per digest, which
is a checksum of the file's content. The PDF a supervisor and ten PhD
students all hold is on disk once. The database holds metadata only and
stays small even compared with the modest attachment store.

| Scenario | Active users | Attachments | Database | Application | PostgreSQL |
|---|---|---|---|---|---|
| Pilot | 2,000 | 100 GB | Under 2 GB | 1 node, 2 vCPU, 4 GB | 2 vCPU, 8 GB |
| Early production | 25,000 | 1.3 TB | 10 to 20 GB | 2 nodes, 4 vCPU, 8 GB each | 4 to 8 vCPU, 32 GB, fast disk |
| National | 100,000 | 5 TB | Around 50 GB | 3 to 4 nodes behind a load balancer | 8 to 16 vCPU, 64 GB |

The numbers are credible because the application is measured at about 125 MB
of memory when idle, and attachments are stored once per file digest so
shared PDFs are not duplicated. The database only holds metadata. The
attachment directory must stay on a block-backed filesystem or an NFS mount,
with backups going to object storage, because object-storage filesystem
mounts implement rename as a copy followed by a delete, and the server will
not fall back to copying.

## What it costs

Indicative only. Infrastructure is priced at market rates: small virtual
machines plus bulk attachment storage at 3 to 10 euro per terabyte per month.
At 50 MB per active user, the storage cost is negligible and the virtual
machines dominate the infrastructure cost. Staff effort is stated as
approximate FTE and left unpriced. SURF's own internal rates determine that
line.

| Scenario | Infrastructure per year | Staff (approximate FTE) |
|---|---|---|
| Pilot, 2,000 users | 1,500 to 3,000 euro | 0.10 to 0.15 |
| Early production, 25,000 users | 2,000 to 6,500 euro | 0.15 to 0.25 |
| National, 100,000 users | 10,000 to 20,000 euro | 0.25 to 0.40 |

The comparison comes from the status quo. The University of Twente, the
originator of this proposal, already pays about 5,000 euro per year for a
Zotero institution subscription with unlimited storage, covering roughly
5,000 FTE and 10,000 students. Scaled by
addressable population to the whole sector, about 75 times larger, the total
is roughly 350,000 to 400,000 euro per year. A shared national server
at 100,000 active users needs 10,000 to 20,000 euro per year of
infrastructure, roughly 200 to 400 euro per institution per year across the
sector's roughly fifty institutions, plus 0.25 to 0.40 FTE of staff time. It
adds what the subscription does not offer. The data stays in the country,
and sign-in runs through SURFconext. The comparison holds whatever internal
rate SURF applies to that staff line, because the effort is a fraction of one
person's time. The pilot is cheap in absolute terms and produces the evidence
needed for the national decision.

## Maturity and risks

altero is at release 1.0.0-beta.2. Two real Zotero profiles passed 47 scenario
and database combinations across SQLite and PostgreSQL, covering 594 phases of
desktop synchronization, and the project documents what is deliberately not
implemented. The warnings relevant to this proposal:

- **Treat the pilot as a pilot.** Keep backups and keep zotero.org or local
  copies available during the pilot. Do not migrate irreplaceable libraries
  until the pilot report is positive.
- **Mobile.** The official Zotero iOS and Android applications have the server
  address compiled in and cannot point at another server. Desktop is the
  supported platform. Mobile needs a custom build, which the project supports
  but does not distribute.
- **Maintainer capacity.** altero currently depends on a small team of
  maintainers. The license and public source remove the vendor part of that
  risk, and SURF operating the service is the kind of deployment that widens
  the contributor base.
- **Agreements.** SURF acts as processor, institutions as controllers, so a
  data processing agreement and a retention policy are part of the pilot
  setup. The SURFconext client id must stay fixed once issued, because the
  user identifiers SURF issues are tied to it.

## Recommended next steps

1. SURF holds an intake meeting with the altero maintainer and evaluates this
   proposal and the SSO analysis.
2. SURF registers the service in the SURFconext test environment, and one or
   two institutions run a pilot for one semester with real libraries and a
   support arrangement as described above.
3. The pilot report decides on general availability: measured sync reliability,
   real support load, storage growth and user satisfaction.

## References

- [Why altero exists](https://altero.run/latest/motivation/) and the
  [implementation status](https://altero.run/latest/status/)
- [Connecting a Zotero client](https://altero.run/latest/clients/), the
  client documentation this section summarizes
- [Zotero client source repository](https://github.com/zotero/zotero) and
  [dataserver source repository](https://github.com/zotero/dataserver),
  both AGPL-3.0
- [SURFconext OpenID Connect reference](https://servicedesk.surf.nl/wiki/spaces/IAM/pages/128909841/OpenID+Connect+reference)
  and [connecting in five steps](https://servicedesk.surf.nl/wiki/spaces/IAM/pages/128910038/Connect+to+SURFconext+in+5+Steps)
- [Zotero storage pricing](https://www.zotero.org/storage/) and the
  [institution storage FAQ](https://www.zotero.org/support/storage_institutions_faq)
- [EndNote site license order form, University of Hawaiʻi](https://www.hawaii.edu/sitelic/endnote/endnoteform.pdf),
  the source of the $110 per seat per year figure
- [Twente ends its EndNote license and moves to Zotero](https://www.utwente.nl/onderwijs/student-services/actueel/nieuws/2025/11/560478/endnote-licentie-eindigt-op-31-december-2025)
- [Radboud's EndNote 2025 on SURFspot](https://www.surfspot.nl/endnote-2025-radboud-universiteit.html)
- [RefWorks becomes EndNote Fusion, Erasmus University Rotterdam](https://www.eur.nl/nieuws/refworks-wordt-endnote-fusion)
- [RefWorks ends in December 2025, University of Groningen](https://www.rug.nl/library/news/251030-refworks-ends-december-2025)
- [Transfer your RefWorks data before 1 January, Utrecht University](https://www.uu.nl/en/news/transfer-your-refworks-data-before-1-january)
- [Access to RefWorks ends on 30 June, University of Amsterdam](https://uba.uva.nl/en/content/news/2025/05/access-to-refworks-ends-on-30-june.html)
- [From RefWorks to Mendeley, Avans Hogeschool](https://avans.libguides.com/blogs/Xplora-Nieuws/van-refworks-naar-mendeley)
- [List of Citavi use at higher education institutions, Bibhub](https://biblioarchive.blog/2025/03/05/liste-citavi-nutzung-an-hochschulen/),
  covering German institutions
- [Mendeley institutional license discontinuation, University of Twente](https://www.utwente.nl/en/lisa-library-news/2024/12/29937/discontinuation-mendeley-institutional-license)
- [RefWorks access discontinuing, University of Georgia](https://www.libs.uga.edu/refworks-discontinued),
  including the 120-day account purge after license end
- [EndNote Fusion](https://endnote.com/fusion/), Clarivate's successor product
- [Paperpile pricing](https://paperpile.com/pricing/) and
  [site licenses](https://paperpile.com/sites/); its
  [iOS and Android apps](https://paperpile.com/ios-and-android/) are official
- [Mendeley mobile app retirement](https://blog.mendeley.com/2021/03/11/mendeley-refocusing-announcement-mobile-app-retirement/)
- [Citavi cloud privacy notice, HTWK Leipzig](https://bibliothek.htwk-leipzig.de/en/recherche/literatur-verwalten/citavi-cloud),
  restricting personal and confidential data in the Citavi cloud
- [Sciwheel is becoming Lean Library Workspace](https://leanlibrary.com/sciwheel-is-becoming-lean-library-workspace/)
- [Self-hosting documentation request, zotero/dataserver issue 105](https://github.com/zotero/dataserver/issues/105),
  the state of dataserver self-hosting
- [Zotero synchronization overview](https://www.zotero.org/support/sync),
  the basis for the WebDAV and group-library comparison
