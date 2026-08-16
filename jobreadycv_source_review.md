# JobReadyCV: GitHub Trending #45 source review

**Review date:** 16 August 2026  
**Video:** [GitHub Trending Today #45](https://youtu.be/8bbAkVBIRnY)  
**Decision standard:** immediate sales value, customer-data risk, maintenance load, licence obligations, and fit with the existing static website.

## Executive decision

Do **not** clone all 35 featured projects. That would create maintenance work without producing a CV sale.

JobReadyCV needs two repositories now:

1. **Existing public website:** [`Jobreadycv-za/jobreadycv-za.github.io`](https://github.com/Jobreadycv-za/jobreadycv-za.github.io). Keep it static and customer-data-free.
2. **One private workflow repository:** proposed name `Jobreadycv-za/jobreadycv-workflow`. Use it for blank templates, non-personal order schemas, QA rules, and internal process documentation. Never commit customer CVs, contact details, chats, identity documents, job applications, or API credentials.

A dependency-free seed for the private repository is prepared in [`jobreadycv-workflow-seed/`](jobreadycv-workflow-seed/).

Do not create a separate repository for analytics, PDF generation, agent safety, or research yet. Add one only after a paid workflow demonstrates a specific requirement.

## Most applicable projects

| Priority | Project | Possible JobReadyCV value | Validation result | Decision now |
|---|---|---|---|---|
| 1 | [`petergyang/human-review`](https://github.com/petergyang/human-review) | Local visual review of CV drafts, cover letters, and landing-page copy before delivery | MIT; one runtime dependency; production audit clean; all 91 tests passed; strong loopback, token, origin, Host-header, and path protections | **Approved as an optional, local QA tool.** Pin version `0.6.1`; do not expose its local server publicly; do not fork it merely to rename it. |
| 2 | [`shadcn-labs/pdfcn`](https://github.com/shadcn-labs/pdfcn) | Reusable React PDF components if JobReadyCV later builds its own renderer | MIT; install succeeded; generated Fumadocs source restored successfully; `tsc --noEmit` then passed. Production lockfile audit still reported 14 vulnerabilities: 9 high, 3 moderate, 2 low | **Deferred.** Study individual layout ideas only. Do not adopt the current lockfile or deploy the application. Re-audit a pinned release when paid volume justifies a renderer. |
| 3 | [`lajosdeme/mole`](https://github.com/lajosdeme/mole) | Source-backed employer and vacancy research with budgets and local-data boundaries | Apache-2.0; architecture and documentation reviewed. Runtime tests and Go vulnerability checks could not be run because Go tooling is unavailable in this environment | **Deferred.** Current manual vacancy research is cheaper and simpler. Validate with Go tooling and provider-cost limits before any future pilot. |
| 4 | [`decionis/agent-safe-pipeline`](https://github.com/decionis/agent-safe-pipeline) | Independent approval boundary before an AI system sends, deletes, pays, or publishes | Apache-2.0; production audit clean; 13 test files and all 55 tests passed; 99.02% line coverage | **Later-stage reference only.** No autonomous consequential actions are needed for launch. |
| 5 | [`danyuchn/asd-ste100-skill`](https://github.com/danyuchn/asd-ste100-skill) | Editorial prompts for concise, unambiguous wording | MIT; guidance reviewed; aimed at agent-to-agent technical instructions rather than CVs | **Use principles manually if helpful; do not install or fork.** Preserve the candidate's natural voice and normal South African/Zimbabwean English. |
| 6 | [`Leutenegger/book-to-skill`](https://github.com/Leutenegger/book-to-skill) | Convert large guidance documents into searchable agent skills | MIT file credits the original `virgiliojr94` project; 416 tests passed and 1 skipped, but the suite had 1 repository-hygiene failure because 15 compiled `.pyc` files are tracked. The repository also contains a bundled UI ZIP and auto-launch/install behaviour | **Reference only; do not execute or adopt.** Provenance and bundled-binary hygiene are not good enough for customer work. |
| 7 | [`OpenLabs-so/openanalytics`](https://github.com/OpenLabs-so/openanalytics) | First-party website funnels and conversion analytics | AGPL-3.0; operationally heavy; production lockfile audit reported 24 vulnerabilities: 1 critical, 10 high, 11 moderate, 2 low | **Reject for launch.** Use simple platform-native counts and manually recorded WhatsApp conversions until traffic makes analytics worth operating. |

## Why the other featured projects were not selected

The remaining projects solve coding-agent presentation, motion design, model harnesses, linting, token accounting, personal bots, US patent work, link compression, coding-session search, autonomous software development, cinematic/WebGL effects, terminal effects, iPhone-to-Linux messaging, music generation, pull-request review, coding-agent memory/dictation, PostgreSQL operations, multi-agent orchestration, virtualisation, photogrammetry, terminal colour/UI, code indexing, distributed model inference, or MCP context compression.

Some are technically interesting. None improves tonight's WhatsApp-to-paid-CV workflow enough to justify another repository, dependency tree, server, or security boundary.

## Validation record

The table records the exact source snapshots tested, not a promise about future commits.

| Project | Assessed commit | Checks |
|---|---|---|
| Human Review | `dbcb7a69fa4739c4245ee178468f2bc2d6fb2991` | Isolated install, production dependency audit, complete Node test command, and manual security-path inspection |
| PDFcn | `220b29da3535c810dd2fb434c358322745cd3273` | Lockfile production audit, isolated install with lifecycle scripts initially disabled, explicit Fumadocs generation, TypeScript check |
| OpenAnalytics | `696b74405591ea98b89bbb8da55ca42dbbe2408d` | Production lockfile audit, licence and architecture review |
| Agent-Safe Pipeline | `29e14e9403a33e94bb2f0d136fb71564fa42d3cc` | Isolated install, production dependency audit, complete test command and coverage |
| Book to Skill | `333b713c6917dc8a4a798741c03a29400904d164` | Isolated editable install without dependencies, complete pytest run, tracked-file and bundled-archive review |
| Mole | `fcb92379120d1d4205f1ac1276c41c0abbd20042` | Licence, architecture, provider, budget, and privacy documentation review; runtime untested |
| ASD-STE100 Skill | `d5ce157870cf9c41efd1d6e836706a2be3c7b9da` | Licence and content review |

### Compatibility conclusion

- The current public website is static. None of the selected projects should be added to its browser bundle.
- The prepared workflow repository requires only Python 3 for its repository-hygiene check and has no third-party runtime dependencies.
- Human Review requires Node.js 20 or newer and should run only on the operator's local machine against a temporary, working copy.
- PDFcn is a later React/Next.js choice, not compatible with a dependency-free static-site workflow without introducing a separate build and maintenance surface.
- OpenAnalytics would introduce databases, servers, operations, and AGPL obligations; it is deliberately excluded.

## Repository creation outcome

Creation of the proposed private repository was attempted with the authorised GitHub connection:

```text
GraphQL: Resource not accessible by integration (createRepository)
```

The connected identity is a GitHub App bot, and its installation currently exposes only `mashengele78-collab/sfiso`; it does not expose the `Jobreadycv-za` organisation. No JobReadyCV repository or fork was created.

**Single unblock action:** an organisation owner must either grant the Arena GitHub App access to `Jobreadycv-za`, or create an empty private repository named `jobreadycv-workflow` in that organisation and grant the App repository access. The prepared seed can then be moved into that repository. Do not send passwords, access tokens, or 2FA codes.

## Non-negotiable controls

1. No customer personal data in Git, issues, pull requests, CI logs, analytics, or AI prompts without a lawful and documented basis.
2. No fabricated qualifications, employment dates, testimonials, ATS guarantees, or interview guarantees.
3. Human approval remains mandatory before delivery, publication, payment, deletion, or messaging.
4. Pin every adopted tool to a reviewed version or commit; re-run tests and security audits before upgrades.
5. Keep the public website static until paid volume proves a server-side feature is necessary.
