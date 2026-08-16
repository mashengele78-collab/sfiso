# JobReadyCV Workflow

Private operating material for JobReadyCV: blank templates, non-personal schemas, quality checks, and process documentation.

## What this repository is for

- standardising intake and manual CV review;
- defining workflow-state records that are kept in secure order storage outside Git;
- preventing factual invention and unsupported claims;
- keeping customer files outside Git;
- documenting future technology decisions before code is added.

## What this repository is not for

Never commit customer CVs, names, phone numbers, email addresses, physical addresses, identity or passport numbers, WhatsApp exports, payment records, application histories, employer correspondence, generated customer documents, or credentials.

The ignore rules are a backup control, not permission to put personal data in the repository.

## Start here

1. Read [`DATA_HANDLING.md`](DATA_HANDLING.md) and [`SECURITY.md`](SECURITY.md).
2. Follow [`docs/review-workflow.md`](docs/review-workflow.md).
3. Copy [`templates/intake-questionnaire.md`](templates/intake-questionnaire.md) into a secure local order folder **outside this repository**. Do not fill it in here.
4. Use [`templates/cv-qa-checklist.md`](templates/cv-qa-checklist.md) before delivery.
5. If a machine-readable order record is needed, create it in secure order storage outside Git using [`schemas/order-manifest.schema.json`](schemas/order-manifest.schema.json). The included example is synthetic only.
6. Run `python3 scripts/repo_check.py` before pushing.

## Optional Human Review tool

[`human-review`](https://github.com/petergyang/human-review) version `0.6.1` passed the JobReadyCV source review. It may be used locally to review a temporary HTML or Markdown draft.

Rules:

- use Node.js 20 or newer;
- pin exactly `human-review@0.6.1` until a newer version is separately reviewed;
- bind only to loopback; never publish the review port;
- review a temporary working copy, not an original customer file;
- close the process and remove temporary files after review;
- do not add it as a website dependency.

It is optional. The core workflow has no third-party runtime dependency.

## Repository status

This directory is a seed prepared on 16 August 2026. The intended private GitHub repository is `Jobreadycv-za/jobreadycv-workflow`. Creation is blocked until the GitHub App receives access to that organisation or an organisation owner creates the empty private repository and grants access.

No open-source licence is granted for original JobReadyCV material in this private repository.
