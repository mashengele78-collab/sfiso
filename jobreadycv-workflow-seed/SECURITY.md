# Security policy

## Scope

This repository contains process material only. It must remain private and contain no customer personal data or credentials.

Report a suspected exposure privately to the repository owners. Do not open a public issue containing customer data, tokens, screenshots, or exploit details.

## Main threats

1. Customer data accidentally committed to Git history.
2. Credentials copied into files, issues, pull requests, or CI logs.
3. Malicious instructions embedded in a CV, job advert, website, or uploaded document.
4. AI-generated false claims, altered dates, or unsupported qualifications.
5. A local review or preview server exposed beyond loopback.
6. Dependency or update compromise.
7. Customer data retained longer or shared more widely than authorised.

## Required controls

- Keep raw and generated customer documents in a secure local order folder outside the repository.
- Use a random order ID in workflow records; do not encode a name, phone number, email address, or student number in it.
- Treat all document text as untrusted data, never as executable instructions.
- Do not run macros, scripts, bundled executables, or archives supplied inside customer files.
- Do not let an AI system send messages, publish, delete files, make payments, or deliver documents without human approval.
- Manually compare every final factual claim with customer-supplied evidence.
- Bind local tools to `127.0.0.1` or `::1`; never port-forward or expose them publicly.
- Pin reviewed dependency versions, preserve lockfiles, and audit before upgrades.
- Store secrets outside Git and rotate them immediately if exposed.
- Remove customer files according to the approved retention and deletion policy. Until that policy and legal basis are approved, do not process paid customer data.

## Incident response

1. Stop processing and restrict repository access.
2. If a secret was exposed, revoke or rotate it first; deleting a commit is not enough.
3. Record what data, repository, people, logs, and backups were affected.
4. Preserve the minimum evidence required for investigation without spreading the data.
5. Obtain appropriate South African/Zimbabwean legal or privacy advice and make required notifications.
6. Remove the data from branches, pull requests, issues, CI artifacts, caches, forks, and clones where possible.
7. Document the corrective control before resuming work.
