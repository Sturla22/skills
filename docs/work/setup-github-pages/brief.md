# Product Brief

## Storage

- Work ID: setup-github-pages
- File path: `docs/work/setup-github-pages/brief.md`

## Request summary

Set up a GitHub Pages site for the `sturla22/skills` repo, served directly from the `main` branch `/docs` folder with no build step. Use the existing `docs/operating-model-guide/index.html` as the primary deep-dive page; add a new `docs/index.html` landing page and a `docs/.nojekyll` file.

## Problem / desired outcome

The repo has no public web presence. Content lives only in GitHub's raw markdown view, which is hard to share and discover. The desired outcome is a live `https://sturla22.github.io/skills/` URL that gives visitors a styled landing page and a link into the existing Operating Model Guide HTML page — with no CI pipeline or build tooling required.

## Why this matters

The repo is a public starter kit aimed at firmware teams adopting AI-assisted workflows. A polished web landing page makes it easier to share, reference, and evaluate. The `docs/operating-model-guide/index.html` already exists and is high-quality; this work surfaces it.

## Code drivers

- User scenarios — lets repo visitors access documentation via a public URL rather than navigating raw GitHub markdown
- Design intent communication — reinforces that this is a finished, shareable product rather than an internal scratch repo

## Code drivers

Which of the following justify this work?

- User scenarios — enables or improves a real actor workflow
- Risk — addresses a known failure mode, safety, security, or reliability concern
- Epistemic uncertainty — a spike or prototype to reduce unknowns before committing to a design
- Design intent communication — types, assertions, structure, or naming chosen to make intent explicit for future maintainers
- External obligation — regulatory, certification, or standards mandate

Code traceable to none of these is a candidate for removal, not refinement.

## Stakeholders / users

- **Repo owner (Sturla)** — wants a public URL to share
- **Prospective adopters** — firmware engineers or teams evaluating the starter kit
- **Existing users** — want a stable URL reference for the operating model

## Stakeholder needs / system outcomes

1. A live, visually polished landing page at `https://sturla22.github.io/skills/`
2. The existing Operating Model Guide accessible as a sub-page, unchanged
3. Zero ongoing build or deploy maintenance burden (pure static HTML from main branch)

## Stakeholder needs / system outcomes

## Design criteria / key parameters

- Match the dark GitHub-like visual style already established in `docs/operating-model-guide/index.html` (CSS variables: `--bg: #0d1117`, accent `#58a6ff`)
- No JavaScript frameworks; vanilla HTML/CSS only
- No build step; GitHub Pages serves static files directly from `/docs` on main
- `docs/.nojekyll` must be present to prevent Jekyll from processing HTML files
- Landing page must link to the Operating Model Guide and to the GitHub repo itself
- Landing page should give a concise description of what the repo is and who it is for

## In scope

- `docs/index.html` — new landing page (styled, links to operating model guide and repo)
- `docs/.nojekyll` — suppresses Jekyll processing
- Updating `CHANGELOG.md` with an `Unreleased` entry (minor addition, no contract change)
- Instructions in the PR / commit for the repo owner to enable Pages in GitHub Settings

## Out of scope

- Modifying `docs/operating-model-guide/index.html`
- Setting up a CI/CD pipeline or GitHub Actions workflow for Pages
- Full MkDocs / Jekyll / Docusaurus site rendering of all markdown files
- Custom domain configuration
- Rendering the `docs/templates/` or `docs/work/` directories as web pages

## Out of scope

## Constraints

- Must work with zero build tooling — pure static HTML/CSS served by GitHub Pages
- Must not modify the existing `docs/operating-model-guide/index.html`
- Must be committed to branch `claude/setup-github-pages-fhap0` and pushed
- The GitHub Pages setting (Settings → Pages → Source) must be enabled by the repo owner manually after merge; this work provides the files, not the setting activation

## Commit and PR title policy

- No Jira ticket IDs
- Conventional Commit style: `feat(docs): add GitHub Pages landing page`

## Existing conventions to preserve

- Pitchfork layout: new files go under `docs/`; no new top-level directories
- CHANGELOG.md `Unreleased` section with Keep a Changelog headings
- Branch: `claude/setup-github-pages-fhap0`

## Commit and PR title policy

- Should Jira ticket IDs prefix commit messages?
- Should Jira ticket IDs prefix PR titles?

## Existing conventions to preserve

- Existing issue tracker, commit, or PR conventions:
- Existing release or branching process:
- Existing docs, ADR, or architecture layout:
- Existing build, test, and CI expectations:
- Existing agent, instruction, or automation files:

## System context / external interfaces

- GitHub Pages serves static files from the `/docs` folder of the `main` branch at `https://sturla22.github.io/skills/`
- Existing file: `docs/operating-model-guide/index.html` (must remain unmodified and reachable at `/skills/operating-model-guide/`)
- Existing file: `docs/presentations/ai_sessions.html` (already in `/docs`, reachable at `/skills/presentations/ai_sessions.html`)

## Acceptance criteria

- `docs/index.html` exists, is valid HTML5, and opens correctly in a browser (manual check)
- `docs/.nojekyll` exists (empty file is fine)
- `docs/index.html` visually matches the dark theme of `docs/operating-model-guide/index.html`
- `docs/index.html` contains a working relative link to `operating-model-guide/` 
- `docs/index.html` contains a link to `https://github.com/sturla22/skills`
- `docs/operating-model-guide/index.html` is unmodified (git diff shows no changes to it)
- `CHANGELOG.md` has an `Unreleased` entry noting the Pages landing page
- Changes are committed and pushed to `claude/setup-github-pages-fhap0`

## Delivery class

Non-productized tool (static documentation site). TDD is not required; manual visual verification of HTML is the acceptance gate.

## TDD expectation

TDD skipped — static HTML/CSS with no logic. Verification is opening the file in a browser and confirming visual correctness and link validity.

## Validation intent / evidence

Manual: open `docs/index.html` locally in a browser, confirm styling, links, and content. The operating model guide link must navigate to `docs/operating-model-guide/index.html`.

## SemVer / changelog expectation

MINOR addition (new user-visible docs surface). Add to `Unreleased → Added` in `CHANGELOG.md`.

## Assumptions

- GitHub Pages will be enabled on the `main` branch `/docs` source by the repo owner after this PR merges
- The existing `docs/operating-model-guide/index.html` needs no changes
- `docs/.nojekyll` is sufficient to prevent Jekyll interference (no `_config.yml` needed)

## Open questions

None — scope is fully defined.

## Recommended next owner(s)

`developer` — implement `docs/index.html` and `docs/.nojekyll`, update `CHANGELOG.md`, commit and push.

## Parallelization notes

Single lane; no parallel work needed.

## Delegation notes

Delegate to `developer`. One commit is sufficient (or two if CHANGELOG is logically separate). Push to `claude/setup-github-pages-fhap0`.

## Measures of effectiveness / performance

## Behavior rules / examples (BDD)

## Behavior scenarios (BDD)

## Derived requirements / traceability notes

## Public contract / compatibility impact

## Delivery class

## TDD expectation

## Validation intent / evidence

## SemVer / changelog expectation

## Assumptions

## Open questions

## Recommended next owner(s)

## Parallelization notes

## Delegation notes
