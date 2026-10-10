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
small server landscape and 0.1 to 0.4 FTE of staff time, depending on scale.
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
- **Cost.** There are no per-seat licenses. The cost is storage and staff time,
  which at national scale works out to roughly one euro per active user per
  year under the assumptions below.
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
| Free storage | 300 MB | Unlimited on institution plans | Product includes limited online storage | Limited free storage | Sized by the institutions |
| Group libraries | Draw on the owner's quota | Unlimited | Limited collaboration features | Limited self-hosting and control | Full group libraries, no quota |
| Cost model | Free | Individual plans at $20 to $120 per user per year, or an institution plan priced per FTE | Recurring license fees | Free with commercial owner | Storage plus 0.1 to 0.4 FTE |
| Self-hosting | Files only, through WebDAV, and group libraries not at all | Same | No | No | The whole service |

Two notes for fairness. First, zotero.org is run by a nonprofit, and its
storage subscriptions fund Zotero's development. A national server does not
remove the case for supporting Zotero upstream, and the pilot budget should
include a contribution to the Zotero project. Second, altero exists because a
self-hosted option was missing, not because zotero.org serves users badly.

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
Vereniging Hogescholen and SURF when drafting the final proposal. Not everyone
needs a server: most libraries fit in the free tier. The scenarios below assume
1 GB of attachments per active user on average, which is generous for students
and modest for research groups, and a database that stays small next to the
attachments.

| Scenario | Active users | Attachments | Database | Application | PostgreSQL |
|---|---|---|---|---|---|
| Pilot | 2,000 | 2 TB | Under 2 GB | 1 node, 2 vCPU, 4 GB | 2 vCPU, 8 GB |
| Early production | 25,000 | 25 TB | 10 to 20 GB | 2 nodes, 4 vCPU, 8 GB each | 4 to 8 vCPU, 32 GB, fast disk |
| National | 100,000 | 100 TB | Around 50 GB | 3 to 4 nodes behind a load balancer | 8 to 16 vCPU, 64 GB |

Context that makes these numbers credible: the application is measured at
about 125 MB of memory when idle, attachments are stored once per file digest
so shared PDFs are not duplicated, and the database only holds metadata. The
attachment directory must stay on a block-backed filesystem or an NFS mount,
with backups going to object storage, because the server refuses the
copy-then-rename behavior of object-storage filesystem mounts.

## What it costs

Indicative only, to be refined with SURF rates. Assumptions: 90,000 euro per
FTE per year including overhead, and 3 to 10 euro per terabyte per month for
bulk attachment storage.

| Scenario | Infrastructure per year | Staff per year | Total | Per active user per year |
|---|---|---|---|---|
| Pilot, 2,000 users | 2,000 to 5,000 euro | 9,000 to 14,000 euro | 11,000 to 19,000 euro | 5 to 10 euro |
| Early production, 25,000 users | 4,000 to 10,000 euro | 14,000 to 23,000 euro | 18,000 to 33,000 euro | 0.70 to 1.30 euro |
| National, 100,000 users | 15,000 to 30,000 euro | 23,000 to 36,000 euro | 38,000 to 66,000 euro | 0.40 to 0.70 euro |

The comparison at the top gives the other side of the ledger: individual
zotero.org unlimited storage costs $120 per heavy user per year, and an
institution plan is priced per FTE across the whole institution. The national
server is cheaper per served user at scale and keeps the data in the country.
The pilot costs more per user, which is normal, and buys the evidence needed
for the national decision.

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
- [Zotero synchronization overview](https://www.zotero.org/support/sync),
  the basis for the WebDAV and group-library comparison
