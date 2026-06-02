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

1. **Paste job posting** into Claude Cowork
2. Claude searches LinkedIn (`/company/{slug}/people/?facetSchool={ID}`) and the company website for alumni
3. Claude searches LinkedIn and the company website for hiring division contacts
4. Claude generates BCC lists (multiple email format variants per person)
5. Claude creates two Gmail drafts (alumni + team) via the Gmail MCP
6. Claude generates a tailored cover letter PDF saved to `output/`

### LinkedIn extraction script

When browsing LinkedIn manually, use `scripts/linkedin_extract.js` in your browser console to extract people from the page.

### Gmail drafts

**Finding contacts:**
Before creating either draft, search LinkedIn (`/company/{slug}/people/?facetSchool={ID}`) and the company website to find:
- **USC alumni** at the company → used for the alumni draft BCC
- **Hiring division / commercial team contacts** → used for the team draft BCC (trim to 6–10 most decision-relevant people)

**Generating BCC email addresses:**
For each person found, generate all 4 format variations using the company's domain:
1. `first.last@companydomain`
2. `first@companydomain`
3. `firstlast@companydomain`
4. `flast@companydomain`

Add every variation as BCC on the appropriate draft:
- Alumni draft BCC → all format variations for each USC alum found
- Team draft BCC → all format variations for each hiring team contact found

**Subject line:**
```
{ROLE} Application, USC Grad
```
Use the exact role title from the job posting. Example: `Software Engineer Application, USC Grad`

**Rules:**
- **To: field MUST remain empty** — do not populate it under any circumstances; the user fills it in manually before sending
- Do **not** create either draft unless BCC is populated
- **Attach your resume manually** before sending each draft (Gmail MCP does not support attachments)

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
- Team BCC lists are trimmed to 6–10 most decision-relevant people to avoid over-spamming
- Cover letters are 1 page, no em dashes, with embedded handwritten signature

---

## Contributing

Pull requests welcome. If you adapt this for a different school or email workflow, consider opening a PR to add your config as an example in `config/examples/`.
