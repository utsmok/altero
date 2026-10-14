# Brief: a national Zotero server for the Netherlands, hosted by SURF

Samuel Mok, information specialist, Universiteit Twente
([s.mok@utwente.nl](mailto:s.mok@utwente.nl)), October 14, 2026.

This brief summarizes the proposal in [national-hosting-proposal.md](national-hosting-proposal.md),
which carries the full analysis, the figures and the sources. Both documents
are fork-local research material and are not part of the altero documentation
set.

## The idea

Zotero is the free reference manager our library now supports. By default it
copies every library, including attached PDFs and notes, to servers at
zotero.org in the United States. The proposal is that SURF operates one shared
server for all Dutch universities and hogescholen, running altero, an open
source program that behaves exactly like the zotero.org service. Researchers
and students keep the Zotero Desktop application they already use, sign in
with their own institutional account through SURFconext, and their library
stays in the Netherlands.

## Why now

The timing comes from the market, not from the software. Twente ended its
Mendeley license in December 2024 and its EndNote agreement on December 31,
2025, and moved to Zotero with an institution subscription of about 5,000 euro
per year. Groningen, Utrecht, Amsterdam and Erasmus are leaving RefWorks in
the same period, so the sector is paying for reference-manager migrations
either way. The question is where these migrations land. A shared open source
server is the landing place that keeps the data, the client and the exit path
under the institutions' own control. altero has reached the state where the
idea is testable: it passed an acceptance suite of 47 scenarios with real
Zotero client profiles, and the SURFconext sign-in is implemented rather than
promised.

## What users would notice

For daily work, almost nothing changes. The Zotero Desktop application, the
browser connector, the Word plugin and the built-in PDF reader keep working,
and every library also keeps a complete copy on the user's own device. There
are two differences. First, the sign-in screen on first use belongs to the
user's own institution instead of zotero.org. Second, the client needs a
one-time setting that points it at the national server, and a small companion
plugin sets that setting automatically, so most users never see it. Official
phone and tablet applications only work with zotero.org, so the service starts
desktop-first, and mobile follows with a custom build if the pilot goes well.

## Why this is a good idea

- **Privacy and the GDPR.** Library data, including PDFs and notes, stays on
  Dutch infrastructure under EU law, and sign-in releases the minimum set of
  personal details the service needs.
- **Cost.** There are no per-seat licenses. National infrastructure costs an
  estimated 10,000 to 20,000 euro per year plus a fraction of one staff
  position, against roughly 350,000 to 400,000 euro per year if every
  institution bought its own zotero.org subscription.
- **Independence.** The institutions hold the source code, export is a core
  feature of the client, and the service can move between hosting providers.
  No vendor can change the product around the data or close the account.
- **Continuity.** The desktop application keeps a complete local copy of every
  library, so users are protected even if the service ever stops.

## The honest drawbacks

- zotero.org already works and is affordable. An institution that does not
  care where its data lives gets a cheaper and lower-risk service there, and
  the national server earns its keep specifically on data location, group
  libraries, institutional sign-in and account management.
- altero is young. It is at release 1.0.0-beta.2 and has no production
  deployments anywhere yet, which is exactly why the plan starts with a pilot
  and not with a national rollout.
- The two client settings that redirect the desktop application are not an
  officially supported configuration surface, so a future desktop release
  could change their behavior. A compatibility suite pins tested releases and
  the distributed client package sets both settings, which keeps this risk
  small but not zero.
- Official mobile apps cannot connect to any other server today. Desktop is
  the supported platform for the pilot.
- The software is not the hard part. Retention policy, uptime commitments and
  multi-year funding are, and they belong to SURF rather than to the
  software.

## What it takes

| Phase | Users | Setup effort | Staff | Infrastructure per year |
|---|---|---|---|---|
| Pilot, 1 to 2 institutions | hundreds to a few thousand | 3 to 5 working days | 0.10 to 0.15 FTE | 1,500 to 3,000 euro |
| National service | 50,000 or more | none, it scales from the pilot | 0.25 to 0.40 FTE | 10,000 to 20,000 euro |

The deployment is one application, one database and a directory of files, so
the setup is measured in days. Local support work does not change, because
questions about using Zotero stay with the local library either way. For
scale, Twente's own subscription costs about 5,000 euro per year for one
institution, and a national server costs each institution roughly 200 to 400
euro per year.

## What a national server adds beyond storage

The same server can become the place where publications flow between Zotero,
ORCID and the institutional repository. Users link their ORCID iD once, and
the server publishes their works to ORCID with their consent, where Pure and
other research-information systems already pick them up. The server can also
warn every user about retracted papers, using the retraction list that Zotero
clients already request. These additions are not part of the pilot. They are
the reason a shared server is a platform rather than a disk.

## Proposed next steps

1. Take the proposal to SURF for an intake meeting with the altero
   maintainer.
2. Offer Twente as one of the pilot institutions for a one-semester pilot with
   real libraries.
3. Decide on wider adoption from the pilot report: measured reliability, real
   support load and storage growth.

Your backing for the first two steps is all I need. Until the pilot starts,
the only Twente cost is a small amount of my time.
