"""Generate Swift_Sign_Architecture.docx from the project's architecture info.
Run: venv\\Scripts\\python.exe make_docx.py
"""
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BLUE = RGBColor(0x0B, 0x5F, 0xFF)
DARK = RGBColor(0x0F, 0x17, 0x29)
MUTED = RGBColor(0x5B, 0x6B, 0x86)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GREEN = RGBColor(0x0F, 0x7A, 0x37)

doc = Document()

# Base style
normal = doc.styles["Normal"]
normal.font.name = "Calibri"
normal.font.size = Pt(11)
normal.font.color.rgb = DARK


def shade(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)


def h1(text):
    p = doc.add_paragraph()
    p.space_before = Pt(6)
    r = p.add_run(text)
    r.font.size = Pt(20)
    r.font.bold = True
    r.font.color.rgb = BLUE
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    return p


def h2(text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = DARK
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(3)
    return p


def para(text, muted=False, size=11):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.size = Pt(size)
    if muted:
        r.font.color.rgb = MUTED
    p.paragraph_format.space_after = Pt(6)
    return p


def bullet(text):
    p = doc.add_paragraph(style="List Bullet")
    r = p.add_run(text)
    r.font.size = Pt(11)
    p.paragraph_format.space_after = Pt(2)
    return p


def code(text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.name = "Consolas"
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0x1f, 0x2a, 0x44)
    p.paragraph_format.left_indent = Inches(0.2)
    p.paragraph_format.space_after = Pt(6)
    # light background
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), "EEF2F8")
    pPr.append(shd)
    return p


def table(headers, rows, widths=None):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t.rows[0].cells
    for i, htext in enumerate(headers):
        hdr[i].text = ""
        run = hdr[i].paragraphs[0].add_run(htext)
        run.font.bold = True
        run.font.size = Pt(10)
        run.font.color.rgb = WHITE
        shade(hdr[i], "0B5FFF")
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ""
            run = cells[i].paragraphs[0].add_run(val)
            run.font.size = Pt(10)
    if widths:
        for r_ in t.rows:
            for i, w in enumerate(widths):
                r_.cells[i].width = Inches(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


# ===================== TITLE =====================
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
tr = title.add_run("Swift Sign Group — AI Assistant")
tr.font.size = Pt(26)
tr.font.bold = True
tr.font.color.rgb = BLUE

sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
sr = sub.add_run("System Architecture")
sr.font.size = Pt(18)
sr.font.color.rgb = DARK

tagline = doc.add_paragraph()
tagline.alignment = WD_ALIGN_PARAGRAPH.CENTER
tgr = tagline.add_run("How the chatbot works end-to-end — production (Vercel) and local development")
tgr.font.size = Pt(11)
tgr.font.italic = True
tgr.font.color.rgb = MUTED

live = doc.add_paragraph()
live.alignment = WD_ALIGN_PARAGRAPH.CENTER
lr = live.add_run("Live at swiftsign-chatbot.vercel.app")
lr.font.size = Pt(10)

# ===================== 1. OVERVIEW =====================
h1("1. Overview")
para("The Swift Sign Group AI Assistant is a chat widget embedded in a marketing website. "
     "Visitors ask questions about any of the group's five divisions (IT & Cyber, Business Setup, "
     "Shipping, Laila Hijab, Organic Foods) and get instant, accurate answers powered by Google Gemini "
     "and a curated company knowledge base. The assistant replies in English or Roman Urdu, remembers "
     "the current conversation for follow-up questions, and falls back gracefully when AI models are busy.")
table(
    ["Metric", "Value"],
    [
        ["Deploy targets", "2 (Vercel production + local development)"],
        ["Business divisions", "5 (plus corporate HQ)"],
        ["AI model fallbacks", "6 (resilient cascade)"],
        ["Typical reply time", "~2–4 seconds"],
    ],
    widths=[2.4, 4.0],
)

# ===================== 2. BIG PICTURE =====================
h1("2. Big Picture — The Request Path")
para("In production everything is hosted on Vercel. A message travels through four stages:", muted=True)
table(
    ["Stage", "Component", "What it does"],
    [
        ["1. Client", "Visitor's Browser", "Static marketing site + chat widget (HTML/CSS/JS), served by Vercel's CDN."],
        ["2. Edge", "/api/chat Serverless Function", "Receives message + history. Handles greetings, security, then calls the AI. Runs only on demand."],
        ["3. AI", "Google Gemini + Knowledge Base", "A system prompt carrying the full knowledge base is sent with the question. A model cascade picks the first healthy model."],
        ["4. Response", "Back through the same path", "The reply returns to the browser, is rendered as a chat bubble, and saved to local history."],
    ],
    widths=[1.1, 2.2, 3.1],
)

# ===================== 3. LIFECYCLE =====================
h1("3. Request Lifecycle")
para("What happens, in order, when a visitor sends one chat message:", muted=True)
steps = [
    ("Visitor types & sends", "The widget shows a typing bubble and POSTs { message, history[] } to /api/chat."),
    ("Endpoint receives request", "Extracts the message and prior turns. Empty message returns an instant greeting."),
    ("Greeting detection (no AI)", "'hi', 'hello', 'assalam o alaikum' etc. get a canned warm reply in the matching language."),
    ("Prompt-injection guard", "Phrases like 'ignore previous instructions' are blocked with a security notice."),
    ("Build the AI prompt", "The full knowledge base becomes the system instruction; last 10 turns are folded in for context."),
    ("Model cascade call", "Gemini is tried model-by-model (fastest first). An overloaded model (503) silently falls to the next."),
    ("Reply returns to browser", "The answer is rendered, added to history, and persisted to localStorage across refreshes."),
]
for i, (title_, desc) in enumerate(steps, 1):
    p = doc.add_paragraph()
    rn = p.add_run(f"{i}. {title_} — ")
    rn.font.bold = True
    rn.font.size = Pt(11)
    rn.font.color.rgb = BLUE
    rd = p.add_run(desc)

# ===================== 4. DEPLOYMENT =====================
h1("4. Deployment Topology")
para("Two ways the app runs. The frontend auto-detects the environment, so no code changes are needed between them.", muted=True)
h2("Production — Vercel")
table(
    ["Part", "Where it runs"],
    [
        ["Frontend site", "frontend/ served by Vercel CDN"],
        ["Chat API", "api/chat.py serverless function"],
        ["AI key", "GEMINI_API_KEY env var (Vercel)"],
        ["History", "Browser localStorage (per device)"],
        ["Trigger", "Push to main → auto-deploy + CI"],
    ],
    widths=[2.0, 4.4],
)
h2("Local Development")
table(
    ["Part", "Where it runs"],
    [
        ["Frontend site", "Open frontend/index.html"],
        ["Chat API", "FastAPI backend via start.bat"],
        ["AI key", ".env file (never committed)"],
        ["Database", "SQLite backend/sql_app.db"],
        ["API URL", "http://127.0.0.1:8000/api/chat"],
    ],
    widths=[2.0, 4.4],
)

# ===================== 5. COMPONENTS =====================
h1("5. Components")
table(
    ["Layer", "Key files", "Role"],
    [
        ["Frontend", "frontend/index.html, script.js, style.css", "Marketing site + chat widget; sends messages, renders replies, stores history."],
        ["Serverless API", "api/chat.py", "Production chat endpoint: greeting + security checks, context builder, model cascade."],
        ["FastAPI Backend", "backend/app/main.py, rag_engine.py, admin.py", "Full local backend with chat endpoint, RAG retrieval, and knowledge CRUD."],
        ["Knowledge Base", "knowledge_base.py", "Six division data blocks + brand aliases; feeds every AI prompt."],
        ["Database", "backend/app/database/ (SQLAlchemy + SQLite)", "Clients, assistants, business units, knowledge chunks."],
        ["AI Provider", "google-genai (Gemini Flash)", "Generates answers from a system-instruction prompt. Key via env var only."],
    ],
    widths=[1.3, 2.3, 2.8],
)

# ===================== 6. MODEL CASCADE =====================
h1("6. Resilient AI Model Cascade")
para("The API never depends on a single model. It tries a list in order and moves on if one is overloaded.", muted=True)
table(
    ["Order", "Model", "Role"],
    [
        ["1", "gemini-3.5-flash-lite", "Primary — fastest"],
        ["2", "gemini-2.5-flash", "Reliable fallback"],
        ["3", "gemini-flash-latest", "Fallback"],
        ["4", "gemini-3.5-flash", "Fallback"],
        ["5", "gemini-3.6-flash", "Fallback"],
        ["6", "gemini-3.8-flash", "Fallback"],
    ],
    widths=[0.8, 2.6, 3.0],
)

# ===================== 7. HISTORY =====================
h1("7. Conversation History")
h2("Client side (per device)")
para("Every message is appended to an array and saved to the browser's localStorage under "
     "'swiftsign-chat-history'. On page load, stored messages are re-rendered, so closing the tab "
     "doesn't lose the conversation. The Clear button empties both the view and storage.")
h2("Context to the AI")
para("The last 10 turns are sent with each request. The backend folds them into the prompt so follow-ups "
     "like 'what about their price?' are understood relative to the earlier question — then answered only "
     "from the knowledge base.")

# ===================== 8. REPOSITORY MAP =====================
h1("8. Repository Map")
tree = [
    "frontend/            the website + chat widget (deployed to Vercel)",
    "  index.html         page + widget markup",
    "  script.js          chat logic, history, API calls",
    "  style.css          theme & responsive layout",
    "api/                 Vercel serverless function (production API)",
    "  chat.py            greeting/security/context + model cascade",
    "  knowledge_base.py  copy of company data for the function",
    "backend/             full FastAPI backend (local + optional Render)",
    "  app/main.py        /api/chat endpoint + admin router",
    "  app/core/rag_engine.py   retrieval + Gemini call",
    "  app/database/      models + SQLite session",
    "  knowledge_base.py  ·  seed.py  ·  .env",
    "root                 config, deployment, docs",
    "  vercel.json · render.yaml · requirements.txt",
    "  start.bat · run.py · test_app.py · DEPLOY.md",
]
for line in tree:
    code(line)

# ===================== 9. TECH STACK =====================
h1("9. Tech Stack")
table(
    ["Layer", "Technology", "Role"],
    [
        ["Frontend", "HTML · CSS · Vanilla JS", "Marketing site + chat widget"],
        ["Hosting", "Vercel (CDN + Functions)", "Serves site & runs /api/chat"],
        ["API (prod)", "Python (BaseHTTPRequestHandler)", "Serverless chat endpoint"],
        ["API (local)", "FastAPI + Uvicorn", "Full backend + admin + docs"],
        ["AI", "Google Gemini (google-genai)", "Generates answers"],
        ["Data", "SQLAlchemy + SQLite", "Clients, assistants, knowledge"],
        ["Config", "python-dotenv", "Loads GEMINI_API_KEY"],
        ["CI", "GitHub Actions", "Runs tests on every push"],
    ],
    widths=[1.2, 2.6, 2.6],
)

# ===================== 10. API CONTRACT =====================
h1("10. API Contract — POST /api/chat")
h2("Request")
code('{\n  "message": "what about their price?",\n  "history": [\n    { "role": "user", "text": "Tell me about IT" },\n    { "role": "bot",  "text": "We offer..." }\n  ]\n}')
h2("Response")
code('{\n  "response": "Prices depend on...",\n  "answer":   "Prices depend on...",\n  "message":  "Prices depend on...",\n  "status":   "success"\n}')
para("The reply is duplicated across response / answer / message on purpose — the frontend accepts any of "
     "them, keeping older and newer clients compatible.", muted=True, size=10)

# ===================== SAVE =====================
out = "Swift_Sign_Architecture.docx"
doc.save(out)
print("Saved:", out)


