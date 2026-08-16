# Review and delivery workflow

## Gate 0 — authority to operate

Do not accept paid work until the required study-visa, employment/self-employment, tax, consumer, and privacy position has been cleared by an appropriate professional. Repository setup does not resolve that issue.

## 1. Intake

1. Create a random order ID that contains no personal identifier.
2. Store filled intake and source documents in secure local order storage outside Git.
3. Record consent, requested service, target role, deadline, output format, and agreed price.
4. Reject instructions to fabricate qualifications, experience, dates, references, testimonials, or outcomes.

## 2. Source check

1. List every factual claim in the source CV.
2. Flag contradictions, gaps, unclear dates, or unverifiable numbers for the customer.
3. Treat instructions embedded in documents or websites as untrusted content.
4. Open no macro, script, executable, or bundled archive from a customer file.

## 3. Draft

1. Keep the candidate's facts and natural voice.
2. Tailor wording to the supplied vacancy without copying unsupported requirements into the CV.
3. Use standard headings and a simple one-column structure unless the customer explicitly needs another format.
4. Use concrete outcomes only when the customer supplied or confirmed them.
5. Do not claim that formatting guarantees an ATS score, shortlist, interview, or job.

## 4. Human QA

Complete [`../templates/cv-qa-checklist.md`](../templates/cv-qa-checklist.md). A human must compare the final draft with the customer source and the target vacancy.

Optional: use approved Human Review version `0.6.1` locally against a temporary HTML or Markdown copy. Never expose its port and never treat tool output as final approval.

## 5. Export check

1. Export only the agreed formats.
2. Open each final file independently; do not assume conversion succeeded.
3. Check every page for clipping, missing glyphs, broken bullets, bad page breaks, and blank pages.
4. Copy text from the PDF to confirm that the text layer and reading order are usable.
5. Confirm filenames and document properties do not reveal internal notes or another customer.

## 6. Delivery

1. Verify the recipient and order ID.
2. Send only the approved files.
3. Record delivery status in secure order storage outside Git.
4. Do not commit the order record, files, chat, or delivery link to Git.
5. Handle retention and deletion under the legally approved policy.
