# Auto Applier

Automated job application outreach workflow powered by Claude (Cowork). For every role you apply to, Auto Applier finds alumni and team contacts, generates BCC email lists, creates Gmail drafts, and produces a tailored one-page cover letter — all from a single job posting.

---

## What it does

For each job posting you provide, the workflow:

1. **Finds alumni** at the company from your school (LinkedIn + company website)
2. **Finds team contacts** in the hiring division (LinkedIn, company About/Team pages, etc.)
3. **Generates BCC lists** with multiple email format variants per person
4. **Creates two Gmail drafts** automatically:
   - Alumni draft — mentions shared school, alumni sign-off
   - Team draft — generic professional opener
5. **Generates a tailored cover letter PDF** — one page, signed, role-specific

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/auto-applier.git
cd auto-applier
```

### 2. Install dependencies

```bash
pip install reportlab pypdf pyyaml pymupdf
```

### 3. Configure your profile

Edit `config/user_config.yaml`:

```yaml
user:
  name: "Your Name"
  email: "you@gmail.com"
  phone: "(123) 456-7890"
  location: "City, ST"
  degree: "B.S. in Your Major"
  school_name: "Your School Name"

school:
  full_name: "University of Southern California"
  short_name: "USC"
  linkedin_facet_id: "3084"       # Find your school's LinkedIn ID below
  alumni_greeting: "fellow Trojan"
  alumni_sign_off: "Fight on!"
```

**Finding your school's LinkedIn facet ID:**
Go to your school's LinkedIn page. The numeric ID appears in the URL or page source. For USC it is `3084`.

### 4. Add your assets

Place the following in the `assets/` folder:
- `resume.pdf` — your resume
- `signature.jpeg` — your handwritten signature (see `assets/README.md` for extraction instructions)

### 5. Customize email templates (optional)

Edit `config/email_templates.yaml` to adjust the alumni and team email body text. Tokens like `{ROLE}`, `{COMPANY}`, `{SCHOOL}`, `{ALUMNI_GREETING}`, and `{SIGN_OFF}` are filled in automatically.

---

## Workflow (Claude / Cowork)

Auto Applier is designed to be run inside **Claude Cowork** with the Gmail MCP connected. Paste a job posting into Claude and the workflow runs automatically.

### Step-by-step

1. **Paste job posting** into Claude Cowork. **If a job posting URL is given, Claude MUST open it directly** (Chrome MCP, not just WebSearch) before doing anything else — see "Job posting URLs / ATS pages" below.
2. Claude searches LinkedIn (`/company/{slug}/people/?facetSchool={ID}`) and the company website for alumni
3. Claude searches LinkedIn and the company website for hiring division contacts
4. Claude generates BCC lists (multiple email format variants per person)
5. **Claude MUST read `config/email_templates.yaml` before writing any draft.** Fill in the tokens ({NAME}, {ROLE}, {COMPANY}, {SCHOOL_FULL}, {SIGN_OFF}, {ROLE_FOCUS}) and use the body verbatim. Never rewrite or paraphrase the template copy.
6. Claude creates two Gmail drafts (alumni + team) via the Gmail MCP
7. Claude generates a tailored cover letter PDF saved to `output/` — only when explicitly requested

### Job posting URLs / ATS pages (STRICT — never deviate)

Job postings hosted on ATS platforms (iCIMS, Greenhouse, Lever, Workday, SmartRecruiters, etc. — e.g. `careers-cnb.icims.com/jobs/13227/...`) are routinely **not indexed by search engines**, especially when the URL carries candidate-session tracking params (`from=login`, `eem=`, `code=`, `ga=`, etc.). WebSearch for the role title or job ID will frequently return nothing but the company's generic careers portal/login page — that is NOT the same as "the role doesn't exist" or "details aren't available."

These pages are also commonly JS-rendered, so `mcp__workspace__web_fetch` (raw HTML, no JS) often returns an empty shell even though the page works fine in a browser.

Required behavior whenever a job posting is provided as a URL (or whenever WebSearch can't find a posting the user references):
1. **Open the URL directly with the Chrome MCP** (`navigate` + `get_page_text`). If `get_page_text` comes back as boilerplate/empty (common on these JS-heavy ATS pages), **take a screenshot and read the rendered page** instead of concluding the posting can't be found.
2. Pull the actual role details (team name, responsibilities, qualifications) from that page — don't fall back to guessing from the job title alone.
3. Only report "couldn't find this posting" after directly opening the URL/careers page in the browser and confirming it's truly inaccessible (e.g., requires login credentials Claude doesn't have) — never after a WebSearch miss alone.

### LinkedIn extraction script

When browsing LinkedIn manually, use `scripts/linkedin_extract.js` in your browser console to extract people from the page.

### Gmail drafts

Drafts are created with all outreach addresses in BCC. The To: field must be left blank — pass `to: []` (empty array) when calling `create_draft`. **Never put Victor's email or any placeholder in the To: field.** Fill in a recipient manually in Gmail before sending. **Attach your resume manually** before sending each draft (Gmail MCP does not support attachments).

---

## Output

All generated files are saved to the `output/` folder:

```
output/
  Cover Letter - Company Name.pdf
```

---

## Repo structure

```
auto-applier/
├── README.md
├── config/
│   ├── user_config.yaml        # Your personal info and school settings
│   └── email_templates.yaml    # Alumni and team email templates
├── assets/
│   ├── resume.pdf              # Your resume (add manually)
│   ├── signature.jpeg          # Your signature (add manually)
│   └── README.md               # Instructions for signature extraction
├── scripts/
│   ├── linkedin_extract.js     # Browser console script for LinkedIn scraping
│   └── generate_cover_letter.py  # Cover letter PDF generator
└── output/                     # Generated cover letters land here
```

---

## Notes

- Email format verification is done via RocketReach or web search each run
- If no alumni are found at a company, the alumni draft and BCC list are skipped
- Cover letters are NOT generated unless explicitly requested. When requested: 1 page, no em dashes, with embedded handwritten signature, must fill the whole page (closing/signature anchored to bottom)
- **"Anchored to bottom" is not the same as "fills the page."** `scripts/generate_cover_letter.py` uses a `VerticalFill` flowable that always pushes the closing/signature block down to the bottom margin, regardless of how short the body is. That mechanism alone does NOT make the letter look full — if the body paragraphs are short, the result is a technically-one-page letter with a large, unprofessional dead gap between the body and the signature. Filling the page is a CONTENT requirement, not something the script does for you.
- Both email drafts must include BCC recipients with all 4 email format variations per person (first.last, first, firstlast, flast — all @companydomain). Alumni draft BCCs USC alumni found at the company; team draft BCCs hiring division contacts

## Team contact sourcing rules (STRICT — never deviate)

1. **Hard minimum: 10+ distinct people on every team BCC list. Not 5-6, not "5-6+" — 10 is the floor.** A team draft with fewer than 10 people is incomplete and must not be sent to `create_draft` yet.
2. **Search the immediate hiring team/division first** (LinkedIn + company site). Whatever that turns up — even if it's only 2-4 people — is just the starting count, not the final list.
3. **If step 2 produced fewer than 10 people, broadening is mandatory, not optional, and not something to wait for the user to request.** Immediately run additional searches outside the immediate team at the same company: adjacent departments, other seniority levels (analyst through MD/SVP), other office locations, and related/parent functions (e.g. broader "Capital Markets" or "Strategy" rather than only the exact sub-team named in the posting). Keep adding searches until the combined list reaches 10+ people.
4. **Explicit numeric gate before calling `create_draft` — do this every time, out loud in your own reasoning:** count the distinct people gathered so far. If the count is below 10, that is the answer to "am I done sourcing" — no. Run at least 2-3 more broadened searches before concluding the list is final. Only proceed to draft creation once the count is actually 10+ (or you have exhausted realistic search angles and can state what was tried).
5. **A short, highly-targeted list is not better than a longer, slightly-broader one.** When in doubt, include the borderline-relevant contact rather than omit it to keep the list "clean" — err toward more outside-team contacts, not fewer.
6. **Multiple roles at the same company in one request: no contact overlap.** If the user asks for outreach on more than one role at the same company, track which people were already used (alumni or team) for each role and exclude them when sourcing the next role's contacts. Each role's BCC lists (alumni + team) must be made up of people not BCC'd on any other role's drafts in the same request.

## Email writing rules (STRICT — never deviate)

1. **Follow the template exactly.** Email body must match the structure in `config/email_templates.yaml`. Do not rewrite, expand, or restructure the copy. Only fill in the tokens ({NAME}, {ROLE}, {COMPANY}, {SCHOOL_FULL}, {SIGN_OFF}, {ROLE_FOCUS}).
2. **No em dashes — ever.** Em dashes (—) are forbidden in all outputs: emails AND cover letters. Use a comma, hyphen, or reword the sentence instead.
3. **No contact info in signature.** Email signature is ONLY `Best,\n{NAME}` (team) or `{SIGN_OFF}\n\nBest,\n{NAME}` (alumni). Never include phone number, email address, or any other contact details — the email is sent from Victor's Gmail account.

## Cover letter rules (STRICT — never deviate)

1. **Write enough content to fill the page — don't rely on the script.** `VerticalFill` only anchors the closing/signature to the bottom margin; it does nothing to fill the gap above it. Body content must do that work.
2. **Minimum density: 3 paragraphs, ~280-350 words total, 5-7 sentences per paragraph.** Short, generic 3-4 sentence paragraphs are not acceptable — they leave a large dead gap above the signature even though the signature itself is correctly anchored at the bottom.
3. **Use specific, researched details**, not generic filler, to reach that length: cite something concrete about the company's strategy, products, recent news, or the specific responsibilities in the job posting. This is what naturally produces enough substantive content, rather than padding with repetition.
4. **Always verify visually before presenting the file.** After generating the PDF, render page 1 to a PNG (e.g. with `pymupdf`/`fitz`: `page.get_pixmap(matrix=fitz.Matrix(2,2)).save(...)`) and read the image. Confirm there is no large empty gap between the last body paragraph and "Sincerely," — if there is, lengthen the body and regenerate. Do not skip this check.
5. No em dashes (see rule 2 above — applies to cover letters too).

---

## Contributing

Pull requests welcome. If you adapt this for a different school or email workflow, consider opening a PR to add your config as an example in `config/examples/`.
