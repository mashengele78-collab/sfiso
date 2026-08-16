# Technology decisions

## ADR-001: one private workflow repository

**Status:** accepted, 16 August 2026

Keep the existing public static website. Add one private repository for blank templates, non-personal schemas, QA, and process documents. Do not split launch operations into multiple repositories.

Reason: one small repository reduces access-control mistakes, dependency maintenance, and work that does not lead to paid delivery.

## ADR-002: no customer data in Git

**Status:** accepted

Raw CVs, filled intake, chats, payment records, real order IDs, order-level status/QA records, and generated deliveries remain outside Git. Only blank schemas, synthetic examples, and non-identifying aggregates belong here.

Reason: Git history is durable, replicated, and difficult to erase reliably. A random identifier linked to a customer elsewhere is pseudonymous, not anonymous.

## ADR-003: Human Review is optional local QA

**Status:** accepted with controls

Version `0.6.1` may be used on loopback for temporary HTML/Markdown working copies. It is not a website dependency and is not authorised to publish or deliver output.

Validation at assessed commit `dbcb7a69fa4739c4245ee178468f2bc2d6fb2991`: zero production-audit findings; all 91 tests passed; loopback, token, origin, Host-header, and path protections reviewed.

## ADR-004: defer a custom PDF renderer

**Status:** deferred

PDFcn is not adopted. At assessed commit `220b29da3535c810dd2fb434c358322745cd3273`, generated source and TypeScript checking worked, but the production lockfile audit reported 14 vulnerabilities (9 high, 3 moderate, 2 low).

Reconsider only when paid volume shows that current document production is the bottleneck. Start from a fresh pinned release and re-run licence, audit, type, rendering, accessibility, and malicious-input tests.

## ADR-005: reject self-hosted OpenAnalytics for launch

**Status:** rejected for launch

At assessed commit `696b74405591ea98b89bbb8da55ca42dbbe2408d`, its production lockfile audit reported 24 vulnerabilities, including 1 critical. It also adds AGPL-3.0 obligations and substantial server/database operations.

Use manually recorded, non-personal funnel counts until traffic proves the need for analytics.

## ADR-006: consequential automation requires a separate approval boundary

**Status:** future guardrail

Do not automate sending, publishing, payment, deletion, or document delivery now. If that changes, evaluate an independent authorisation pattern such as Agent-Safe Pipeline rather than letting an agent approve itself.
