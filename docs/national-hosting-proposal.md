# Proposal: a shared Zotero sync server for Dutch higher education

Draft proposal for SURF, universities and hogescholen, October 10, 2026.
This document is fork-local research material and is not part of the altero
documentation set. The technical SSO analysis it builds on is in
[sso-surf.md](sso-surf.md).

## Summary

The proposal is that SURF operates one shared altero server for all Dutch
universities and hogescholen. Users keep the Zotero Desktop application they
already use, sign in through their own institution via SURFconext, and keep
their library data on Dutch infrastructure. altero is free software under the
AGPL-3.0 license, so there are no license fees. The realistic costs are one
small server landscape and 0.1 to 0.4 FTE of staff time, depending on scale,
and a few terabytes of attachment storage even at national size.
A pilot with one or two institutions can start after a short technical
preparation, and the SURFconext connection is configuration work because
altero already implements it.

## What is proposed

A sync server is the service that copies a reference library between a
researcher's devices and their group's shared library. Zotero is a widely used,
free, open source reference manager. Its desktop application is open source and
runs everywhere. By default it synchronizes with a service at zotero.org in the
United States.

altero is an open source server that speaks the same synchronization protocol.
An unmodified Zotero Desktop application synchronizes with it, including
attachments, notes, annotations, full-text search and group libraries. One
server can serve all institutions, because users sign in through SURFconext and
altero already supports that sign-in method.

## Why this is worth doing

- **Privacy and the GDPR.** Library data, including PDFs and notes, stays on
  infrastructure in the Netherlands under EU law. Sign-in releases the minimum
  set of attributes, the server does no profiling, and the administrator role
  is designed so that operating the service does not mean reading everyone's
  library.
- **Autonomy.** Institutions stop depending on one American service's storage
  quotas, pricing and terms. A group library no longer draws on the personal
  quota of whichever member owns the group.
- **Open source.** The server is AGPL-3.0, the client is open source, and
  export is a first-class feature, so users and institutions are never locked
  in. Institutions can fix or extend the software instead of filing wishes
  with a vendor.
- **Cost.** There are no per-seat licenses. The cost is staff time and one
  small server landscape, under one euro per active user per year at national
  scale under the assumptions below.
- **Continuity.** The desktop application keeps a complete local copy of every
  library, so users are protected even if the service stops. The service can be
  moved between infrastructures because both the client and the server are open
  source.

### How the alternatives compare

| | zotero.org free | zotero.org paid | EndNote | Mendeley | Shared altero server |
|---|---|---|---|---|---|
| Software | Open source client | Open source client | Commercial | Closed, owned by Elsevier | Open source client and server |
| Where the data lives | United States | United States | United States (Clarivate) | United States (Elsevier) | Netherlands |
| Institutional sign-in | No | No | No | No | Yes, via SURFconext |
| Free storage | 300 MB | Unlimited on institution plans | Limited online storage included with the license | 2 GB personal and 100 MB shared since the institutional upgrade ended | Sized by the institutions |
| Group libraries | Draw on the owner's quota | Unlimited | Limited collaboration features | Private groups are capped and share 100 MB | Full group libraries, no quota |
| Cost model | Free | Individual plans at $20 to $120 per user per year, or an institution plan, about 5,000 euro per year for a university with 15,000 students and staff | About $110 per seat per year in one public university program, campus-wide quotes on request | Free after the institutional edition was discontinued in 2024 | Staff time plus a small server landscape |
| Self-hosting | Files only, through WebDAV, and group libraries not at all | Same | No | No | The whole service |

Two notes for fairness. First, zotero.org is run by a nonprofit, and its
storage subscriptions fund Zotero's development. A national server does not
remove the case for supporting Zotero upstream, and the pilot budget should
include a contribution to the Zotero project. Second, altero exists because a
self-hosted option was missing, not because zotero.org serves users badly.

EndNote and Mendeley show the two other models. EndNote is licensed per seat:
one public university's site license program charges $110 per seat per year,
and a campus-wide agreement is quoted individually by Clarivate. Mendeley
shows what a closed institutional arrangement can cost later: Elsevier
discontinued the Mendeley Institutional Edition in 2024, and at the University
of Twente the institutional benefits ended, which dropped users to 2 GB of
personal storage and 100 MB of shared storage. A service built on open source
software has no equivalent risk, because the institutions hold the source code
and can always move the data.

### The wider field

The same comparison across the rest of the market. Prices are quoted
individually where no public figure exists.

| Tool | Institutional price | Data location | Openness | Autonomy and exit |
|---|---|---|---|---|
| RefWorks (Clarivate) | Campus subscription, quote-based | United States | Closed | Being retired; Clarivate purges accounts 120 days after a license ends, and steers users to EndNote Fusion |
| EndNote and EndNote Fusion (Clarivate) | About $110 per seat per year in one public program, campus quotes otherwise | United States | Closed | Proprietary library format; Fusion adds sign-on, analytics and AI under Clarivate's cloud |
| Citavi (Lumivero) | Campus license, quote-based | Provider cloud, run by Lumivero | Closed | At least one German university forbids storing personal or confidential project data in the Citavi cloud |
| Paperpile | From roughly $50 per user per year with the academic discount, site licenses quoted | The user's own Google Drive | Closed | Requires Google accounts; export through open formats |
| Lean Library Workspace, formerly Sciwheel | Institutional, quoted | Provider cloud, run by Technology from Sage | Closed | Dropped or migrated by several universities after the product changed hands and name |
| ReadCube and Papers (Digital Science) | Individual and institutional | United States | Closed | Niche in the Netherlands |
| JabRef | Free | No central service | Open source | BibTeX-centered, no managed group synchronization, so it solves a different problem |

### Known use in Dutch institutions

Where each product already has a Dutch footprint, and who to ask for
first-hand experience and prices. The commercial pattern here is not subtle:
every Dutch RefWorks licensee is leaving the product, Twente has now dropped
two reference managers in two years, and the replacements are either Zotero or
Clarivate products.

| Product | Known use in the Netherlands | Where to get more detail |
|---|---|---|
| Zotero, client | Guides and support at nearly every university library, including Utrecht, Leiden, Amsterdam and Twente | The libraries' information specialists |
| Zotero, institution storage | Not public. At least two universities: the originator of this proposal (about 5,000 euro per year for roughly 5,000 FTE and 10,000 students) and Twente, whose campus-wide license has run since September 2025 with unlimited storage for institutional addresses | zotero.org storage contact; the two libraries directly |
| EndNote | Campus licenses at Leiden, Radboud, Maastricht and Utrecht; Radboud's version is distributed through SURFspot. Twente ends its license on December 31, 2025 | The libraries; SURFspot for member pricing; Clarivate sales |
| EndNote Fusion | Erasmus University Rotterdam is migrating its RefWorks users to Fusion | The EUR library; Clarivate sales |
| Mendeley | Twente's institutional license ended in December 2024. Avans moved its users from RefWorks to Mendeley | Twente's library; Avans Xplora; Elsevier support |
| RefWorks | Groningen ended it in December 2025, Utrecht required data export before January, Amsterdam ended access on June 30, 2025, and Erasmus is moving to Fusion | The four libraries; Clarivate |
| Citavi | No public Dutch campus license found; the published adoption list covers German institutions | Lumivero or its reseller Alfasoft |
| Paperpile | No public Dutch institutional licensees found | Paperpile sales |
| Lean Library Workspace, formerly Sciwheel | No public Dutch licensees found | Technology from Sage |
| ReadCube and Papers | No public Dutch licensees found | Digital Science |
| JabRef, self-hosted dataserver, altero | No known institutional deployments in the Netherlands. altero has no production deployments anywhere yet, so a pilot would be the first | altero's GitHub discussions |

None of this changes the recommendation, for two reasons. First,
interoperability: Zotero Desktop, its browser connector, its word processor
plugins and its catalog of citation styles form one ecosystem, and only
zotero.org and altero serve that client. Choosing another manager means
choosing a different client and migrating every library. Second, product churn
is the autonomy argument in practice: RefWorks is being retired, the Mendeley
institutional edition ended in 2024, and Sciwheel users were moved to a
renamed product. A hosted service always carries the risk that the product
around the data changes or disappears. Self-hosting the server does not
prevent that, but it keeps the data, the client and the exit path under the
institutions' control.

One further option deserves mention for completeness: Zotero's own dataserver
is open source, so a technical team can run it. Nobody maintains self-hosting
as a product, though. The project documents no supported installation, the
community Docker and LXC projects are one-person efforts that have stalled,
and a national service on the dataserver would mean operating a legacy PHP and
MySQL stack with a search cluster, no web interface, no account administration
and no SURFconext integration. altero is the maintained product aimed at
exactly the operating model this proposal describes.

## What it takes to set up

The deployment is deliberately small: one application, one PostgreSQL database
and one directory of attachment files, with a TLS endpoint in front. There is
no search cluster, message queue or object store to run. The published Docker
image needs no build, so the setup is:

1. Order a small virtual machine or container platform at SURF, mount an
   attachment volume on block storage, and point an SMTP relay at the server.
2. Deploy the Docker Compose stack, set the public URL, the database password
   and the reverse proxy, and confirm a Zotero Desktop client can synchronize.
3. Register the service in the SURFconext SP Dashboard test environment and add
   the SURFconext sign-in provider in the administration screen. The whole
   desktop sign-in flow can be tested before production.
4. Test the backup and restore procedure, because that is what a pilot
   institution will ask about first.

The engineering work is three to five working days. The calendar time is
dominated by the SURFconext registration and the agreements around it, which
SURF handles as part of its normal connection process.

## What it takes to run

Tier 1 support stays where it belongs, with local libraries and IT helpdesks,
because questions about using Zotero are the same as today. The central team
handles everything server-side:

| Phase | Scale | Staff | Main tasks |
|---|---|---|---|
| Pilot | 1 to 2 institutions, hundreds to a few thousand users | 0.1 to 0.15 FTE | Monitoring, monthly updates, backup checks, close contact with pilot users, feedback to the altero project |
| Early production | 5 to 20 institutions, tens of thousands of users | 0.15 to 0.25 FTE | The same, plus onboarding institutions through SURF and capacity management |
| National service | Most of the sector, 50,000 or more users | 0.25 to 0.4 FTE | The same, plus tier 2 support coordination and longer-term capacity planning |

Onboarding an institution is mostly automatic: SURF connects its identity
provider, and users sign in and get an account on first use. When someone
leaves an institution, the server notices the next time they sign in and
suspends the account, which also blocks the desktop client, while keeping the
data for reinstatement or removal under the retention policy.

## What it needs

Planning figures: Dutch higher education has about one million students and
roughly 100,000 to 150,000 staff. Confirm the exact numbers with UNL, the
Vereniging Hogescholen and SURF when drafting the final proposal. Most of those
people never need the server. Roughly half of all students never upload an
attachment, about a quarter only use group libraries, and the FTE and student
counts include many support staff and researchers who hardly use reference
management. The scenarios below therefore assume 50 MB of attachments per
active user on average, treated as an upper limit for the first estimate, and
refit from pilot telemetry once real numbers exist. Deduplication reinforces
this: files are stored once per digest, so the PDF a supervisor and ten PhD
students all hold is on disk once. The database holds metadata only and stays
small next to even that modest attachment store.

| Scenario | Active users | Attachments | Database | Application | PostgreSQL |
|---|---|---|---|---|---|
| Pilot | 2,000 | 100 GB | Under 2 GB | 1 node, 2 vCPU, 4 GB | 2 vCPU, 8 GB |
| Early production | 25,000 | 1.3 TB | 10 to 20 GB | 2 nodes, 4 vCPU, 8 GB each | 4 to 8 vCPU, 32 GB, fast disk |
| National | 100,000 | 5 TB | Around 50 GB | 3 to 4 nodes behind a load balancer | 8 to 16 vCPU, 64 GB |

Context that makes these numbers credible: the application is measured at
about 125 MB of memory when idle, attachments are stored once per file digest
so shared PDFs are not duplicated, and the database only holds metadata. The
attachment directory must stay on a block-backed filesystem or an NFS mount,
with backups going to object storage, because the server refuses the
copy-then-rename behavior of object-storage filesystem mounts.

## What it costs

Indicative only, to be refined with SURF rates. Assumptions: 90,000 euro per
FTE per year including overhead, and 3 to 10 euro per terabyte per month for
bulk attachment storage. At 50 MB per active user, storage is a rounding error
and the virtual machines dominate the infrastructure cost.

| Scenario | Infrastructure per year | Staff per year | Total | Per active user per year |
|---|---|---|---|---|
| Pilot, 2,000 users | 1,500 to 3,000 euro | 9,000 to 14,000 euro | 10,500 to 17,000 euro | 5 to 8.50 euro |
| Early production, 25,000 users | 2,000 to 6,500 euro | 14,000 to 23,000 euro | 16,000 to 29,500 euro | 0.65 to 1.20 euro |
| National, 100,000 users | 10,000 to 20,000 euro | 23,000 to 36,000 euro | 33,000 to 56,000 euro | 0.35 to 0.55 euro |

The honest comparison comes from the status quo. One Dutch university already
pays about 5,000 euro per year for a Zotero institution subscription with
unlimited storage, covering roughly 5,000 FTE and 10,000 students. Scaled by
addressable population to the whole sector, about 75 times larger, that is
roughly 350,000 to 400,000 euro per year in total. A shared national server at
100,000 active users costs about a tenth of that, works out to roughly 600 to
1,000 euro per institution per year, and adds what the subscription does not
offer: the data stays in the country and sign-in runs through SURFconext. The
pilot costs more per active user, which is normal, and buys the evidence
needed for the national decision.

## Maturity and risks

altero is at release 1.0.0-beta.2. Two real Zotero profiles passed 47 scenario
and database combinations across SQLite and PostgreSQL, covering 594 phases of
desktop synchronization, and the project documents what is deliberately not
implemented. The warnings that matter for this proposal:

- **Treat the pilot as a pilot.** Keep backups and keep zotero.org or local
  copies available during the pilot. Do not migrate irreplaceable libraries
  until the pilot report is positive.
- **Mobile.** The official Zotero iOS and Android applications have the server
  address compiled in and cannot point at another server. Desktop is the
  supported surface; mobile needs a custom build, which the project supports
  but does not distribute.
- **Upstream capacity.** altero currently depends on a small upstream team.
  The license and public source remove the vendor-risk part of that, and SURF
  operating the service is exactly the kind of deployment that widens the
  contributor base.
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
- [SURFconext OpenID Connect reference](https://servicedesk.surf.nl/wiki/spaces/IAM/pages/128909841/)
  and [connecting in five steps](https://servicedesk.surf.nl/wiki/spaces/IAM/pages/128910038/)
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
  [site licenses](https://paperpile.com/sites/)
- [Citavi cloud privacy notice, HTWK Leipzig](https://bibliothek.htwk-leipzig.de/en/recherche/literatur-verwalten/citavi-cloud),
  restricting personal and confidential data in the Citavi cloud
- [Sciwheel is becoming Lean Library Workspace](https://leanlibrary.com/sciwheel-is-becoming-lean-library-workspace/)
- [Self-hosting documentation request, zotero/dataserver issue 105](https://github.com/zotero/dataserver/issues/105),
  the state of dataserver self-hosting
- [Zotero synchronization overview](https://www.zotero.org/support/sync),
  the basis for the WebDAV and group-library comparison
