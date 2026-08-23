#!/usr/bin/env python3
"""
Build the résumé PDF at public/Tilak-Raj-Resume.pdf.

Run:  python3 -m venv .venv && .venv/bin/pip install reportlab
      .venv/bin/python scripts/build-resume.py

Content comes from the 2026 CV. Two deliberate departures from that file:

  * "over 7 years of experience" is corrected to ten — Oct 2015 onward.
  * No client names and no internal project names. This PDF is published on a
    public site, so it follows the same rule the site does: employers are
    named, clients are described by sector.

Typography: the site uses Merriweather + Source Sans, which exist in this repo
only as woff2 (reportlab cannot embed those). Helvetica stands in — denser and
more ATS-parseable for a résumé anyway — while the plum, the letterspaced caps
and the hairline rules carry the portfolio's identity across.
"""

from reportlab.lib.colors import Color
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate, Frame, HRFlowable, KeepTogether,
    PageTemplate, Paragraph, Spacer,
)

OUT = "public/Tilak-Raj-Resume.pdf"
SITE = "thetilakraj.github.io/portfolio"

PLUM = Color(0x60 / 255, 0x57 / 255, 0x68 / 255)
INK = Color(0x32 / 255, 0x2B / 255, 0x38 / 255)
MUTED = Color(0x55 / 255, 0x4E / 255, 0x5C / 255)
FAINT = Color(0x8A / 255, 0x82 / 255, 0x94 / 255)
RULE = Color(0xC9 / 255, 0xBF / 255, 0xCE / 255)
AMBER = Color(0x8E / 255, 0x57 / 255, 0x0D / 255)
MARGIN = 0.62 * inch


def style(name, **kw):
    base = dict(name=name, fontName="Helvetica", fontSize=8.9, leading=12.2,
                textColor=INK, spaceBefore=0, spaceAfter=0)
    base.update(kw)
    return ParagraphStyle(**base)


S = {
    "name": style("name", fontName="Helvetica-Bold", fontSize=25, leading=26,
                  textColor=PLUM, spaceAfter=4),
    "title": style("title", fontSize=9.6, leading=13, textColor=AMBER,
                   spaceAfter=5),
    "contact": style("contact", fontSize=8.2, leading=11.6, textColor=MUTED,
                     spaceAfter=2),
    "section": style("section", fontName="Helvetica-Bold", fontSize=7.9,
                     leading=10, textColor=PLUM, spaceBefore=13, spaceAfter=5),
    "role": style("role", fontName="Helvetica-Bold", fontSize=9.9,
                  leading=12.6, spaceBefore=7),
    "org": style("org", fontSize=8.6, leading=11.4, textColor=MUTED,
                 spaceAfter=3),
    "body": style("body", textColor=MUTED, alignment=TA_JUSTIFY),
    "bullet": style("bullet", fontSize=8.7, leading=12.1, textColor=MUTED,
                    leftIndent=9.5, bulletIndent=1.5, spaceAfter=1.6),
    "kv": style("kv", fontSize=8.7, leading=12.2, textColor=MUTED,
                spaceAfter=2.4),
}


def caps(text):
    return "&nbsp;".join(list(text.upper()))


def section(label):
    return [Paragraph(caps(label), S["section"]),
            HRFlowable(width="100%", thickness=0.6, color=RULE, spaceAfter=6)]


def job(role, org, when, where, bullets):
    flow = [Paragraph(role, S["role"]),
            Paragraph(f'<font color="#605768"><b>{org}</b></font> &nbsp;·&nbsp; '
                      f'{where} &nbsp;·&nbsp; <font color="#8A8294">{when}</font>',
                      S["org"])]
    for b in bullets:
        flow.append(Paragraph(b, S["bullet"], bulletText="—"))
    return KeepTogether(flow)


def skills(label, items):
    return Paragraph(
        f'<font color="#605768"><b>{label}</b></font><br/>{items}',
        ParagraphStyle(name=f"sk-{label}", parent=S["kv"], spaceAfter=6.5))


story = []
story.append(Paragraph("Tilak Raj", S["name"]))
story.append(Paragraph(
    "SAP BTP Lead Consultant &nbsp;·&nbsp; SAP Build Work Zone &nbsp;·&nbsp; "
    "SAPUI5 / Fiori &nbsp;·&nbsp; UI/UX", S["title"]))
story.append(Paragraph(
    'Toronto, Ontario, Canada &nbsp;·&nbsp; '
    '<a href="mailto:thetilakraj@gmail.com"><font color="#8E570D">'
    'thetilakraj@gmail.com</font></a>', S["contact"]))
story.append(Paragraph(
    '<a href="https://www.linkedin.com/in/thetilakraj/"><font color="#8E570D">'
    'linkedin.com/in/thetilakraj</font></a> &nbsp;·&nbsp; '
    f'<a href="https://{SITE}/"><font color="#8E570D">{SITE}</font></a>',
    S["contact"]))
story.append(Spacer(1, 4))
story.append(HRFlowable(width="100%", thickness=1.4, color=PLUM, spaceAfter=2))

story += section("Summary")
story.append(Paragraph(
    "Engineer turned consultant and designer, with over ten years delivering "
    "end-to-end SAP implementations across SAP ECC and S/4HANA landscapes for "
    "the energy (hydrocarbon), retail, FMCG and agriculture sectors. I design, "
    "build and customise SAP Cloud Platform applications on SAP BTP and SAP "
    "BAS, and currently lead the technical delivery of an enterprise SAP BTP "
    "platform toward production launch across multiple vendor teams. Alongside "
    "that I design and ship consumer products end to end through my own "
    "company — research and design system through engineering, billing and "
    "release.", S["body"]))

story += section("Experience")

story.append(job("Technical Lead", "Chicken Farmers of Ontario",
                 "Sep 2024 – Present", "Toronto, ON", [
    "Lead operational readiness and the technical production launch of an "
    "enterprise SAP BTP platform, owning the implementation plan across "
    "pre-implementation, smoke test and post-launch support.",
    "Govern vendor-delivered development: SAPUI5 and CAP code review, daily "
    "stand-ups with application vendors and weekly technical meetings with "
    "services vendors, enforcing agreed coding standards.",
    "Review vendor architecture and technology stack against the target to "
    "surface integration risk before integration, alongside BTP setup, "
    "security and identity (IAS) and version-control practice.",
    "Own QA across all business domains for both SAP BTP (SAPUI5, CAP) and "
    "SAP Gateway services, resolving high and medium defects within the "
    "planned release window.",
    "Author SAP Gateway and ECC technical specification documents, and run "
    "production releases, Jira delivery and after-hours support.",
]))

story.append(job("Senior Software Developer", "Chicken Farmers of Ontario",
                 "Apr 2022 – Sep 2024", "Toronto, ON", [
    "Built an internal audit application with a SAPUI5 front end integrated "
    "to Dataverse, keeping data dynamically maintained.",
    "Automated document upload to SharePoint through the Microsoft Graph API "
    "directly from the application.",
    "Ran user acceptance testing end to end, absorbing requirement changes "
    "and defect fixes through to sign-off.",
    "Redesigned a producer-facing data collection application in Figma "
    "following a focus group with farmers, then oversaw its build.",
]))

story.append(job("SAP UI5 Fiori Consultant",
                 "Baariz Technology Solutions / OCR Solutions",
                 "Oct 2021 – Mar 2022", "Doha, Qatar", [
    "Delivered SAP UI5 Fiori applications on a short international posting, "
    "establishing shared requirement vocabulary in week one across a "
    "multi-language, multi-culture delivery team.",
    "Hardened layouts for right-to-left and multi-language rendering.",
]))

story.append(job("Associate Consultant", "Wipro",
                 "Jan 2021 – Jul 2021", "Bengaluru, India", [
    "Designed high-fidelity prototypes in SAP Build for a suite of paired "
    "request and administration workflow applications spanning expense, "
    "procurement and permitting for an energy-sector client.",
    "Treated the suite as one interaction system across nine deployments "
    "rather than nine separate applications.",
]))

story.append(job(
    "Associate Consultant &rarr; Senior Consultant, Package Implementation",
    "LTIMindtree", "May 2019 – Dec 2020", "Bengaluru, India", [
    "Delivered master data governance applications for an FMCG client, "
    "including multi-stage approval matrices and master data request "
    "monitoring.",
    "Built cost centre and internal order management apps, and treated "
    "notification email templates as a designed interface surface.",
]))

story.append(job(
    "Associate Software Engineer &rarr; Application Development Analyst",
    "Accenture", "Oct 2015 – Mar 2019", "Bengaluru, India", [
    "Delivered analytical and portfolio dashboards with drill-down and custom "
    "filtering, hierarchical data tables, sales and procurement transaction "
    "apps, process flows, org charts and document services.",
    "Built offline-capable enterprise mobile applications using the SMP SDK "
    "with Cordova and Kapsel plugins for plant and field users.",
    "Recognised with the Accenture Client &amp; Customer Award for "
    "accelerating delivery toward a new Diamond Client relationship.",
]))

story += section("Selected Product Work")

story.append(job("Radioverse — station-first live internet radio",
                 "TritSync Incorp Inc.", "2025 – Present",
                 "listenradioverse.com", [
    "Designed, built and shipped solo across every layer: research, design "
    "system, Next.js and Firebase engineering, Stripe billing, security "
    "hardening and production operations. Live in production.",
    "Curated catalogue across 34 markets with quality filtering, dedupe and "
    "genre balancing; playback resilience with mid-stream stall recovery; "
    "PWA with a Serwist service worker.",
    "Mobile cold TTFB 3.1s to ~0.8s and CLS 0.673 to ~0.007.",
]))

story.append(job(
    "Spellum — offline-first spelling learning for adults and ESL learners",
    "TritSync Incorp Inc.", "2025 – Present", "iOS, in development", [
    "Measures transfer to unseen words rather than rewarding word-completion "
    "volume, so the app only claims progress it can evidence.",
    "Swift and SwiftUI, offline-first, with an OKLCH to Display P3 token "
    "pipeline and fail-closed content and distribution gates.",
]))

story += section("Core Skills")
story.append(skills("SAP", "SAP BTP · SAP ERP · SAPUI5 / Fiori · SAP CAP · "
                    "SAP Gateway · SAP Build Work Zone · SAP BAS · ECC · "
                    "S/4HANA · SMP SDK, Cordova, Kapsel"))
story.append(skills("Design", "User experience research · Focus-group "
                    "facilitation · Figma · SAP Build · Design systems · "
                    "Accessibility · Information architecture"))
story.append(skills("Engineering", "TypeScript · Next.js · React · Swift and "
                    "SwiftUI · Firebase · Stripe · PWA and service workers · "
                    "Astro · Git"))
story.append(skills("Delivery", "Technical leadership · Vendor governance and "
                    "code review · QA strategy · Production readiness and "
                    "launch · Technical specification authorship · Jira"))

story += section("Certifications")
for c in [
    "SAP Certified Development Associate — SAP Fiori Application Developer "
    "<font color='#8A8294'>(SAP, Sept 2020)</font>",
    "SAP Certified Development Associate — SAP HANA 2.0 SPS04 "
    "<font color='#8A8294'>(SAP, Sept 2020)</font>",
    "Intelligent Enterprise User Experience with SAP Fiori 3",
    "SAP Fiori Overview: Design, Develop and Deploy",
    "Building Applications with SAP Cloud Application Programming Model",
]:
    story.append(Paragraph(c, S["bullet"], bulletText="—"))

story += section("Education")
story.append(Paragraph(
    "<b>Humber College</b> — Postgraduate, User Experience (UX) Design "
    "&nbsp;·&nbsp; <font color='#8A8294'>Toronto, 2021</font>", S["kv"]))
story.append(Paragraph(
    "<b>M. S. Ramaiah Institute of Technology</b> — B.E., Electrical and "
    "Electronics Engineering &nbsp;·&nbsp; "
    "<font color='#8A8294'>Bengaluru, 2015</font>", S["kv"]))

story += section("Awards")
story.append(Paragraph(
    "<b>Accenture Client &amp; Customer Award</b>, team category — for "
    "contribution to client business outcomes, accelerating delivery toward a "
    "new Diamond Client relationship. &nbsp;<font color='#8A8294'>"
    "Accenture Technology, December 2018</font>", S["kv"]))


def decorate(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PLUM)
    canvas.rect(0, 0, 5.5, LETTER[1], stroke=0, fill=1)
    canvas.setFont("Helvetica", 6.8)
    canvas.setFillColor(FAINT)
    canvas.drawString(MARGIN, 0.4 * inch, "Tilak Raj")
    canvas.drawRightString(LETTER[0] - MARGIN, 0.4 * inch, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(
    OUT, pagesize=LETTER, leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=0.5 * inch, bottomMargin=0.6 * inch,
    title="Tilak Raj — SAP BTP Lead Consultant", author="Tilak Raj",
    subject="Résumé", creator="Tilak Raj")
doc.addPageTemplates([PageTemplate(id="main", frames=[
    Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="body")
], onPage=decorate)])
doc.build(story)
print(f"wrote {OUT}")
