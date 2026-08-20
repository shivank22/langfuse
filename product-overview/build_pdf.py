#!/usr/bin/env python3
"""Assemble product-overview PDF (local extension of product-overview-pdf skill).

- Cover: title, subtitle, author
- Footer: left = page_label + page; right = AI-Council Switzerland
- Per-section optional \"diagram\" / \"diagram_caption\" fields in content.json
"""
import argparse
import json
import sys
from pathlib import Path

try:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import (
        HRFlowable,
        Image,
        ListFlowable,
        ListItem,
        PageBreak,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
    )
    from reportlab.lib.utils import ImageReader
except ImportError:
    sys.exit("Missing dependency. Install with: pip3 install reportlab")

ACCENT = colors.HexColor("#2563EB")
DARK = colors.HexColor("#0F172A")
MUTED = colors.HexColor("#475569")


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        "CoverTitle", parent=styles["Title"], fontSize=28, leading=34,
        textColor=DARK, alignment=TA_CENTER, spaceAfter=12,
    ))
    styles.add(ParagraphStyle(
        "CoverSubtitle", parent=styles["Normal"], fontSize=13, leading=18,
        textColor=MUTED, alignment=TA_CENTER, spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        "CoverAuthor", parent=styles["Normal"], fontSize=11, leading=15,
        textColor=DARK, alignment=TA_CENTER, spaceBefore=10, spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        "SectionHeading", parent=styles["Heading1"], fontSize=16, leading=20,
        textColor=ACCENT, spaceBefore=16, spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        "BodyTextX", parent=styles["BodyText"], fontSize=10.5, leading=15,
        textColor=DARK, alignment=TA_LEFT, spaceAfter=7,
    ))
    styles.add(ParagraphStyle(
        "BulletX", parent=styles["BodyText"], fontSize=10.5, leading=15,
        textColor=DARK, alignment=TA_LEFT,
    ))
    styles.add(ParagraphStyle(
        "IndexItem", parent=styles["BodyText"], fontSize=11, leading=18,
        textColor=DARK, alignment=TA_LEFT, spaceAfter=2, leftIndent=12,
    ))
    styles.add(ParagraphStyle(
        "Caption", parent=styles["Normal"], fontSize=9, leading=12,
        textColor=MUTED, alignment=TA_CENTER, spaceBefore=4, spaceAfter=8,
    ))
    return styles


def scaled_image(path, max_width, max_height):
    reader = ImageReader(path)
    iw, ih = reader.getSize()
    ratio = min(max_width / iw, max_height / ih)
    return Image(path, width=iw * ratio, height=ih * ratio)


def body_to_flowables(body, styles, is_index=False):
    flow = []
    bullets = []

    def flush_bullets():
        if bullets:
            flow.append(ListFlowable(
                [ListItem(Paragraph(b, styles["BulletX"]), leftIndent=10)
                 for b in bullets],
                bulletType="bullet", bulletColor=ACCENT, bulletFontSize=8,
                leftIndent=12, spaceAfter=8,
            ))
            bullets.clear()

    for item in body:
        text = str(item)
        if text.strip().startswith("- "):
            bullets.append(text.strip()[2:].strip())
        else:
            flush_bullets()
            style = styles["IndexItem"] if is_index and text.strip()[:1].isdigit() else styles["BodyTextX"]
            flow.append(Paragraph(text, style))
    flush_bullets()
    return flow


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--content", required=True)
    ap.add_argument("--diagram", default=None, help="Fallback diagram for Core Features")
    ap.add_argument("--output", default="product-overview.pdf")
    args = ap.parse_args()

    content_path = Path(args.content)
    base_dir = content_path.parent
    content = json.loads(content_path.read_text())

    styles = build_styles()
    doc = SimpleDocTemplate(
        args.output, pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2.2 * cm,
        title=content.get("title", "Product Overview"),
        author=content.get("author", ""),
    )
    content_width = doc.width
    story = []

    story.append(Spacer(1, 5 * cm))
    story.append(Paragraph(content.get("title", "Product Overview"), styles["CoverTitle"]))
    if content.get("subtitle"):
        story.append(Paragraph(content["subtitle"], styles["CoverSubtitle"]))
    story.append(Spacer(1, 0.4 * cm))
    story.append(HRFlowable(width="40%", thickness=2, color=ACCENT,
                            hAlign="CENTER", spaceBefore=8, spaceAfter=8))
    if content.get("author"):
        story.append(Paragraph(f"Author: {content['author']}", styles["CoverAuthor"]))
    story.append(PageBreak())

    for section in content.get("sections", []):
        heading = section.get("heading", "")
        story.append(Paragraph(heading, styles["SectionHeading"]))
        story.append(HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#E2E8F0"),
                                spaceBefore=0, spaceAfter=10))
        is_index = heading.strip().lower() == "index"
        story.extend(body_to_flowables(section.get("body", []), styles, is_index=is_index))

        diagram_name = section.get("diagram")
        if not diagram_name and heading.strip().lower() == "core features and infra" and args.diagram:
            diagram_name = args.diagram
        if diagram_name:
            diagram_path = Path(diagram_name)
            if not diagram_path.is_absolute():
                diagram_path = base_dir / diagram_path
            if diagram_path.exists():
                # Infra + detailed build/runtime figures need more height
                tall = any(
                    k in diagram_path.name
                    for k in ("architecture", "evaluations", "agentic-observability")
                )
                max_h = 14 * cm if tall else 9 * cm
                story.append(Spacer(1, 0.25 * cm))
                story.append(scaled_image(str(diagram_path), content_width, max_h))
                caption = section.get("diagram_caption", "Diagram")
                story.append(Paragraph(caption, styles["Caption"]))
            else:
                print(f"Warning: diagram not found: {diagram_path}", file=sys.stderr)

    footer_right = content.get("footer", "AI-Council Switzerland")
    page_label = content.get("page_label", content.get("title", ""))

    def add_footer(canvas, doc_):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(MUTED)
        left = f"{page_label}  ·  Page {doc_.page}" if page_label else f"Page {doc_.page}"
        canvas.drawString(2 * cm, 1.2 * cm, left)
        if footer_right:
            canvas.drawRightString(doc_.pagesize[0] - 2 * cm, 1.2 * cm, footer_right)
        canvas.restoreState()

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
