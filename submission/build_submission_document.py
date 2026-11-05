from __future__ import annotations

import re
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "submission"
ASSET_DIR = OUT_DIR / ".document-assets"
DOCX_PATH = OUT_DIR / "The Quiet Collection Project Documentation.docx"
DIAGRAM_PATH = ASSET_DIR / "system-architecture.png"

INK = "241D19"
GREEN = "344334"
GREEN_LIGHT = "E8EDE5"
BRASS = "A78042"
PARCHMENT = "F5F0E4"
GRAY = "6B655E"
BORDER = "D9D9D9"


def font(size: int, bold: bool = False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Georgia Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Georgia.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def draw_architecture_diagram(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    width, height = 1800, 1280
    image = Image.new("RGB", (width, height), "#F7F3E9")
    d = ImageDraw.Draw(image)

    title_font = font(54, True)
    label_font = font(29, True)
    small_font = font(23, False)
    arrow_color = "#5B533F"

    def rounded_box(box, label, fill, outline="#6F5C37", label_color="#201A16", radius=24, max_chars=24):
        x1, y1, x2, y2 = box
        d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=4)
        lines = []
        for paragraph in label.split("\n"):
            lines.extend(textwrap.wrap(paragraph, width=max_chars) or [""])
        line_height = 34
        total = line_height * len(lines)
        y = (y1 + y2 - total) / 2
        for line in lines:
            bbox = d.textbbox((0, 0), line, font=label_font)
            x = (x1 + x2 - (bbox[2] - bbox[0])) / 2
            d.text((x, y), line, font=label_font, fill=label_color)
            y += line_height

    def center(box):
        return ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)

    def edge_point(box, target):
        cx, cy = center(box)
        tx, ty = target
        dx, dy = tx - cx, ty - cy
        if abs(dx) / max(1, box[2] - box[0]) > abs(dy) / max(1, box[3] - box[1]):
            x = box[2] if dx > 0 else box[0]
            y = cy + dy * abs((x - cx) / dx) if dx else cy
        else:
            y = box[3] if dy > 0 else box[1]
            x = cx + dx * abs((y - cy) / dy) if dy else cx
        return x, y

    def arrow(src, dst, label=None, dashed=False):
        start = edge_point(src, center(dst))
        end = edge_point(dst, center(src))
        if dashed:
            segments = 18
            for i in range(0, segments, 2):
                a = i / segments
                b = min(1, (i + 1) / segments)
                p1 = (start[0] + (end[0] - start[0]) * a, start[1] + (end[1] - start[1]) * a)
                p2 = (start[0] + (end[0] - start[0]) * b, start[1] + (end[1] - start[1]) * b)
                d.line([p1, p2], fill=arrow_color, width=5)
        else:
            d.line([start, end], fill=arrow_color, width=5)
        import math
        angle = math.atan2(end[1] - start[1], end[0] - start[0])
        length = 22
        left = (end[0] - length * math.cos(angle - .55), end[1] - length * math.sin(angle - .55))
        right = (end[0] - length * math.cos(angle + .55), end[1] - length * math.sin(angle + .55))
        d.polygon([end, left, right], fill=arrow_color)
        if label:
            mx, my = (start[0] + end[0]) / 2, (start[1] + end[1]) / 2
            tb = d.textbbox((0, 0), label, font=small_font)
            pad = 8
            d.rounded_rectangle((mx - (tb[2]-tb[0])/2 - pad, my - 20, mx + (tb[2]-tb[0])/2 + pad, my + 18), radius=8, fill="#F7F3E9")
            d.text((mx - (tb[2]-tb[0])/2, my - 15), label, font=small_font, fill="#4D4536")

    d.text((80, 48), "The Quiet Collection System Architecture", font=title_font, fill="#201A16")
    d.text((82, 116), "Deterministic personality logic with bounded AI character dialogue", font=small_font, fill="#6B655E")

    visitor = (690, 175, 1110, 280)
    player = (690, 350, 1110, 465)
    visual = (165, 545, 555, 690)
    interface = (650, 545, 1040, 690)
    api = (1245, 545, 1635, 690)
    assets = (70, 825, 390, 970)
    interaction = (420, 825, 740, 970)
    state = (770, 825, 1090, 970)
    scoring = (1120, 825, 1440, 970)
    fallback = (1470, 825, 1760, 970)
    result = (1120, 1085, 1440, 1220)

    rounded_box(visitor, "Visitor\nmobile or desktop", "#E8EDE5")
    rounded_box(player, "p5.js Web Editor player", "#D7E1D2")
    rounded_box(visual, "p5.js canvas +\nThree.js museum", "#F0DFC1")
    rounded_box(interface, "React interface +\ndialogue", "#F0DFC1")
    rounded_box(api, "OpenAI Responses API", "#E8EDE5")
    rounded_box(assets, "GLB models, textures,\nfont and BGM", "#FFFDF7", max_chars=25)
    rounded_box(interaction, "Navigation, hotspots,\nstamp stations and\nAbraham patrol", "#FFFDF7", max_chars=25)
    rounded_box(state, "Authored copy + visit state\nin localStorage", "#FFFDF7", max_chars=26)
    rounded_box(scoring, "Deterministic scoring\nand six specimens", "#FFFDF7", max_chars=25)
    rounded_box(fallback, "Authored fallback\ndialogue", "#F7E9D0", max_chars=20)
    rounded_box(result, "Final placard + visitor\nin the display case", "#D7E1D2", max_chars=25)

    arrow(visitor, player)
    arrow(player, visual)
    arrow(player, interface)
    arrow(visual, assets)
    arrow(visual, interaction)
    arrow(interface, state)
    arrow(state, scoring)
    arrow(scoring, result)
    arrow(interface, api, "live chat")
    arrow(api, interface, "bounded reply")
    arrow(api, fallback, "if unavailable", dashed=True)

    d.rounded_rectangle((40, 510, 1775, 1245), radius=28, outline="#B6A47A", width=3)
    d.text((68, 480), "BROWSER EXPERIENCE", font=small_font, fill="#6B655E")
    image.save(path, quality=95)


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_margins(cell, top=130, start=140, bottom=130, end=140):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for margin, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{margin}"))
        if node is None:
            node = OxmlElement(f"w:{margin}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_cell_border(cell, color=BORDER, size="6"):
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = tc_pr.first_child_found_in("w:tcBorders")
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tc_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = f"w:{edge}"
        border = borders.find(qn(tag))
        if border is None:
            border = OxmlElement(tag)
            borders.append(border)
        border.set(qn("w:val"), "single")
        border.set(qn("w:sz"), size)
        border.set(qn("w:color"), color)


def prevent_row_split(row):
    tr_pr = row._tr.get_or_add_trPr()
    if tr_pr.find(qn("w:cantSplit")) is None:
        tr_pr.append(OxmlElement("w:cantSplit"))


def remove_paragraph_borders(element):
    p_pr = element.get_or_add_pPr()
    border = p_pr.find(qn("w:pBdr"))
    if border is not None:
        p_pr.remove(border)


def style_run(run, name="Aptos", size=None, bold=None, color=None, italic=None):
    run.font.name = name
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), name)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    if color is not None:
        run.font.color.rgb = RGBColor.from_string(color)


def add_body(doc, text, *, bold_lead=None, italic=False, keep=False, space_before=0, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if keep:
        p.paragraph_format.keep_with_next = True
    if bold_lead and text.startswith(bold_lead):
        lead = p.add_run(bold_lead)
        style_run(lead, bold=True, color=INK)
        rest = p.add_run(text[len(bold_lead):])
        style_run(rest, italic=italic, color=INK)
    else:
        run = p.add_run(text)
        style_run(run, italic=italic, color=INK)
    return p


def add_bullets(doc, items):
    for item in items:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.12
        style_run(p.add_run(item), color=INK)


def add_numbered(doc, items):
    for index, item in enumerate(items, 1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(.28)
        p.paragraph_format.first_line_indent = Inches(-.22)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.line_spacing = 1.12
        style_run(p.add_run(f"{index}.  {item}"), color=INK)


def add_heading(doc, text, level=1):
    p = doc.add_heading(text, level=level)
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_before = Pt(14 if level == 1 else 10)
    p.paragraph_format.space_after = Pt(6)
    return p


def add_table(doc, headers, rows, widths=None, font_size=9.5):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.rows[0]._tr.get_or_add_trPr().append(OxmlElement("w:tblHeader"))
    prevent_row_split(table.rows[0])
    for index, header in enumerate(headers):
        cell = table.rows[0].cells[index]
        if widths:
            cell.width = Inches(widths[index])
        set_cell_shading(cell, GREEN)
        set_cell_margins(cell)
        set_cell_border(cell)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_after = Pt(0)
        style_run(p.add_run(header), size=font_size, bold=True, color="FFFFFF")
    for row_index, row in enumerate(rows):
        added_row = table.add_row()
        prevent_row_split(added_row)
        cells = added_row.cells
        for index, value in enumerate(row):
            cell = cells[index]
            if widths:
                cell.width = Inches(widths[index])
            set_cell_shading(cell, "FFFFFF" if row_index % 2 == 0 else "F3F5F1")
            set_cell_margins(cell)
            set_cell_border(cell)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.08
            style_run(p.add_run(str(value)), size=font_size, color=INK)
    return table


def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = paragraph.add_run()
    fld_char1 = OxmlElement("w:fldChar")
    fld_char1.set(qn("w:fldCharType"), "begin")
    instr_text = OxmlElement("w:instrText")
    instr_text.set(qn("xml:space"), "preserve")
    instr_text.text = "PAGE"
    fld_char2 = OxmlElement("w:fldChar")
    fld_char2.set(qn("w:fldCharType"), "end")
    run._r.append(fld_char1)
    run._r.append(instr_text)
    run._r.append(fld_char2)
    style_run(run, size=9, color=GRAY)


def read_system_prompt():
    source = (ROOT / "museum-site/lib/abraham.mjs").read_text(encoding="utf-8")
    match = re.search(r"export const instructions=`(.*?)`;", source, re.S)
    if not match:
        raise RuntimeError("Could not extract Abraham's system prompt")
    return match.group(1).strip()


def build_document():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    draw_architecture_diagram(DIAGRAM_PATH)
    prompt = read_system_prompt()

    doc = Document()
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(.72)
    section.bottom_margin = Inches(.72)
    section.left_margin = Inches(.78)
    section.right_margin = Inches(.78)

    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = "Aptos"
    normal._element.rPr.rFonts.set(qn("w:ascii"), "Aptos")
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Aptos")
    normal.font.size = Pt(10.5)
    normal.font.color.rgb = RGBColor.from_string(INK)
    for style_name, size in (("Title", 30), ("Subtitle", 15), ("Heading 1", 21), ("Heading 2", 14), ("Heading 3", 11.5)):
        style = styles[style_name]
        style.font.name = "Georgia"
        style._element.rPr.rFonts.set(qn("w:ascii"), "Georgia")
        style._element.rPr.rFonts.set(qn("w:hAnsi"), "Georgia")
        style.font.size = Pt(size)
        style.font.color.rgb = RGBColor(0, 0, 0)
        if style_name in ("Heading 1", "Heading 2", "Heading 3"):
            style.font.bold = True
    remove_paragraph_borders(styles["Title"]._element)

    footer = section.footer
    footer_p = footer.paragraphs[0]
    style_run(footer_p.add_run("THE QUIET COLLECTION  |  "), size=8.5, color=GRAY)
    add_page_number(footer_p)

    # Cover
    p = doc.add_paragraph(style="Title")
    remove_paragraph_borders(p._element)
    p.paragraph_format.space_before = Pt(72)
    p.paragraph_format.space_after = Pt(18)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.add_run("The Quiet Collection Project Documentation")
    sub = doc.add_paragraph(style="Subtitle")
    sub.paragraph_format.space_after = Pt(36)
    sub.add_run("System Architecture Prompt Design Interaction Patterns and Development Reflection")
    meta = doc.add_paragraph()
    meta.paragraph_format.space_after = Pt(24)
    style_run(meta.add_run("Submission version\n"), size=10, bold=True, color=GREEN)
    style_run(meta.add_run("4 November 2026"), size=10.5, color=INK)
    add_body(doc, "The Quiet Collection is a mobile-first personality quiz presented as an explorable natural history museum. The visitor does not begin as a known person taking a test; they enter as an unidentified entity, collect eight stamps, and are finally appraised by Abraham, the museum's hamster administrator.", space_after=12)
    add_body(doc, "The central technical decision is that the result is computed by deterministic local scoring. The AI does not choose the user's personality outcome. It only gives Abraham bounded, optional dialogue and a visit-based note. This separation keeps the six specimen results stable, testable and available even when the API cannot be reached.", space_after=12)
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(28)
    p.paragraph_format.space_after = Pt(0)
    style_run(p.add_run("Project format"), size=9, bold=True, color=BRASS)
    add_body(doc, "p5.js player with React interface, Three.js museum rendering, Blender and Hunyuan assets, authored scoring, local visit persistence and optional OpenAI Responses API dialogue.")
    doc.add_page_break()

    # 1 Architecture
    add_heading(doc, "1 System Architecture", 1)
    add_body(doc, "The experience is mostly client-side. The p5.js Web Editor player loads the interface, the 3D museum and its media assets. The browser stores the visit locally, calculates the result from authored choice IDs and renders the final placard. A model request occurs only when the visitor asks Abraham to speak live or requests a personal result note.")
    picture_p = doc.add_paragraph()
    picture_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    picture_p.paragraph_format.keep_with_next = True
    picture_p.add_run().add_picture(str(DIAGRAM_PATH), width=Inches(6.85))
    caption = doc.add_paragraph("Figure 1. The Quiet Collection system architecture. The dotted branch shows the authored dialogue fallback used when live chat is unavailable.")
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    caption.paragraph_format.space_after = Pt(12)
    for run in caption.runs:
        style_run(run, size=9, italic=True, color=GRAY)

    add_heading(doc, "1.1 Components and responsibilities", 2)
    add_table(doc,
              ["Layer", "Technology", "Responsibility"],
              [
                  ["Player shell", "p5.js Web Editor", "Hosts the sketch and starts the packaged museum experience."],
                  ["Presentation", "React and CSS", "Entry, reception dialogue, stamp card, station choices, settings, chat and archival result sheet."],
                  ["Museum rendering", "Three.js and WebGL", "Loads the museum and Abraham GLB files, handles camera movement, hotspots, lighting, floating details and result specimens."],
                  ["Authored logic", "JSON and JavaScript modules", "Stores questions and copy, validates answer IDs, computes scores, selects evidence and maps a result code to a specimen."],
                  ["Local state", "Browser localStorage", "Keeps the visitor name, eight answers, discoveries, recent dialogue, music preferences and completion state on that device."],
                  ["Character dialogue", "OpenAI Responses API", "Generates short Abraham replies from fixed instructions and a bounded visit record. It does not control scoring."],
                  ["Media", "GLB, MP3, PNG and font files", "Provides the museum, Abraham, portrait, soundtrack, fallback scene and typography."],
              ],
              widths=[1.25, 1.6, 4.0], font_size=9.2)

    add_heading(doc, "1.2 Data flow", 2)
    add_numbered(doc, [
        "The visitor enters the museum and supplies a name. A versioned visit object is created in the browser.",
        "Each station records a stable choice ID. Decorative discoveries and free conversation are stored separately and cannot add points.",
        "After all eight stamps, the scoring module recomputes four dimension totals from the recorded choices and resolves one of six paired outcomes or a mixed result.",
        "The result page maps the fixed result code to a real natural-history specimen and places a stylised model in the central glass case.",
        "If the visitor talks to Abraham, the app sends the latest message plus a sanitised visit context to the model. The reply returns to the dialogue layer only.",
        "If live dialogue is unavailable, authored fallback lines keep the game usable and preserve the user's answers."
    ])

    add_heading(doc, "1.3 API deployment note", 2)
    add_body(doc, "The current p5.js live-chat build can call the Responses API directly from the browser using a shared key. This meets the prototype requirement that testers do not enter a key, but any key placed in public sketch code can be inspected and reused by others. The project also contains a safer Vercel route in which the browser calls /api/abraham and the server reads OPENAI_API_KEY from an environment variable. That server route is the recommended architecture for a public release.")
    doc.add_page_break()

    # 2 Prompt and interaction documentation
    add_heading(doc, "2 Prompt and Interaction Documentation", 1)
    add_body(doc, "Abraham is both a visible character and the only generative interface in the game. The prompt therefore has to preserve character voice without allowing the model to redefine the quiz. The implementation uses three layers: fixed instructions, structured visit context and a complete authored fallback.")

    add_heading(doc, "2.1 Prompt strategy", 2)
    add_bullets(doc, [
        "Character: Abraham is a small, earnest museum administrator who treats the warm but uncanny museum as an ordinary workplace.",
        "Voice: replies are one to three short sentences, casual and concrete, with slight obliviousness rather than sinister intent or exaggerated cuteness.",
        "Role boundary: Abraham may chat for fun at any stage, but he cannot assign a specimen before the card is complete and cannot change the application-computed specimen afterward.",
        "Evidence boundary: only the eight scored choices affect the result. Discoveries, free conversation and the optional reflection may personalise wording but never add points.",
        "Memory boundary: the model is told to use only supplied records and not invent actions, feelings, motives, time spent or dialogue.",
        "Safety and tone: the prompt avoids diagnostic claims and psychological certainty. The museum ending remains fictional and knowingly uncanny rather than a real claim about the visitor.",
        "Output boundary: the API returns plain text, not markdown or scores, with a maximum output budget of 300 tokens."
    ])

    add_heading(doc, "2.2 Structured prompt context", 2)
    add_table(doc,
              ["Field", "Purpose", "Scoring effect"],
              [
                  ["mode", "Chooses casual chat or a result-specific remark.", "None"],
                  ["visitorName", "Lets Abraham address the visitor by the supplied name or Item-09.", "None"],
                  ["specimen", "Contains the already computed result profile, or null before completion.", "Already fixed"],
                  ["choices", "Provides stable question IDs, exact choice text and authored evidence summaries.", "Computed locally first"],
                  ["discoveries", "Records optional oddities such as the backwards clock or drawer of stars.", "None"],
                  ["reflection", "Allows the visitor to qualify an interpretation in their own words.", "None"],
                  ["conversation", "Supplies a bounded recent dialogue history for continuity.", "None"],
                  ["latestMessage", "Tells Abraham what to answer now.", "None"],
              ], widths=[1.22, 3.8, 1.75], font_size=9.1)

    add_heading(doc, "2.3 Request and response pattern", 2)
    add_numbered(doc, [
        "The visitor taps Abraham or opens the companion dialogue from the result page.",
        "The client appends the visitor's message to the local conversation and sends a chat request.",
        "The application restores and validates the visit record before creating the model context. Invalid answer IDs are discarded and the specimen is recomputed rather than trusted from the browser payload.",
        "The model receives the fixed Abraham instructions and the structured context. The request disables provider-side storage and limits the output length.",
        "The returned plain-text reply appears in a Genshin-style dialogue strip. The current question and any unsubmitted choice remain intact when the conversation closes.",
        "On timeout, configuration failure or an unusable response, the app shows a short authored Abraham line instead of a technical error."
    ])

    add_heading(doc, "2.4 Player interaction patterns", 2)
    add_table(doc,
              ["Moment", "Player action", "System response", "Design intention"],
              [
                  ["Entry", "Select Enter the museum.", "Music starts after a user gesture and the reception scene opens.", "Introduce the quiz clearly without exposing scores."],
                  ["Reception", "Enter a name and continue Abraham's dialogue.", "The stamp card animates into the left tool dock.", "Make onboarding diegetic rather than a form wizard."],
                  ["Exploration", "Move with a joystick, drag to look and pinch or scroll to zoom.", "The camera stays within authored bounds while optional hotspots remain discoverable.", "Make the museum the main activity and reduce visible hand-holding."],
                  ["Stamp station", "Select a numbered display and choose one of four approaches.", "Abraham confirms the selection and a stamp is added; the answer can later be revised.", "Present personality choices as museum decisions rather than questionnaire fields."],
                  ["Abraham", "Tap the 3D character at any time.", "He stops his patrol, approaches the conversation framing and replies without forcing quiz progress.", "Treat him as a companion, not a help menu."],
                  ["Oddities", "Inspect the clock, drawer, labels, meteorite or leaves.", "A short uncanny interaction is recorded for possible dialogue callbacks.", "Reward curiosity without secretly affecting personality."],
                  ["Completion", "Finish all eight spaces and return for appraisal.", "A final tie-break preference is offered only when needed by the authored flow.", "Keep the result traceable and deterministic."],
                  ["Result", "Read the placard, view the specimen, talk, save or share.", "The visitor appears in the case as one of six real specimens and Abraham welcomes them to their permanent place.", "Deliver the uncanny reveal while still explaining the personality pattern."],
              ], widths=[.95, 1.65, 2.45, 1.8], font_size=8.55)

    doc.add_page_break()
    add_heading(doc, "2.5 Scoring interaction", 2)
    add_body(doc, "The four hidden dimensions are Inquiry, Continuity, Agency and Relationship. Every answer adds two points to a primary concern and one point to a secondary concern. All eight questions offer each dimension once as a primary and once as a secondary, so no dimension receives more opportunities merely because of question order. The algorithm checks the top pair, support across separate questions and an optional final preference for an exact tie. A language model never receives authority to change this result.")
    add_table(doc,
              ["Result code", "Specimen", "Combined concerns"],
              [
                  ["IC", "Paper nautilus eggcase", "Inquiry and continuity"],
                  ["CA", "Caddisfly case", "Continuity and agency"],
                  ["AR", "Sea bean", "Agency and relationship"],
                  ["CR", "Glass sponge skeleton", "Continuity and relationship"],
                  ["IA", "Fulgurite", "Inquiry and agency"],
                  ["IR", "Starling feather", "Inquiry and relationship"],
              ], widths=[1.0, 2.6, 3.2], font_size=9.3)
    add_body(doc, "The automated test suite evaluates all 65,536 complete answer combinations. It verifies balanced scoring opportunities, deterministic outcomes, evidence from three distinct questions, safe visit restoration and graceful API fallbacks.", space_before=9)
    doc.add_page_break()

    # 3 Reflection
    add_heading(doc, "3 Reflection on the Development Process", 1)
    add_body(doc, "The project changed substantially as the idea became more specific. It began as a request for a personality quiz with a story, but the first concepts still felt recognisably like a quiz hidden inside a narrative. The strongest shift came from asking a different question: instead of what a museum about the user would contain, what would the user be if they were a museum display item? Choosing a natural history museum made the premise more concrete and gave the results a visual and thematic home.")

    add_heading(doc, "3.1 Finding the creative direction", 2)
    add_body(doc, "The early design balanced warmth and unease. The visual references suggested a low-poly, game-like museum with dramatic amber light, dark wood and painterly rendering. Later feedback pushed the museum away from obvious horror. The clock, labels, drawer and floating objects became uncanny because they behave slightly incorrectly, while still belonging in the room. Keeping the original warm palette was important: the unsettling feeling comes from movement, text and implication rather than purple lighting or conventional horror colours.")
    add_body(doc, "The final result concept was another important correction. The outcome could not simply be an object already displayed somewhere in the museum, because that would make the reveal feel arbitrary. The selected set - paper nautilus eggcase, caddisfly case, sea bean, glass sponge skeleton, fulgurite and starling feather - consists of real things that users could recognise or look up, but they are unusual enough to fit the museum's dreamlike tone.")

    add_heading(doc, "3.2 Developing Abraham", 2)
    add_body(doc, "Abraham moved from a static guide concept to the emotional centre of the experience. His 3D model was generated externally, imported as GLB, rigged and animated for walking, idle movement and facial expression. In the browser he patrols the museum, produces occasional thought bubbles and stops when the visitor taps him. This helped the museum feel inhabited without adding crowds or conventional quest markers.")
    add_body(doc, "His writing required repeated revision. The first version sounded too formal and serious for a small hamster in a mysterious place. The final prompt makes him casually helpful, concrete and slightly oblivious. He notices impossible things but does not understand why they might be alarming. That contrast lets the game be creepy without turning Abraham into a villain. It also makes the final line about the visitor's forever home sound affectionate and unsettling at the same time.")

    add_heading(doc, "3.3 Moving from interface to game", 2)
    add_body(doc, "A major usability lesson was that more explanation did not automatically make the experience clearer. Early versions showed progress text, visible Easter-egg controls, movement buttons and multiple prompts at once. The viewport became crowded and the museum stopped feeling like the main activity. The interface was gradually reduced to a small tool dock, a joystick, optional map and settings, and contextual dialogue. Question numbers, secondary instructions and repeated labels were removed where the environment already communicated the action.")
    add_body(doc, "Camera behaviour also affected the sense of embodiment. A high or heavily offset camera made Abraham disappear behind dialogue and caused large scene shifts while rotating. Lowering and stabilising the view, reducing the implied player body and constraining movement made the experience calmer. These changes were not decorative; they determined whether exploration felt intentional or like moving a webpage around a 3D background.")

    add_heading(doc, "3.4 Technical decisions and challenges", 2)
    add_bullets(doc, [
        "The Blender scene could not be transferred to the browser with every Eevee painterly effect intact. The web version therefore keeps the geometry, warm PBR materials, focused lighting, fog and stylised motion rather than attempting a pixel-perfect render match.",
        "The web experience combines technologies instead of forcing every feature into p5 alone. p5 provides the distributable player and canvas context, Three.js handles the GLB scene and camera, and React provides accessible interface controls and dialogue.",
        "Large models and audio exposed p5 Web Editor upload limits. The assets had to be compressed, packaged carefully and referenced from predictable paths. The background track was re-encoded to a smaller MP3 while keeping the full duration.",
        "Live AI dialogue created a deployment trade-off. A direct browser key is simple for testing but public. A same-origin server route is safer and already exists in the project, so moving the final public build to that route is a clear next step.",
        "Separating AI dialogue from scoring made the system easier to test. The same quiz result is produced even when the API is missing, slow or unavailable."
    ])

    add_heading(doc, "3.5 What worked well", 2)
    add_bullets(doc, [
        "The museum premise integrates narrative, navigation, visual design and personality scoring instead of using story as a wrapper around radio buttons.",
        "The stamp card gives progress a physical metaphor and lets the player choose gallery order without seeing hidden dimensions.",
        "Real specimens make the result memorable while the archival placard explains the personality pattern directly.",
        "Abraham creates continuity across onboarding, exploration, chat and the final reveal.",
        "Authored fallbacks and deterministic scoring keep the experience functional without the API."
    ])

    add_heading(doc, "3.6 What I would improve next", 2)
    add_bullets(doc, [
        "Move the public p5 chat to the hosted API route so the key is never shipped to the browser, then add a durable usage limit before wider testing.",
        "Conduct mobile user tests focused on navigation, discoverability of stamp stations, dialogue readability and whether players understand that oddities do not affect the result.",
        "Optimise GLB meshes, textures and audio further, and test on older phones with low-power WebGL settings.",
        "Add stronger accessibility alternatives, including a complete 2D exploration mode, clearer keyboard focus treatment and verified screen-reader labels for every interactive station.",
        "Pilot the result language with users to check whether every answer feels defensible and whether the six specimens feel specific without sounding scientifically diagnostic."
    ])

    add_heading(doc, "3.7 Final reflection", 2)
    add_body(doc, "The most useful lesson from this project was that atmosphere and interaction design cannot be separated. A mysterious museum is not created only by its lighting or models; it also depends on what the interface chooses not to explain, when the character interrupts, how the camera moves and whether the player is trusted to explore. The process improved when each feature was judged against the same question: does this make the visitor feel as though they are discovering the museum, or merely completing a form inside it?")
    add_body(doc, "The AI component became stronger when its responsibility became smaller. Abraham feels responsive because he can remember a real choice or conversation, but the outcome remains authored, traceable and testable. That balance preserves the surprise of a live character without asking the model to decide who the user is.")
    doc.add_page_break()

    # Appendix A
    add_heading(doc, "Appendix A Abraham System Prompt", 1)
    add_body(doc, "The following prompt is the implemented character instruction used for both casual chat and result remarks. Structured visit context is supplied separately at runtime.", italic=True)
    for paragraph in prompt.split("\n"):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(.25)
        p.paragraph_format.right_indent = Inches(.18)
        p.paragraph_format.space_after = Pt(7)
        p.paragraph_format.line_spacing = 1.05
        style_run(p.add_run(paragraph), name="Aptos", size=9.3, color=INK)

    doc.add_page_break()
    add_heading(doc, "Appendix B Implementation References", 1)
    add_table(doc,
              ["Area", "Primary file"],
              [
                  ["Main experience state and screen flow", "museum-site/app/page.jsx"],
                  ["3D museum, camera and interactions", "museum-site/components/Museum.jsx"],
                  ["Reception and stamp-card handoff", "museum-site/components/Reception.jsx"],
                  ["Questions and answer evidence", "museum-site/lib/questions.json"],
                  ["Scoring and result selection", "museum-site/lib/quiz.mjs"],
                  ["Abraham prompt and API context", "museum-site/lib/abraham.mjs"],
                  ["Protected server endpoint", "museum-site/app/api/abraham/route.ts"],
                  ["p5 direct dialogue adapter", "p5-museum/direct-chat.js"],
                  ["Result specimen geometry", "museum-site/lib/result-specimens.mjs"],
                  ["Automated scoring and fallback tests", "museum-site/tests/quiz.test.mjs"],
              ], widths=[3.0, 3.8], font_size=9.4)

    # Keep all headings black and set document metadata.
    doc.core_properties.title = "The Quiet Collection Project Documentation"
    doc.core_properties.subject = "System architecture, prompt design, interaction patterns and project reflection"
    doc.core_properties.author = ""
    doc.core_properties.keywords = "personality quiz, p5.js, Three.js, OpenAI, interaction design"
    doc.save(DOCX_PATH)
    print(DOCX_PATH)


if __name__ == "__main__":
    build_document()
