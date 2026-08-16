# Data handling rules

## Repository rule

Git stores history and replicates it. Therefore, this repository is a **zero-customer-data zone**.

Allowed:

- blank templates;
- synthetic examples that cannot be mistaken for real people;
- blank schemas that describe records stored outside Git;
- aggregate business counts that cannot identify a person.

Prohibited:

- real order IDs, order-level status records, names, initials linked to an order, phone numbers, emails, addresses, dates of birth, identity/passport/student numbers;
- CV content, employment history, education records, references, photos, signatures, job applications, or interview notes;
- WhatsApp messages, voice notes, screenshots, analytics identifiers, payment proof, bank details, or transaction references;
- customer PDF/DOCX files or final deliveries;
- API keys, passwords, cookies, access tokens, private keys, or recovery codes.

## Local order folders

Filled intake and customer documents must live in an access-controlled local folder outside the Git checkout. Use a random identifier such as `JRCV-20260816-A7K4Q9`; never use a customer name or phone number in a file or folder name.

Recommended separation:

```text
secure-order-storage/
  JRCV-20260816-A7K4Q9/
    source/
    working/
    delivery/
    consent/
```

This structure is illustrative. The actual storage, backup, access, retention, and secure-deletion process must be legally approved before paid processing begins.

## AI and third parties

- Do not paste identifying customer data into a model merely because it is convenient.
- Minimise data first; replace contact details and identity fields with placeholders when the task does not require them.
- Record which provider received which data, for what purpose, and under which approved terms.
- Do not use customer material to train, benchmark, market, or build a portfolio without separate, explicit permission and a lawful basis.
- Never upload customer files to an unreviewed GitHub project, online ATS checker, converter, analytics service, or browser extension.

## Delivery and deletion

Verify the recipient and output files before delivery. Do not promise a retention period until it is operationally and legally approved. Honour valid access, correction, and deletion requests through the approved process.
