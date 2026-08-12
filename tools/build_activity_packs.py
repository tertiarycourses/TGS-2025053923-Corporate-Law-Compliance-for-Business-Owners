#!/usr/bin/env python3
"""Build one printable PDF pack from each activity folder's Markdown files."""

from __future__ import annotations

import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
ACTIVITIES = ROOT / "activities"
BLUE = colors.HexColor("#1F6FEB")
NAVY = colors.HexColor("#172B4D")
TEAL = colors.HexColor("#10B981")
VIOLET = colors.HexColor("#7C3AED")
INK = colors.HexColor("#161B26")
GREY = colors.HexColor("#5B6372")
LINE = colors.HexColor("#DDE5EF")


def clean(text: str) -> str:
    return (text.replace("\u2011", "-").replace("\u2013", "-")
            .replace("\u2014", "-").replace("\u00a0", " "))


def inline(text: str) -> str:
    text = clean(text.strip())
    links: list[tuple[str, str]] = []

    def save_link(match: re.Match[str]) -> str:
        links.append((match.group(1), match.group(2)))
        return f"@@LINK{len(links) - 1}@@"

    text = re.sub(r"\[([^]]+)]\((https?://[^)]+)\)", save_link, text)
    text = html.escape(text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    for index, (label, url) in enumerate(links):
        replacement = (
            f'<link href="{html.escape(url, quote=True)}" color="#1F6FEB">'
            f'<u>{html.escape(clean(label))}</u></link>'
        )
        text = text.replace(f"@@LINK{index}@@", replacement)
    return text


base = getSampleStyleSheet()
body = ParagraphStyle("Body", parent=base["BodyText"], fontName="Helvetica",
                      fontSize=9.3, leading=12.8, textColor=INK, spaceAfter=5)
title = ParagraphStyle("Title", parent=body, fontName="Helvetica-Bold", fontSize=21,
                       leading=25, textColor=NAVY, spaceAfter=9)
h2 = ParagraphStyle("H2", parent=body, fontName="Helvetica-Bold", fontSize=13.5,
                    leading=16.5, textColor=BLUE, spaceBefore=7, spaceAfter=5,
                    keepWithNext=True)
h3 = ParagraphStyle("H3", parent=body, fontName="Helvetica-Bold", fontSize=10.8,
                    leading=13.5, textColor=VIOLET, spaceBefore=5, spaceAfter=4,
                    keepWithNext=True)
meta = ParagraphStyle("Meta", parent=body, fontSize=8.8, leading=11.5,
                      textColor=GREY, spaceAfter=2)
bullet = ParagraphStyle("Bullet", parent=body, leftIndent=14, firstLineIndent=-8,
                        bulletIndent=4, spaceAfter=4)
step = ParagraphStyle("Step", parent=body, leftIndent=18, firstLineIndent=-13,
                      bulletIndent=3, spaceAfter=5)
quote = ParagraphStyle("Quote", parent=body, leftIndent=10, rightIndent=10,
                       borderColor=TEAL, borderWidth=1, borderPadding=7,
                       backColor=colors.HexColor("#EAF8F2"), textColor=NAVY,
                       spaceBefore=6, spaceAfter=6)
small = ParagraphStyle("Small", parent=body, fontSize=7.1, leading=9.1)
small_header = ParagraphStyle("SmallHeader", parent=small, fontName="Helvetica-Bold",
                              textColor=colors.white)


class ActivityPack(BaseDocTemplate):
    def __init__(self, filename: str, activity_no: int, **kwargs):
        self.activity_no = activity_no
        super().__init__(filename, pagesize=A4, leftMargin=17 * mm, rightMargin=17 * mm,
                         topMargin=18 * mm, bottomMargin=18 * mm, **kwargs)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height,
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates(PageTemplate("activity", [frame], onPage=self.decorate))

    def decorate(self, canvas, doc):
        width, height = A4
        canvas.saveState()
        canvas.setFillColor(NAVY)
        canvas.rect(0, height - 7 * mm, width, 7 * mm, fill=1, stroke=0)
        canvas.setFillColor(TEAL)
        canvas.rect(0, 0, width, 3 * mm, fill=1, stroke=0)
        canvas.setFont("Helvetica-Bold", 8)
        canvas.setFillColor(colors.white)
        canvas.drawString(17 * mm, height - 4.8 * mm,
                          "CORPORATE LAW COMPLIANCE FOR BUSINESS OWNERS")
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(GREY)
        canvas.drawString(17 * mm, 9 * mm,
                          f"TGS-2025053923 | Activity {self.activity_no} | Real-life case pack")
        canvas.drawRightString(width - 17 * mm, 9 * mm, f"Page {doc.page}")
        canvas.restoreState()


def markdown_story(path: Path) -> list:
    lines = path.read_text(encoding="utf-8").splitlines()
    story: list = []
    index = 0
    while index < len(lines):
        value = lines[index].strip()
        if not value:
            story.append(Spacer(1, 2.5 * mm))
            index += 1
            continue
        if value.startswith("# "):
            story.append(Paragraph(inline(value[2:]), title))
            index += 1
            continue
        if value.startswith("## "):
            story.append(Paragraph(inline(value[3:]), h2))
            index += 1
            continue
        if value.startswith("### "):
            story.append(Paragraph(inline(value[4:]), h3))
            index += 1
            continue
        if value.startswith("|"):
            block: list[str] = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                block.append(lines[index].strip())
                index += 1
            rows = [[cell.strip() for cell in row.strip("|").split("|")] for row in block]
            rows = [row for position, row in enumerate(rows) if position != 1]
            data = [[Paragraph(inline(cell or " "), small_header if row_index == 0 else small)
                     for cell in row] for row_index, row in enumerate(rows)]
            col_widths = [25 * mm, 25 * mm, 25 * mm, 29 * mm, 18 * mm, 20 * mm, 27 * mm]
            table = Table(data, colWidths=col_widths, repeatRows=1, hAlign="LEFT")
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), BLUE),
                ("GRID", (0, 0), (-1, -1), 0.5, LINE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]))
            story.extend([Spacer(1, 1.5 * mm), table, Spacer(1, 2 * mm)])
            continue
        numbered = re.match(r"(\d+)\.\s+(.*)", value)
        if numbered:
            story.append(Paragraph(f"<b>{numbered.group(1)}.</b> {inline(numbered.group(2))}", step))
            index += 1
            continue
        if value.startswith("- [ ] "):
            story.append(Paragraph("&#9744;&nbsp;&nbsp;" + inline(value[6:]), bullet))
            index += 1
            continue
        if value.startswith("- "):
            story.append(Paragraph("&#8226;&nbsp;&nbsp;" + inline(value[2:]), bullet))
            index += 1
            continue
        if value.startswith("> "):
            story.append(Paragraph(inline(value[2:]), quote))
            index += 1
            continue
        style = meta if value.startswith("**") and ":**" in value else body
        story.append(Paragraph(inline(value), style))
        index += 1
    return story


def main() -> None:
    folders = sorted(path for path in ACTIVITIES.glob("activity-[0-9][0-9]-*") if path.is_dir())
    if len(folders) != 8:
        raise SystemExit(f"Expected 8 activity folders, found {len(folders)}")
    for folder in folders:
        number = int(folder.name.split("-")[1])
        source_files = [folder / "activity-workbook.md", folder / "real-life-case-brief.md",
                        folder / "completion-checklist.md"]
        missing = [str(path) for path in source_files if not path.is_file()]
        if missing:
            raise SystemExit(f"Activity {number} is missing: {', '.join(missing)}")
        story: list = []
        for position, source in enumerate(source_files):
            if position:
                story.append(PageBreak())
            story.extend(markdown_story(source))
        output = folder / "activity-pack.pdf"
        ActivityPack(str(output), number, title=f"Activity {number} real-life case pack",
                     author="Tertiary Infotech Academy Pte Ltd",
                     subject="Corporate Law Compliance for Business Owners").build(story)
        print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
