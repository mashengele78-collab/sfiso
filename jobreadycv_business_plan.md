# A. Access report

**Audit date:** 15 August 2026 (Africa/Harare time).  
**Known operating facts:** the owner is a Zimbabwean student in Stellenbosch on a South African study visa, has no paid clients or testimonials yet, and has 13–20 hours available per week.

## 1. What was accessible

| Asset | Access achieved | What could be inspected | What remains invisible |
|---|---|---|---|
| YouTube `KfeLAVrkX9Y` | Full page and full transcript | All spoken lessons in the 3:09 video | Nothing material for this task |
| YouTube `RmwI_QqcPQc` | Full page and full transcript | All spoken lessons in the 12:05 video | Nothing material for this task |
| Instagram `@jobreadycv_za` | Instagram itself returned HTTP 403, but the current public profile and post pages were exposed through Imginn | Display name, handle, avatar thumbnail, one seven-slide carousel, one 36-second reel, captions, hashtags, dates, visible likes/comments, and absence of currently exposed Stories | Bio, link, follower/following counts, account Insights, profile visits, reach, saves, shares, reel plays/watch time, audience geography, DMs, audio and frame-by-frame reel content. The mirror outputs `undefined` where profile metadata would normally appear, so the bio cannot be verified. |
| TikTok `@boschbanter` | Not successfully accessed | Only the handle supplied by the owner can be assessed | Profile existence/status, display name, bio, link, followers, following, likes, videos, views, comments, shares, content topics and analytics are all unverified |
| `JobReadyCV.za` domain | DNS checked independently | `jobreadycv.za`, `www.jobreadycv.za`, `jobreadycv.co.za` and `jobreadycv.co.zw` did not resolve when checked | Registration ownership and future availability were not established |

## 2. Instagram facts actually observed

1. Display name: **Jobreadycv.za**.
2. Handle: **@jobreadycv_za**.
3. Two exposed items, both posted 13 August 2026:
   - A seven-slide service-introduction carousel: **3 visible likes, 0 comments**.
   - A 36-second reel: **1 visible like, 0 comments**. Plays were not exposed.
4. The carousel says the service offers CV writing, cover letters, LinkedIn profiles and career guidance. It targets students, graduates, job seekers and career changers, says “Across South Africa,” and ends with a DM CTA.
5. The carousel includes an “ATS-friendly” claim, but no method, example, price, turnaround, process, human identity or evidence supporting the claim.
6. The mirror exposed no current Stories.

Observed pages:
- Profile: <https://imginn.com/jobreadycv_za/>
- Carousel: <https://imginn.com/p/Db-LphBjIU6/>
- Reel: <https://imginn.com/p/Db-MTXPMXNF/>

## 3. TikTok access attempts and conclusion

TikTok’s profile, embed, search and related public endpoints returned HTTP 403 from this environment. Search engines had no indexed result for the exact handle. Countik returned blank/undefined data; Urlebird reported that the profile could not be found; Dumpor stopped at Cloudflare verification; TikVib returned 404; and other public viewer URL patterns produced no profile. These failures do **not** prove that the account does not exist. They mean no content or metric should be invented.

**The one definitive audit finding is that `@boschbanter` is off-brand for a CV business.** “Bosch banter” signals Stellenbosch humour, commentary or campus entertainment. It does not signal CV writing and it breaks recognition with `@jobreadycv_za`.

## 4. Material access warning

`JobReadyCV.za` currently reads like a live web address, but it did not resolve. That is a trust risk if it appears on posts or logos. Until a working domain is registered and connected, treat **JobReadyCV** as the brand name—not as a website—and use a direct WhatsApp Business link.

# B. Key lessons from each video

## 1. Video 1 — “How to Start Resume Writing Service Business”

Source: <https://www.youtube.com/watch?v=KfeLAVrkX9Y>

### What the video actually teaches

1. **Writing quality is the product.** A resume writer needs error-free writing and research ability.
2. **Students close to graduation or internships are a practical target market.** The video specifically identifies college students as prospects.
3. **The startup equipment is basic.** A computer, internet presence and writing/software tools are sufficient; it is not a capital-heavy business.
4. **Start as a freelancer, then market the service.** Delivery capability comes before trying to look like a large agency.
5. **Create a longer-term plan and a social strategy.** The speaker recommends planning roughly two years ahead rather than operating randomly.
6. **A CV needs deliberate structure.** The video mentions formatting, strategic ordering, career objective, education, skills, experience, work history, career path and a future view.
7. **Word of mouth is central.** Satisfied clients and personal recommendations are presented as the main growth mechanism.

### Business actions for JobReadyCV

1. Use a **two-pass quality-control system** before every delivery:
   - Pass 1: facts, dates, job-title consistency, chronology, truthful claims and vacancy keywords.
   - Pass 2: spelling, grammar, punctuation, formatting, links, filenames and PDF text selection.
2. Narrow the first market to **students, recent graduates and early-career applicants applying to internships, graduate programmes and entry-level roles**. Do not launch as a general “career guidance” service for everyone.
3. Spend nothing on an office and do not wait for a website. Start with WhatsApp Business, Google Forms, Google Drive/Docs, Word mobile/desktop and a simple spreadsheet.
4. Build one honest sample CV and one before/after example before asking strangers to pay. Mark fictional or composite samples clearly; never present them as client work.
5. Put a referral request into the delivery workflow. Do not hope that word of mouth happens by itself.
6. Keep one operating sheet for the next 90 days: lead source, inquiry, quote, payment, deadline, package, time spent, review and referral.

### What the video does **not** cover

The video does not explain ATS parsing rules, job-description keyword analysis, quantified achievement bullets, page-length decisions, pricing, deposits, revisions, client intake, privacy, ethical use of AI, proof-building, lead conversion, local payment methods or South African/Zimbabwean market conditions. “Career objective” and “future view” are not universal requirements; use a short professional summary only when it helps the target application. The video is a basic business overview, not a complete CV-writing method.

## 2. Video 2 — “How To Market Your Business On Social Media”

Source: <https://www.youtube.com/watch?v=RmwI_QqcPQc>

### What the video actually teaches

1. **Every post needs a commercial job:** generate leads, nurture leads or convert leads.
2. **Content must be reverse-engineered from the offer.** Start with what is being sold and the buyer’s problem, not with a random trend.
3. **Testing must be intentional.** Publish with a hypothesis and measure the response instead of posting for activity’s sake.
4. **Branding should be consistent and memorable.** Repetition helps recognition.
5. **Keep an inventory of stories.** Real situations and transformation stories are more memorable than isolated facts.
6. **Stories outperform unsupported information.** A specific applicant problem and correction is stronger than “five CV tips” with no context.
7. **Every video needs a next step.** A viewer should know exactly what to do after watching.
8. **Content should build know, like and trust.** Trust is necessary before a buyer sends personal documents or money.
9. **Use roughly 80% value and 20% direct CTA content.** Most posts should help; a minority should explicitly sell.

### Business actions for JobReadyCV

1. Label every planned post **G, N or C**:
   - **G — Generate:** attract a relevant applicant, e.g. “Three errors in this Stellenbosch internship CV.”
   - **N — Nurture:** demonstrate the process, e.g. an anonymised before/after bullet.
   - **C — Convert:** state the package, price, turnaround and WhatsApp CTA.
2. Reverse-engineer content from the initial offer: **job-specific, ATS-safe application documents for early-career roles**. Content should therefore focus on actual vacancies, weak bullets, keywords, simple formatting and first-job evidence—not broad inspiration.
3. Use one test per post. Example: “A vacancy-breakdown reel with CTA `WhatsApp TARGET` should produce two qualified chats from 500 relevant views.” Track chats, not just views.
4. Use the same name, colours, profile image, promise and CTA on Instagram, TikTok and WhatsApp. Do not split attention between “JR,” “Jobreadycv.za” and “Bosch Banter.”
5. Start a phone note called **Story Bank** with:
   - a mistake found in a public job advert/application process;
   - a fictional sample transformed step by step;
   - a beta client’s problem, process and honest result, with written permission;
   - the owner’s own application-document lesson;
   - a question repeatedly asked in DMs.
6. End each post with one action, not three: “WhatsApp `TARGET` with the vacancy link for the package list.”
7. Use proof that exists before testimonials exist: a visible checklist, a sample transformation, process transparency, clear terms and the owner’s face/name if comfortable. Do not fake social proof.

### What the video does **not** cover

It does not provide prices, outbound sales mechanics, paid-ad economics, referral design, retainer/retention tactics, analytics thresholds, local platforms, WhatsApp selling, EcoCash or study-visa compliance. The 80/20 ratio is a guideline, not a guarantee. With a new account and four total visible likes, social content alone is unlikely to produce fast sales; direct, permission-based outreach must do the early acquisition work.

## 3. Supplemental ATS guidance — not taught in either video

This is separate evidence-based operating guidance, not a claim about the videos.

1. Use a single-column layout with standard headings such as **Professional Summary, Education, Experience, Projects and Skills**.
2. Avoid tables, text boxes, columns, icons, charts, profile photos and critical contact details in headers/footers.
3. Use a normal font, consistent dates and simple bullets. Put the most relevant recent information first, usually in reverse chronology.
4. Tailor wording to the supplied vacancy, using truthful job-description keywords in context. Never keyword-stuff or use hidden white text.
5. Write achievement/evidence bullets where facts allow: **action + task/context + result/scale**. Do not invent percentages or responsibilities.
6. Deliver an editable DOCX and a text-selectable PDF; follow the employer’s requested file type. Test the PDF by copying its text into a plain-text note and checking the order.
7. Do not add ID/passport numbers, date of birth, marital status, full street address or a photo unless an application specifically and legitimately requires it.

References:
- University of Virginia ATS guidance: <https://career.virginia.edu/Students/Prepare/Resumes/NavigatingATS>
- Columbia ATS guidance: <https://www.careereducation.columbia.edu/resources/optimizing-your-resume-applicant-tracking-systems>
- Harvard resume guidance: <https://careerservices.fas.harvard.edu/resources/create-a-strong-resume/>

# C. Social media audit

## 1. Instagram `@jobreadycv_za`

### Scorecard based only on visible evidence

| Area | Finding | Commercial effect | Immediate correction |
|---|---|---|---|
| Brand name | Handle is aligned to JobReadyCV, but the display name uses `Jobreadycv.za`, the slides use both “JR” and JobReadyCV, and the claimed `.za` address does not resolve | Mixed naming and a dead-looking web address reduce trust | Standardise to **JobReadyCV**. Use “JobReadyCV — CV Writer SA + ZW” in the searchable name field. Remove website-style `.za` from graphics until it works. |
| Audience | Students, graduates, job seekers and career changers “across South Africa” is too broad; Zimbabwe is absent | The account does not tell a specific buyer “this is for me” | Lead with students/recent graduates applying for internships, graduate programmes and entry-level roles in SA and Zimbabwe |
| Offer | Four broad services are listed, including vague “career guidance”; no package, scope, price or turnaround is visible | A prospect cannot compare value or decide quickly | Pin a price/process post with three packages and 48–72-hour turnaround |
| CTA | “Send us a DM” / “DM us to get started” | High friction and no reason to act now; no information about what to send | Use one tracked CTA: **“WhatsApp `TARGET` with the vacancy link and your deadline.”** |
| Content | One seven-slide introduction carousel and one short reel; the carousel is service-led rather than problem/proof-led | There is not enough useful content to establish expertise | Publish vacancy breakdowns, ATS corrections, before/after bullets and a visible QA process |
| Trust | No visible human identity, process, sample, terms, price or client proof | Sending a CV means sharing sensitive information; an anonymous new page is a hard sell | Add owner introduction, confidentiality statement, sample work and plain-language terms |
| Proof | No paid clients or testimonials; none are visibly claimed | Zero proof is normal at launch but must be handled honestly | Use clearly labelled sample work and obtain honest beta reviews; do not manufacture testimonials |
| Copy quality | Caption uses “Linkedin,” “isnt” and “lets”; the reel uses the awkward line “Get your CVs tailored and worked on with us”; hashtag `#cvprofesional` is misspelled | Errors are unusually damaging because proofreading is the product | Proofread every caption with the same two-pass QA used for client work; use “LinkedIn,” “isn’t,” “let’s,” “professional” |
| Engagement | Carousel: 3 likes/0 comments; reel: 1 like/0 comments; only two days of visible history | There is no evidence of a responsive audience yet | Do not use follower growth as the month-one strategy; use outbound conversations and measure qualified chats |
| Local fit | `#southafrica` appears, but no Stellenbosch, SU network, Zimbabwe, WhatsApp or payment context appears | The strongest differentiation is unused | Add SA/ZW positioning and vacancy-specific local examples |

### Strengths

1. The account has launched rather than remaining an idea.
2. The Instagram handle is close to the intended brand.
3. The first carousel clearly lists the service categories and includes an ATS-friendly claim.
4. Both carousel and reel formats have been attempted.
5. There is a basic next step—DM—even though it needs improvement.

### Weaknesses that matter most

1. **The copy errors undermine the core promise.** A CV-writing account cannot be casual about proofreading.
2. **There is no concrete offer.** No visible price, turnaround, deliverable, revision rule or process.
3. **The market is too broad.** “Students, graduates, job seekers and career changers” is nearly everyone.
4. **There is no trust bridge.** The buyer cannot see who handles the document, how data is protected or what quality looks like.
5. **The CTA is generic.** “Send a DM” does not qualify the lead or move the person to a sale.
6. **The brand implies a website that does not exist.** This should be corrected immediately.
7. **No content yet gives a prospect a reason to save, share or believe.** The introduction carousel describes the seller rather than solving a buyer’s immediate problem.

### Profile replacement to implement tonight

**Searchable name field**  
`JobReadyCV | CV Writer SA + ZW`

**Bio**  
`ATS-safe CVs for internships & entry-level roles`  
`SA + Zimbabwe | 48–72h | From R399 / US$20`  
`WhatsApp TARGET + your vacancy ↓`

If the first-five beta offer is still open, temporarily change the second line to:  
`5 beta slots: R299 / US$15 | 48–72h`

**Link**  
Use `https://wa.me/[full-number-with-country-code]?text=Hi%20JobReadyCV%2C%20TARGET.%20I%20am%20applying%20for%3A%20` after replacing the bracketed number. Do not publish a fake or incomplete link.

**Three pinned posts**
1. **Start here:** exact buyer, three packages, turnaround, revision and CTA.
2. **Sample before/after:** clearly fictional or anonymised with permission; explain each change.
3. **How it works:** intake → payment → draft → one revision → DOCX/PDF, plus confidentiality and no interview guarantee.

**Highlights once Stories are available**  
`Start` · `Prices` · `Samples` · `Process` · `Reviews` · `FAQ`

## 2. TikTok `@boschbanter`

### Direct verdict

**It is off-brand.** Do not build JobReadyCV under that name merely because the account already exists.

### Decision rule

1. If `@boschbanter` has **little or no relevant audience**, rename it to `@jobreadycv_za`, `@jobreadycvsa` or the closest consistent available handle. Change display name, avatar, bio and link at the same time.
2. If it has a **meaningful but unrelated campus/entertainment audience**, keep it separate. Create a dedicated JobReadyCV account. One crossover announcement is acceptable; repeated promotion to an irrelevant audience is not.
3. If the existing content is controversial, private or inconsistent with professional trust, do not repurpose it even if the follower count looks attractive.

No valid statement can be made yet about its audience, CTA, content, trust, proof or engagement because the profile itself was not visible. The screenshots requested in section J are required for that part of the audit.

## 3. Content standard for both platforms

Before publishing, every post must pass five checks:

1. **Buyer:** Is it specifically useful to an internship, graduate-programme or entry-level applicant?
2. **Evidence:** Is the advice demonstrated with a vacancy, sample, checklist or real permitted story?
3. **Accuracy:** Is every word proofread and every claim supportable?
4. **Job:** Is the post Generate, Nurture or Convert?
5. **Next action:** Is there one CTA that can be measured?

# D. Positioning and offer

## 1. Compliance gate before revenue

**Do not accept payment, invoice a client or promise paid delivery until written guidance confirms that self-employed/freelance CV writing is permitted by the owner’s exact South African study-visa endorsement.**

The official Immigration Regulations say a qualifying study-visa holder may conduct part-time work for no more than 20 hours per week. That wording does not settle whether operating a business or freelance service counts as permitted part-time work. VFS also currently states that study-permit holders may not work during academic vacations. Client location and payment currency do not remove the issue: work performed from Stellenbosch may still be work in South Africa.

Use this email:

> **Subject: Written clarification—freelance/self-employed work on my study visa**  
> I am a Zimbabwean citizen registered as a full-time student at Stellenbosch University and hold a valid South African study visa. My visa/endorsement states: “[copy the wording exactly].” I am considering providing CV-writing services on a freelance/self-employed basis from South Africa for no more than [13/20] hours per week, to clients in South Africa and Zimbabwe. Would this activity be permitted under my current visa, including during university vacations? If not, what permission or visa status would be required? Please confirm in writing and advise whether CIPC/SARS or any other registration is required.

Send it to Stellenbosch University International and obtain advice from Home Affairs/VFS or a qualified South African immigration professional. Keep the written response. Ask separately about SARS/CIPC and cross-border payment obligations; immigration permission and tax/business compliance are different questions.

Until the answer arrives, the sprint can build profiles, samples, systems and an interest waitlist. Do not take a deposit “to hold a place.” Even unpaid client work may have legal implications, so use fictional/composite portfolio samples rather than servicing real clients until clarified.

Official references:
- Immigration Regulations, Regulation 12(3): <https://www.dha.gov.za/images/PDFs/ImmigrationRegulations2014-Updated2018-compressed.pdf>
- VFS South Africa study-visa information: <https://visa.vfsglobal.com/one-pager/dha/southafrica/english/index.html>
- SU International study-visa FAQ: <https://www0.sun.ac.za/international/frequently-asked-questions-1/study-visa.html>

## 2. Positioning

**One-line positioning**

> JobReadyCV creates job-specific, ATS-safe CVs and application documents for students and early-career applicants targeting internships, graduate programmes and entry-level roles in South Africa and Zimbabwe—delivered through WhatsApp in 48–72 hours.

**Why this is defensible**

1. Stellenbosch University already provides registered students with free CV, cover-letter, interview, LinkedIn and employer-networking support. Competing as “general career help for students” is weak.
2. JobReadyCV should instead sell **speed, after-hours WhatsApp convenience, vacancy-specific tailoring, clear deliverables and SA/ZW context**.
3. The owner’s strongest early network is the intersection of Zimbabwean and Stellenbosch student contacts. That can generate conversations faster than broad social posting.

SU service reference: <http://www.sun.ac.za/english/learning-teaching/student-affairs/cscd/career-services/students>

## 3. Geographic order

1. **First: warm Stellenbosch/Zimbabwean student intersection.** Friends, classmates, residence contacts, ZIMSOC contacts and referrals can provide the fastest credible first five customers. Ask group administrators before posting.
2. **Second: Zimbabwean graduates and diaspora applicants applying in SA, Zimbabwe or internationally.** The dual-market perspective is more differentiated here. Use Zimbabwean vacancy examples and USD/EcoCash-compatible options only if the owner can lawfully and operationally accept them.
3. **Third: broader South African student/graduate market.** This is larger but more competitive, with free university services and established CV writers.

ZIMSOC has a public SU listing with an email, Instagram and WhatsApp invitation: <http://www.sun.ac.za/english/students/student-societies/nationality-societies/zimsoc>. Do not scrape or mass-message members. Ask the committee for permission and offer one useful workshop/checklist before requesting promotion.

## 4. Initial offer ladder

The ZAR and USD prices are **separate market prices**, not live currency conversions. Quote and collect in one agreed currency; do not change the price after the client accepts.

| Offer | Price | Exact scope | Capacity/terms |
|---|---:|---|---|
| **First-five beta CV** | **R299 / US$15** | Rebuild or improve one CV for one job family or supplied vacancy; DOCX + text-selectable PDF; one revision | Only five total. Ask for honest feedback after delivery; discount is not conditional on a positive review. Remove this offer after five. |
| **CV Reset** | **R399 / US$20** | One ATS-safe CV targeted to one job family; intake; rewrite/format; DOCX + PDF; one revision | 48–72 hours after complete intake and cleared payment |
| **Job-Target Pack** | **R599 / US$30** | CV tailored to one supplied vacancy + one matching cover letter; keyword/evidence alignment; DOCX + PDF; one revision | Best default offer; 48–72 hours |
| **Full Launch** | **R999 / US$55** | Targeted CV + one cover letter + LinkedIn headline/About/experience rewrite + one 30-minute mock interview and written feedback | Maximum two per week; 4–5 working days |

**Add-ons for existing clients only**

| Add-on | Price | Boundary |
|---|---:|---|
| LinkedIn rewrite | R250 / US$15 | Headline, About, key experience and skills text; client updates the account unless a secure screen-share is agreed |
| Extra vacancy-specific cover letter | R150 / US$8 | One supplied vacancy |
| 30-minute mock interview | R300 / US$18 | One role; structured feedback; no hiring guarantee |
| Genuine 24-hour rush | Base package **+50%** | Offer only when capacity and electricity/data allow; not available for Full Launch by default |

Do not launch a cheaper “quick edit.” It invites poorly scoped work and weak margins. Do not sell broad career guidance until the owner can define credentials, method, boundaries and outcome.

**Pricing rationale:** observed South African entry-level CV offers sit roughly around R300–R500, with broader bundles commonly reaching about R400–R1,000. Observed Zimbabwean offers put a CV around US$15–US$30 and a CV/cover-letter/LinkedIn bundle around US$40. The launch prices are therefore accessible, but not so low that several hours of careful work become pointless. They should be tested against actual conversion and time, not treated as permanent.

Reference pages:
- <https://cvbooster.co.za/>
- <https://cvcivets.co.za/>
- <https://www.cvcentre.co.za/cv-writing/for-students-and-graduates>
- <https://www.workinzimbabwe.com/product/professional-cv-writing-service-in-zimbabwe/>
- <https://zimbowriters.co.zw/cv-writing-services-zimbabwe/>

## 5. Standard terms

1. Full payment upfront for CV Reset and Job-Target Pack. Full Launch may be 50% to book and 50% before editable final files only if payment handling is operationally simple; otherwise full payment upfront.
2. Turnaround starts only after payment, completed intake, current CV/information and the target vacancy are received.
3. One consolidated revision is included if requested within seven calendar days. A new target vacancy or major new information is a new scope.
4. Deliver DOCX plus text-selectable PDF. Never deliver only a Canva CV.
5. Never promise a job, interview, ATS “score,” ranking or response rate.
6. Never invent employers, qualifications, dates, duties, metrics or references.
7. Obtain written permission before showing any client material. Remove names, phone numbers, email, addresses, IDs and employer-sensitive information.
8. Collect only necessary personal data. Store it in an access-controlled Drive folder; do not put CVs in public AI tools without explicit informed consent and a suitable privacy process. Set a deletion period, initially 90 days after delivery, and tell the client.
9. Send a one-page scope/terms message before payment so WhatsApp conversations do not become unlimited consulting.
10. Keep paid-service operating time at or below the lower of the owner’s available hours and the legal limit confirmed in writing. Do not “average” excess hours across weeks.

## 6. Sales workflow

1. Lead sends keyword `TARGET`, vacancy link, deadline and current CV status.
2. Send package card and five qualification questions from section H.
3. Recommend one package; do not dump every add-on on the prospect.
4. Send scope, price, turnaround, payment method and no-guarantee statement.
5. After lawful payment: send intake form and create client row/folder.
6. Confirm that all facts belong to the client and request missing evidence.
7. Draft using vacancy-to-evidence mapping; run ATS and proofreading checks.
8. Deliver watermarked/read-only preview only if using split payment; otherwise deliver DOCX/PDF.
9. Receive one consolidated revision list; finalise.
10. After 48 hours, ask for an honest review. After 14 days, ask for a referral. After 30 days, ask for voluntary application/interview feedback.

## 7. Fastest acquisition channels

Ranked by likely time to first sale, not audience size:

1. **Individual warm WhatsApp messages.** Start with people who know the owner and are actively applying. Personalise every message.
2. **WhatsApp Status.** Post a specific sample/offer and repeat it in different formats; Status is support for direct conversations, not a substitute for them.
3. **Permission-based university and Zimbabwean networks.** ZIMSOC, residence/class groups, faculty societies, alumni, church/community and diaspora groups. Ask admins first.
4. **Referral partners.** Tutors, student leaders, photographers, printing shops, recruiters willing to give general feedback, and people running job groups. Do not pay for access before a channel proves sales.
5. **Vacancy-led public content.** Use Gradlinc/LinkedIn/Indeed/PNet/Careers24 for SA examples and VacancyMail for Zimbabwe examples. Never imply affiliation with an employer or job board.
6. **Instagram and a dedicated TikTok.** Use them to prove competence and catch demand. They are not the primary month-one acquisition engine.
7. **Paid ads:** not in the first 90 days. With no proof, no working funnel and low order values, ads can consume the margin quickly.

## 8. Mobile, low-cost operating stack

| Need | Tool/process | Low-data/load-shedding rule |
|---|---|---|
| Sales and client messaging | WhatsApp Business: greeting, quick replies, labels (`New`, `Qualified`, `Awaiting info`, `Paid`, `Drafting`, `Revision`, `Complete`) and catalogue | Write long replies in Notes first; schedule one or two upload windows; keep SMS/call fallback only with consent |
| Intake | Google Form plus a plain WhatsApp version | Let clients send text answers if the form is expensive or inaccessible |
| Writing | Microsoft Word or Google Docs; one controlled master template | Enable offline files; download source files before planned outages |
| Storage | Google Drive with one private folder per client | Keep local encrypted/offline working copies where possible; sync when connectivity returns |
| Tracking | Google Sheets | One lightweight sheet; no complex CRM |
| Graphics | Canva mobile for social posts only | Reuse three templates; never use decorative Canva layouts for ATS CVs |
| Proofreading | Word Editor, Grammarly or LanguageTool plus manual read-aloud | No tool replaces fact checking; never accept a rewrite blindly |
| Calls | WhatsApp audio, Google Meet only if needed | Audio-first; video optional to preserve data |
| Power | Charged power bank, offline files and honest deadline buffer | Do not sell a 24-hour rush when power/data capacity is uncertain |
| Payments | SA EFT/PayShap if available; Zimbabwe EcoCash USD, InnBucks, bank/remittance only if the owner has compliant accounts | Confirm payer name, amount, fees and currency; never send final work against a screenshot alone—verify receipt |

Do not buy a CRM, scheduling app, premium design pack or website in month one. After legal clearance and first revenue, check a real registrar and connect a resolvable domain. An NXDOMAIN result is not proof that a name is available for registration.

# E. 7-day sprint

**Time budget:** 2–3 hours per day, maximum 13–18 hours for the week. If immigration permission is unresolved, every “sell/close” action below becomes a waitlist/market-research action and no money is accepted.

| Day | Actions in order | Output and pass/fail number |
|---|---|---|
| **1 — Compliance and conversion setup** | 1. Copy the exact visa endorsement. 2. Send the compliance email in section D. 3. Change Instagram name/bio and remove dead-domain wording. 4. Set up WhatsApp Business greeting, labels and `TARGET` quick reply. | Email sent and saved; one functioning WhatsApp link tested from another phone; profile communicates buyer, price, turnaround and CTA |
| **2 — Product system** | 1. Finalise the four packages/terms. 2. Build a short intake Form and WhatsApp alternative. 3. Create client tracker and folder template. 4. Create invoice/receipt template but do not issue it before clearance. | A test lead can move from inquiry to ready-to-draft without improvisation |
| **3 — Proof without deception** | 1. Choose one real public internship/graduate vacancy. 2. Create a clearly fictional early-career CV with weak but realistic content. 3. Produce a corrected ATS-safe version and a five-point explanation. 4. Proofread twice. | One before/after asset; zero spelling errors; no fake person presented as a client |
| **4 — Publish and start conversations** | 1. Publish the sample carousel. 2. Post the price/process card to Status. 3. Send 10–15 personalised warm messages using section H. 4. Record every response. | 10–15 messages, target 4 replies and 2 qualified conversations—not likes |
| **5 — Borrowed distribution** | 1. Ask five group admins/society contacts for permission to share a useful checklist or 20-minute CV teardown. 2. Contact ZIMSOC respectfully. 3. Publish one vacancy-specific tip/reel. | Five admin asks; target two permissions or calls; one content asset |
| **6 — Qualify and close** | 1. Follow up all replies within a fixed 45-minute block. 2. Conduct up to three 10-minute audio consultations. 3. Recommend one package each. 4. If and only if written compliance clearance exists, take payment and onboard; otherwise add the person to a no-deposit waitlist. | Three recommendations; target one lawful paid order or three qualified waitlist leads |
| **7 — Deliver and review the funnel** | If cleared and sold: draft/deliver using QA. If not: create the second sample and refine systems. Then calculate contacts → replies → qualified leads → sales/waitlist. Prepare the next week based on the bottleneck. | First delivery on time or two strong samples; weekly numbers recorded; next 10 follow-ups scheduled |

**Do not spend this week** designing a website, changing the logo repeatedly, creating 20 generic posts, buying ads or offering free custom CVs to strangers.

# F. 30-day plan

## Operating rhythm

1. **Daily:** two 20-minute inbox/follow-up blocks; no constant chat monitoring.
2. **Weekdays:** five new personalised contacts per day once the warm list is ready.
3. **Weekly:** three strong feed posts, three to five WhatsApp Status items, two partner/admin requests and one KPI review.
4. **Content ratio:** of approximately 12 feed posts, use 5 Generate, 4 Nurture and 3 Convert. The rest of the effort is outreach and delivery.
5. **Capacity protection:** accept no more than four normal jobs in a week and no more than two Full Launch packages. Close ordering when promised work would exceed the time cap.

## Daily calendar

| Day | Revenue/outreach action | Content action and CTA | Measure |
|---:|---|---|---|
| 1 | Send visa/compliance request; configure WhatsApp and tracker | Replace bio; Status says exactly who the service helps and “Reply `TARGET`” | Link works; compliance request saved |
| 2 | Build intake, terms, packages and payment checklist | Status: three-step process | Test onboarding completed in under 10 minutes |
| 3 | List 30 warm contacts by relevance, not popularity | Create the fictional before/after sample; do not publish before QA | Asset passes QA |
| 4 | Message warm contacts 1–10 individually | **Feed G:** carousel “Why this graduate bullet says nothing—and the rewrite” → `TARGET` | Replies and qualified chats |
| 5 | Ask five group/society admins for permission | Status poll: “Applying in next 30 days? SA / ZW / Not yet” | Admin replies; poll responses |
| 6 | Follow up day-4 replies; up to three short calls | **Feed G:** vacancy breakdown reel using one real SA role → “Send vacancy link” | Consultations booked |
| 7 | If cleared, onboard first client; otherwise waitlist only | **Feed C:** package/price/process post | Quotes-to-sales or waitlist conversion |
| 8 | Message warm contacts 11–15 | Status: intake checklist screenshot | Five sends; two replies target |
| 9 | Ask two student leaders/tutors for referrals | **Feed N:** show the seven-point QA checklist | Saves/shares and chats |
| 10 | Follow up every open lead with one specific question | No feed post; reshare sample to Status with beta-slot count that is factually current | Open leads moved or closed |
| 11 | Message contacts 16–20 and two Zimbabwe contacts | **Feed G:** VacancyMail role—three keywords and evidence an applicant needs | ZW replies |
| 12 | Offer a 20-minute group CV teardown to one approved network | Status: question box “What role are you applying for?” | Workshop accepted/booked |
| 13 | Deliver active orders; ask for missing facts early | Status: short PDF copy/paste ATS test using sample data | Completion rate and replies |
| 14 | Weekly review; stop the weakest lead source | **Feed C:** “Two package slots this week” only if two real slots exist | Contacts, replies, leads, sales, revenue |
| 15 | Message contacts 21–25; ask one satisfied beta client for an honest review if one exists | Status: review or, if none, transparent sample/process proof | Review obtained without scripting praise |
| 16 | Send three referral asks and two partner asks | **Feed G:** “Do you need a career objective?” Explain when a summary helps | DMs containing target role |
| 17 | Follow up all quotes older than 24 hours | No feed; Status FAQ on price and one revision | Quote decisions |
| 18 | Message five applicants in relevant communities only where promotion is allowed; do not scrape | **Feed N:** anonymised/composite before/after bullet with permission/label | Qualified conversations, not raw DMs |
| 19 | Check one SA graduate-programme deadline and create a lead list of people who opted in | Status: deadline/application-document checklist | Shares to relevant applicants |
| 20 | Deliver orders; request consolidated revisions | Status: “What to send before we start” | First-draft on-time rate |
| 21 | Weekly review and capacity check | **Feed N:** what changed in the service after two weeks; use real process learning, not inflated results | Sales by source; hours per order |
| 22 | Message five new warm/referral contacts | **Feed G:** “One-column vs two-column CV: ATS-safe test” | Saves and `TARGET` chats |
| 23 | Ask two Zimbabwe diaspora/community admins for permission | Status: SA vs ZW application question | Permission and relevant replies |
| 24 | Follow up partner leads; propose referral process, not vague “collaboration” | **Feed N:** explain how a vacancy becomes keywords, evidence and ordering | Partner referrals |
| 25 | Message five new contacts; close stale leads politely | No feed; Status with one sample slide and price | Pipeline cleaned |
| 26 | Hold one approved 20-minute audio/live CV teardown using fictional/public sample | Status summary from the session; no attendee data without consent | Attendees and opt-in consultations |
| 27 | Deliver active jobs and request reviews | Status: delivery checklist | On-time delivery and reviews |
| 28 | Full monthly KPI review and client-source ranking | **Feed C:** next-month package availability and exact CTA | Month totals and next-month forecast |
| 29 | Contact the top five referrers/leads from the best-performing channel | Status: month lesson/process improvement, with no inflated success claim | Repeat/referral conversations |
| 30 | Remove beta price if five are sold; schedule next month; archive/delete data due under policy | Update and pin the current offer card; unpin obsolete pricing | Current profiles, clean tracker, planned capacity |

## Content rules for this calendar

1. A vacancy-led post uses a real public vacancy but does not reproduce personal recruiter details or imply endorsement.
2. Do not claim “ATS approved,” “guaranteed ATS pass,” “90% success” or “get hired faster” without defensible evidence.
3. A testimonial must be the client’s genuine words, with permission. Minor spelling cleanup requires approval; never change meaning.
4. Use low-data formats: compressed 20–35 second reels, static carousels and text Status updates. Captions should carry the substance for people who cannot stream video.
5. If content consumes more than four hours per week without producing qualified chats, reduce production and increase direct outreach.

# G. 60–90 day plan

## Days 31–60 — prove repeatability

1. **End beta pricing after five clients.** Do not keep discounting because a prospect hesitates.
2. **Choose the best two acquisition channels** based on paid sales, not impressions. Allocate 70% of acquisition time to them; pause channels with no qualified leads after a fair test.
3. **Collect five proof assets:** honest reviews, anonymised before/after extracts, turnaround evidence and process clips. A review is not proof that the person got a job.
4. **Build three job-family checklists** from actual demand—for example finance/admin, marketing/communications and IT/data. These are internal QA aids, not mass-produced CVs.
5. **Run two small partner sessions** with permitted societies/groups. Give useful instruction, then offer the package once at the end.
6. **Implement referral credit only after demand exists:** R50/US$3 credit to the referrer on a future order or equivalent discount to the referred buyer, released only after a completed paid order. Check accounting/payment implications first. Never pay group admins secretly.
7. **Buy nothing major.** A working domain and simple one-page site become reasonable only after legal clearance and at least five paid clients. Verify the domain through an accredited registrar at purchase time.
8. **Document SOPs:** lead qualification, intake, vacancy mapping, drafting, QA, revisions, delivery, review request and deletion.
9. **Track time by package.** If CV Reset consistently takes more than 2.5 hours or Job-Target more than 3.5 hours, tighten intake/scope before adding volume.

**Day-60 gate:** continue only if at least one channel has produced three paid clients, first drafts are at least 90% on time, and quality can be maintained within the lawful time limit. If not, fix the offer/channel; do not add services.

## Days 61–90 — scale only what worked

1. **Raise price before raising volume** if either condition occurs:
   - two consecutive weeks are at 80% or more of delivery capacity; or
   - the qualified-lead close rate exceeds 50% for at least 10 leads.
   A first increase can be approximately 10–15%; test it on new leads only.
2. **Create one focused niche page/series** around the best-selling job family. Do not create separate accounts.
3. **Introduce monthly vacancy-tailoring support only if requested repeatedly.** Example: two vacancy-specific CV/cover-letter adjustments per month with strict scope. Price it after measuring time; do not launch a cheap unlimited plan.
4. **Formalise two referral partnerships** that each produced at least two qualified leads. Give them a unique WhatsApp keyword so source attribution is real.
5. **Build a one-page site** with promise, packages, sample, process, terms and WhatsApp CTA if a valid domain is connected. No blog is needed.
6. **Do not hire/subcontract yet** unless legal advice permits it, there is at least eight weeks of excess paid demand, and privacy/quality controls exist.
7. **Do not buy ads** until the organic funnel has at least 20 paid clients, a measured landing-to-chat conversion, a measured close rate and sufficient gross margin to set a maximum acquisition cost.
8. **Review positioning at day 90:** keep SA + ZW if both generate sales; otherwise lead publicly with the stronger market while still serving the other.

## What scaling does not mean

It does not mean posting daily, adding ten services, promising job placement, automating client writing without review, or working beyond visa/academic limits. For this owner, scale first means higher conversion, tighter scope, templates, referrals and higher revenue per lawful hour.

# H. Sales scripts

Replace every bracket before sending. Do not copy-paste a claim that is not true.

## 1. Warm WhatsApp message

> Hi [Name]—I’ve launched JobReadyCV for students and recent graduates applying to internships, graduate programmes and entry-level roles in SA/Zimbabwe. I tailor the CV to the actual role and deliver DOCX + ATS-safe PDF. I’m opening the first five beta CV slots at R299/US$15, with one revision. Are you applying for anything in the next 30 days? If yes, send the vacancy link and I’ll tell you honestly whether the package fits. No pressure if not.

If legal clearance is pending, replace the price sentence with:

> I’m currently building a no-deposit interest list while I confirm my study-visa work conditions in writing. Are you applying for anything in the next 30 days?

## 2. Group-admin permission request

> Hi [Name]. I’m a [course/year if relevant] student and I run JobReadyCV, focused on ATS-safe documents for internships and entry-level roles. May I share one practical before/after CV checklist in [group]? It will include one short line about my paid service, not repeated promotions. I will follow the group rules and won’t DM members without consent. If promotion is not allowed, no problem.

## 3. Approved group post

> Applying for an internship or graduate role? Before sending your CV, check: one column; normal headings; no icons/tables; evidence-based bullets; keywords from the actual vacancy; selectable PDF text. I’ve posted a before/after example here: [link]. JobReadyCV also offers vacancy-specific CV and cover-letter work from R399/US$20, 48–72 hours, one revision. WhatsApp `TARGET` plus the vacancy link: [link]. No job/interview guarantee.

## 4. Instagram/TikTok CTA

> Applying for this kind of role? WhatsApp **TARGET** with the vacancy link and your deadline. I’ll recommend the smallest package that fits.

## 5. WhatsApp greeting/auto-reply

> Thanks for contacting JobReadyCV. To check fit, please send: 1) target role or vacancy link, 2) deadline, 3) current CV—yes/no, 4) years of experience, and 5) country/payment currency. I reply during [real hours]. Please remove ID/passport numbers before sending documents.

## 6. Qualification questions

> Before I quote, please answer five points:
> 1. What exact role/job family are you targeting?
> 2. Send the vacancy link/text if available.
> 3. What is the real application deadline?
> 4. Do you have a current CV and complete dates for education/experience/projects?
> 5. Do you need CV only, CV + cover letter, or LinkedIn/interview support too?

Red flags to decline or re-scope: same-day impossible deadline, request to invent experience, missing core facts, unlimited applications expected, or a senior/executive field beyond the owner’s competence.

## 7. Package recommendation

> Based on the vacancy and your deadline, I recommend the **Job-Target Pack at R599/US$30**: one CV tailored to this vacancy, one matching cover letter, DOCX + selectable PDF, and one consolidated revision within seven days. First draft is due within 48–72 hours after payment and complete intake. I cannot guarantee an interview, but I will align truthful evidence and keywords and run the document through my QA checklist. Shall I send the terms and intake link?

## 8. Price reply

> CV Reset is R399/US$20. The Job-Target Pack is R599/US$30 and includes the vacancy-specific cover letter. Full Launch is R999/US$55 with LinkedIn rewrite and a 30-minute mock interview. Which vacancy and deadline are you working with? I’ll recommend one—not automatically the most expensive.

## 9. Close/payment message

> Confirmed: [package], [currency/amount], for [target role], first draft by [date/time], subject to receiving complete information by [cut-off]. One consolidated revision within seven days is included. New vacancies or major new information are outside this scope. No interview/job outcome is guaranteed. Payment method: [verified method]. I start after the payment is confirmed and the intake is complete. Reply **I AGREE** if these terms are correct.

Do not use this message until the compliance gate is cleared.

## 10. Pending-clearance waitlist message

> I’m interested in helping, but I’m still obtaining written confirmation about the self-employment conditions on my study visa. I will not accept a deposit before that is clear. With your permission, I can record your target role and deadline and contact you when I have the answer. If your deadline is sooner, please use another provider or your university career service rather than wait.

## 11. 24-hour quote follow-up

> Hi [Name], checking whether you still want help with the [role] application due [date]. The remaining question is [specific missing item]. If the timing or price does not work, tell me and I’ll close the quote—no repeated messages.

## 12. Final follow-up

> I’m closing this quote so I don’t keep messaging you. If you apply for another role later, send `TARGET` plus the link and I’ll re-check capacity.

## 13. “It is too expensive” response

> Understood. If you are an SU student, start with the free university career service. For my service, the lowest standard option is CV Reset at R399/US$20 because it includes intake, rewrite, ATS-safe formatting, QA, DOCX/PDF and one revision. I can’t reduce the scope below that without reducing quality. If the beta slots are genuinely still open, the beta rate is R299/US$15.

## 14. “Can’t AI do this?” response

> AI can help generate wording, but it does not verify your facts, decide which evidence is strongest for this vacancy, protect you from invented claims, or guarantee readable formatting. My paid work is the human intake, vacancy mapping, factual rewrite, formatting, QA and revision. If you prefer DIY, I can share the checklist and you can use it yourself.

## 15. “I have no experience” response

> That does not mean there is nothing to use. We can assess projects, coursework, volunteering, leadership, part-time work and demonstrated skills. I will not invent experience. Send the vacancy and your background first; if there is not enough evidence for a credible application, I will say so before taking the job.

## 16. Review request

> Hi [Name], your final files are complete. Would you send an honest 1–3 sentence review covering the process, clarity and turnaround? Please do not say you got an interview/job unless that has actually happened. May I publish it with [first name / initials / anonymous] and a redacted before/after extract? “No” is completely fine.

## 17. Referral request

> If you know one person actively applying for an internship or entry-level role, please forward this link: [WhatsApp link]. Ask them to send `REF-[code]` and their vacancy. Please don’t add people to a group or share their numbers without consent.

## 18. Partner proposal

> You referred [number] relevant applicants last month. I propose a simple tracked arrangement: people send keyword `[PARTNER]`; I report only aggregate inquiry/sale numbers, never client documents; and [transparent credit] applies after a completed paid order. No exclusivity and no hidden fee. If it produces no completed orders in 30 days, we stop.

# I. KPIs and revenue targets

## 1. Month-one funnel assumptions

This is a starting model, not a promise:

1. **100 personalised contacts/conversations** over four weeks—about five each weekday.
2. **40 replies** (40% reply rate) because the first list should be warm or permission-based.
3. **16 qualified leads** (40% of replies) with a real role, usable deadline and ability to buy.
4. **4–6 paid clients** (25–38% of qualified leads) if legal clearance arrives early enough.
5. Content assists trust but is not assumed to create most month-one sales.

If outreach is colder than planned, reply and close rates will be lower. If clearance is delayed, paid revenue will be lower or zero even when demand exists.

## 2. Conservative revenue scenarios

Revenue is gross cash collected before payment fees, data, software, refunds, tax and the owner’s time. ZAR and USD columns are alternative same-market mixes, not amounts to add together or currency equivalents.

| Scenario | Mix | ZAR gross | USD-price gross | Meaning |
|---|---|---:|---:|---|
| **Compliance delayed all month** | No paid orders | **R0** | **US$0** | Correct result: build waitlist/assets; do not trade unlawfully |
| **Month 1 conservative** | 2 beta + 1 CV Reset + 1 Job-Target | **R1,596** | **US$80** | Four clients from zero proof |
| **Month 1 base target** | 3 beta + 1 CV Reset + 2 Job-Target | **R2,494** | **US$125** | Six clients; still manageable |
| **Month 1 stretch, not forecast** | 3 beta + 1 CV Reset + 3 Job-Target + 1 Full Launch | **R4,092** | **US$210** | Eight clients; accept only if deadlines/hours permit |
| **Month 2 base** | 3 CV Reset + 3 Job-Target + 2 Full Launch | **R4,992** | **US$260** | About 25 fulfilment hours across the month |
| **Month 3 base** | 4 CV Reset + 4 Job-Target + 2 Full Launch | **R5,990** | **US$310** | About 30 fulfilment hours across the month |

The month-two and month-three figures are conditional on proof, referrals and legal capacity. They are not an argument for working more than 20 hours in any week. At 13 available hours per week, the month-three mix leaves roughly 5–6 hours per week for sales, admin and content after fulfilment. If measured fulfilment takes longer, reduce orders or raise prices.

## 3. Weekly scorecard

### Sales

1. New personalised contacts sent.
2. Reply rate = replies ÷ new contacts.
3. Qualified-lead rate = qualified leads ÷ replies.
4. Quote rate = quotes ÷ qualified leads.
5. Close rate = paid clients ÷ quotes.
6. Gross cash collected by ZAR/USD and payment method.
7. Average order value by currency.
8. Paid clients by source keyword.
9. Follow-ups due and pipeline value; never count a quote as revenue.

### Delivery and quality

1. Hours spent per package, including messages and revision.
2. First drafts delivered on time; target **90%+**.
3. Revision rate and reason.
4. Defects found after final delivery; target **0 factual or contact-detail defects**.
5. Turnaround from complete intake/payment to first draft.
6. Orders declined due to capacity or scope.
7. Honest reviews requested and received.

### Content

1. Qualified chats attributable to each post/status.
2. WhatsApp link clicks if measurable.
3. Saves, shares and profile visits.
4. Chat-to-qualified-lead rate.
5. Production time per post.

Follower count and likes are secondary. A post with 200 views and two qualified chats is commercially stronger than one with 10,000 irrelevant views and none.

### Client outcome learning

At 30 and 60 days, ask clients voluntarily for applications submitted, responses and interviews. Record this separately from service quality. Do not claim that JobReadyCV caused an interview without enough evidence and permission.

### Compliance and finance

1. Operating hours each week against the written visa condition.
2. Academic-vacation status and any restriction confirmed in writing.
3. Payment fees, FX loss, refunds and direct costs.
4. Client-data deletion dates.
5. Tax/business-registration questions resolved with qualified local guidance. Do not guess a tax set-aside percentage.

## 4. Decision rules

1. **Reply rate below 20% after 30 relevant messages:** the list or opening message is wrong. Improve targeting before sending more.
2. **Replies are healthy but qualified leads below 25%:** the audience is curious but not applying; focus on vacancy/deadline signals.
3. **At least 10 qualified leads but close rate below 20%:** inspect trust, samples, price presentation and speed. Do not automatically discount.
4. **Close rate above 50% and capacity above 80% for two weeks:** raise new-client prices 10–15% or close slots.
5. **Four strong posts produce zero qualified chats:** reduce content time and return to direct/partner outreach.
6. **Revisions exceed 1.5 rounds on average:** intake and scope are failing; enforce one consolidated revision.
7. **A channel produces three paid clients:** keep testing it. A channel produces none after 30 relevant contacts: pause it.
8. **Work approaches the legal/time cap:** stop taking orders. Deadlines and immigration compliance outrank short-term revenue.

## 5. Minimum tracker columns

`Date | Name/ID | Country | Source keyword | Target role | Deadline | Package | Quote currency | Quote amount | Status | Payment verified | Intake complete | First-draft due | Delivered | Revision due | Hours | Review permission | Referral | Delete-data date`

Use initials or a client ID in the sales dashboard; keep personal documents in private folders, not in the tracking sheet.

# J. Clarifying questions

The plan can start with profile/system work now. Question 1 blocks paid trading; questions 2–5 are needed to finalise operations and complete the social audit.

1. **Visa/compliance:** What is the exact wording printed on the study visa/endorsement, what are the university’s official vacation dates, and what written answer do SU International/Home Affairs or a qualified immigration professional give about self-employment/freelancing? Do not send passport numbers in chat.
2. **Payments and WhatsApp:** Which business WhatsApp country code/number will be used, and which methods can actually receive and verify ZAR and USD—SA bank EFT/PayShap, EcoCash USD, InnBucks, Zimbabwean bank or remittance? Are the accounts in the owner’s own lawful name/business structure?
3. **TikTok evidence:** Please provide screenshots of (a) the full profile header, (b) the latest 9–12 video thumbnails, (c) each recent video’s visible views/likes/comments/shares, and (d) TikTok Studio analytics for the last 28 or 60 days: Overview, Content, Viewers/Followers, top territories and active times. Also state whether the account can be renamed and whether its audience is mainly Stellenbosch humour/entertainment.
4. **Instagram evidence:** Please provide a screenshot of the native profile header and Instagram Insights for the last 30 days: accounts reached, profile activity/link taps, follower locations and each post’s reach, saves, shares and watch time. The public mirror could not expose these.
5. **Delivery competence and niche:** What CV-writing, recruitment, HR or proofreading experience/training does the owner have; which degree/fields are understood best; and can one existing personal CV or fictional sample be used to demonstrate a before/after transformation without making false claims?
