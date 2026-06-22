"""
Auto Applier -- Cover Letter Generator
Generates a one-page, signed PDF cover letter tailored to a specific role/company.

Requirements:
    pip install reportlab pypdf

Usage:
    python generate_cover_letter.py \
        --company "CentralSquare Technologies" \
        --address1 "1000 Business Center Drive" \
        --address2 "Lake Mary, FL 32746" \
        --role "Professional Services Consultant (Finance Software)" \
        --body_paragraphs body.txt \
        --output "output/Cover Letter - CentralSquare Technologies.pdf"

body.txt should contain paragraphs separated by blank lines.
"""

import argparse
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Image, Flowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY


class VerticalFill(Flowable):
    """Expands to consume remaining vertical space minus the closing block height,
    pushing content after it (closing + signature) to the bottom of the page."""
    # Approximate height (pts) needed for: spacer + Sincerely + spacer +
    # signature image + spacer + name + degree + school lines
    CLOSING_HEIGHT = 130

    def wrap(self, available_width, available_height):
        self.height = max(0, available_height - self.CLOSING_HEIGHT)
        return (available_width, self.height)

    def draw(self):
        pass
import yaml
import os

# ── Load user config ──────────────────────────────────────────────────────────
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config/user_config.yaml")

with open(CONFIG_PATH) as f:
    config = yaml.safe_load(f)

USER   = config["user"]
ASSETS = config["assets"]

# ── Styles ────────────────────────────────────────────────────────────────────
name_style = ParagraphStyle(
    "Name", fontSize=18, fontName="Times-Bold",
    alignment=TA_CENTER, leading=22, spaceAfter=0, spaceBefore=0
)
contact_style = ParagraphStyle(
    "Contact", fontSize=11, fontName="Times-Roman",
    alignment=TA_LEFT, leading=14, spaceAfter=0, spaceBefore=0
)
body_style = ParagraphStyle(
    "Body", fontSize=11, fontName="Times-Roman",
    alignment=TA_JUSTIFY, leading=14, spaceAfter=8, spaceBefore=0
)


def build_cover_letter(company, address1, address2, role, paragraphs, output_path):
    doc = SimpleDocTemplate(
        output_path, pagesize=letter,
        leftMargin=72, rightMargin=72, topMargin=72, bottomMargin=72
    )

    story = []

    # Header
    story.append(Paragraph(USER["name"], name_style))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=0.75, color=colors.black,
                            spaceAfter=0, spaceBefore=0))
    story.append(Spacer(1, 5))
    story.append(Paragraph(
        f"{USER['phone']} | {USER['email']} | {USER['location']}", contact_style
    ))
    story.append(Spacer(1, 14))

    # Address block
    story.append(Paragraph(company,  contact_style))
    story.append(Paragraph(address1, contact_style))
    story.append(Paragraph(address2, contact_style))
    story.append(Spacer(1, 10))

    # Salutation
    story.append(Paragraph("Dear Hiring Team,", body_style))

    # Body paragraphs
    for para in paragraphs:
        story.append(Paragraph(para.strip(), body_style))

    # Fill remaining page height so closing sits at the bottom
    story.append(VerticalFill())

    # Closing
    story.append(Spacer(1, 6))
    story.append(Paragraph("Sincerely,", contact_style))
    story.append(Spacer(1, 2))

    # Signature image
    sig_path = os.path.join(os.path.dirname(__file__), "..", ASSETS["signature_path"])
    if os.path.exists(sig_path):
        sig = Image(sig_path, width=91.5 * 0.9, height=49.3 * 0.9)
        sig.hAlign = "LEFT"
        story.append(sig)
    story.append(Spacer(1, 2))

    # Name + credentials
    story.append(Paragraph(USER["name"],   contact_style))
    story.append(Paragraph(USER["degree"], contact_style))
    story.append(Paragraph(USER["school_name"], contact_style))

    doc.build(story)
    print(f"Cover letter saved to: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--company",  required=True)
    parser.add_argument("--address1", required=True)
    parser.add_argument("--address2", required=True)
    parser.add_argument("--role",     required=True)
    parser.add_argument("--body_paragraphs", required=True,
                        help="Path to .txt file with paragraphs separated by blank lines")
    parser.add_argument("--output",   required=True)
    args = parser.parse_args()

    with open(args.body_paragraphs) as f:
        raw = f.read()
    paragraphs = [p.strip() for p in raw.split("\n\n") if p.strip()]

    build_cover_letter(
        args.company, args.address1, args.address2,
        args.role, paragraphs, args.output
    )
