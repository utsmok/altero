# Working on this fork

This checkout is Sam's fork of [eseifert/altero](https://github.com/eseifert/altero).
Upstream is authoritative for the product; this fork carries local work between
upstream syncs and exists to develop additions on top of altero.

## Remotes

| Remote    | Points at                          | Role                          |
|-----------|------------------------------------|-------------------------------|
| `upstream`| `https://github.com/eseifert/altero` | the main repo — never push   |
| `origin`  | `https://github.com/utsmok/altero`   | this fork — push here        |

## Before starting any work: sync upstream first

Always pull the latest upstream changes before beginning additions, so work
starts from current upstream code:

```sh
git checkout master
git fetch upstream
git merge upstream/master   # master stays = upstream/master + local commits
git push origin master
```

Then cut a feature branch from `master`. Prefer branches for feature work;
small doc/test additions may land on `master` directly. Never rewrite pushed
`master` history.

## Contributing back upstream

1. Start from an up-to-date `master` (see above) and create a feature branch.
2. Follow `CONTRIBUTING.md` in full: the one architectural rule (behavior in
   `services/`, routing in `api/routes/`), measuring behavior against the live
   Zotero client or dataserver before changing protocol behavior, updating
   `tests/test_routes.py` inventory and `docs/status.md`, and the commit style
   (one change per commit, message explains why).
3. Push the branch to `origin`, then open the pull request against upstream:

   ```sh
   gh pr create --repo eseifert/altero --base master --head utsmok:<branch>
   ```

4. Upstream review is the gate. Do not merge your own protocol PRs into the
   local `master` and treat them as done — track them until upstream lands
   them.

## Local conventions (this machine)

- Python tooling runs through `uv` only (`uv sync`, `uv run`); never bare
  `python`/`pip`.
- The full suite needs PostgreSQL (`ALTERO_TEST_POSTGRES_URL`, see
  `CONTRIBUTING.md`); without it the concurrency tests skip and CI parity is
  weaker.
- Machine-specific dev notes (Docker on the Windows engine, `tools/dev-e2e.sh`,
  headless Zotero testing) live in `E2E-FINDINGS.md`.
- Scratch/labs live under `/tmp/altero-*` and are disposable; anything worth
  keeping belongs in this repo.
