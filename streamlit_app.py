"""Fast evidence-first Groww SIP discovery app.

Uses a local BM25 text-ranking index and structured, evidence-led summaries.
No Ollama server, neural model download, LLM API, or API key is required.
"""
from __future__ import annotations

import csv
import html
import io
import math
import re
from collections import Counter
from pathlib import Path

import streamlit as st


ROOT = Path(__file__).resolve().parent
APP_REVIEWS_PATH = ROOT / "groww_sip_explicit_candidates.csv"
REDDIT_PATH = ROOT / "groww_sip_reddit_pilot.csv"
TOP_K = 5
MIN_SCORE = 1.0
GROWW_PLAY_STORE_URL = "https://play.google.com/store/apps/details?id=com.nextbillion.groww&hl=en_IN"
PROMPTS = [
    "What reasons do Groww reviewers give for pausing, reducing, or stopping an SIP?",
    "What problems do reviewers report with AutoPay, mandates, or SIP debits?",
    "What do reviewers say when their SIP payment, order status, or mutual fund units are unclear?",
    "What do users do outside Groww when they’re unsure whether an SIP payment went through?",
    "Are there positive SIP experiences that differ from the problem reports?",
    "Can these reviews tell us what separates investors with an active SIP after 12 months from those who stop?",
]
GUIDES = [
    (("pause", "skip", "instalment", "installment"), "Skip an SIP instalment", "https://groww.in/help/mutual-funds/mf-sip/how-to-skip-an-sip-instalment--79"),
    (("pause",), "Pause SIP for next month", "https://groww.in/help/mutual-funds/order/can-i-pause-sip-for-next-month"),
    (("cancel", "stop", "terminate", "mandate"), "Cancel an ongoing SIP", "https://groww.in/help/mutual-funds/mf-sip/how-to-cancel-my-sip"),
    (("autopay", "auto pay", "mandate", "debit", "payment", "failed"), "Troubleshoot AutoPay setup", "https://groww.in/help/my-account/payments/i-am-unable-to-set-up-autopay-via-my-bank-account--99"),
    (("unit", "allot", "allocated", "allocation"), "Paid but units are not allocated", "https://groww.in/help/mutual-funds/order/i-have-paid-but-mutual-fund-units-have-not-been-allocated-to-me-yet-3"),
    (("redeem", "redemption", "withdraw"), "Mutual fund redemption help", "https://groww.in/help/mutual-funds"),
]
STOP = set("what why how can could should would i me my the a an to for of in on with about please find show search tell does do is are was were and or us users customer customers investor investors groww review reviews these this those from after before who separates separate active months month years year give sips sip feature features option options issue issues problem problems report reports mention mentions people happens happen investors groww".split())
ALIASES = {
    "autopay": ("autopay", "autodebit", "mandate", "emandate", "upi", "bank"),
    "mandate": ("mandate", "autopay", "autodebit", "emandate", "upi"),
    "pause": ("pause", "skip", "hold", "stop", "temporarily"),
    "stop": ("stop", "cancel", "discontinue", "terminate", "close", "pause"),
    "cancel": ("cancel", "stop", "discontinue", "terminate", "close"),
    "payment": ("payment", "debit", "deduct", "instalment", "installment", "transaction"),
    "debit": ("debit", "deduct", "payment", "autodebit", "bank"),
    "unit": ("unit", "units", "allotment", "allocated", "allocation"),
    "redemption": ("redemption", "redeem", "withdraw", "withdrawal", "sell"),
    "redeem": ("redeem", "redemption", "withdraw", "withdrawal"),
    "stepup": ("stepup", "increase", "raise", "amount"),
    "increase": ("increase", "stepup", "raise", "amount", "change"),
    "crash": ("crash", "crashing", "glitch", "freeze", "hang", "error"),
    "support": ("support", "customercare", "complaint", "ticket", "resolve"),
    "reducing": ("reduce", "decrease", "lower", "stepdown", "amount"),
    "unclear": ("unclear", "missing", "delay", "pending", "status", "not visible"),
    "status": ("status", "pending", "processing", "confirmation", "order", "transaction"),
    "unsure": ("unsure", "uncertain", "check", "confirm", "status", "pending"),
    "outside": ("bank", "upi", "sms", "statement", "support"),
    "through": ("received", "confirmed", "status", "pending", "failed", "debit"),
}
THEMES = [
    ("AutoPay / mandate", re.compile(r"auto.?pay|auto.?debit|mandate|e.?mandate|upi mandate", re.I)),
    ("Payment / debit", re.compile(r"payment|debit|deduct|instal?lment|transaction|bank balance", re.I)),
    ("Pausing / cancellation", re.compile(r"pause|skip|cancel|stop|discontinu|terminate", re.I)),
    ("Units / allocation", re.compile(r"units?|allot|allocat", re.I)),
    ("Redemption / withdrawal", re.compile(r"redeem|redemption|withdraw|sell fund", re.I)),
    ("App reliability", re.compile(r"crash|glitch|bug|error|slow|hang|freeze|login", re.I)),
    ("Support / resolution", re.compile(r"support|customer care|complaint|ticket|response|resolve", re.I)),
    ("Amount changes / step-up", re.compile(r"step.?up|increase|decrease|change.*amount|amount.*change", re.I)),
]
OPPORTUNITIES = {
    "AutoPay / mandate": "Explore clearer mandate status, bank rejection reasons, and a guided retry path.",
    "Payment / debit": "Explore a payment timeline that explains debit status, retry timing, and the next action.",
    "Pausing / cancellation": "Explore making pause, skip, and cancellation states easy to distinguish and confirm.",
    "Units / allocation": "Explore showing payment-to-allotment status and expected next update in one place.",
    "Redemption / withdrawal": "Explore a clearer redemption tracker with stage, expected timing, and any action needed.",
    "App reliability": "Explore surfacing service status and protecting SIP tasks from app interruptions.",
    "Support / resolution": "Explore linking a complaint to a visible owner, status, and expected response time.",
    "Amount changes / step-up": "Explore a clear preview and confirmation of the next SIP amount and effective date.",
}

st.set_page_config(page_title="Groww SIP AI Discovery Engine", page_icon="✳", layout="wide")
st.markdown("""
<style>
:root{--bg:#0B0E11;--card:#171C22;--text:#FFFFFF;--muted:#8A9CAE;--blue:#5367F5;--neon:#08F6B6;--positive:#00D09C;--negative:#FF003C;--line:#303943}
.block-container{width:100%;max-width:none;padding:1.4rem clamp(1.2rem,2.3vw,2.6rem) 1.5rem!important}
html,body,[data-testid="stAppViewContainer"]{font-size:18px!important;background:var(--bg)!important;color:var(--text)!important}
[data-testid="stHeader"]{background:rgba(11,14,17,.96)!important}
[data-testid="stSidebar"]{background:#10151B;min-width:300px!important;max-width:300px!important;border-right:1px solid var(--line)}
[data-testid="stMarkdownContainer"] p,[data-testid="stMarkdownContainer"] li{font-size:1.04rem!important;line-height:1.62!important;color:var(--text)}
[data-testid="stMarkdownContainer"] h1,[data-testid="stMarkdownContainer"] h2,[data-testid="stMarkdownContainer"] h3{color:var(--text)!important}
[data-testid="stMarkdownContainer"] h1{font-size:2rem!important;line-height:1.2!important}
[data-testid="stMarkdownContainer"] h2{font-size:1.5rem!important}
[data-testid="stMarkdownContainer"] h3{font-size:1.18rem!important}
[data-testid="stCaptionContainer"] p{font-size:.92rem!important;line-height:1.5!important;color:var(--muted)!important}
[data-testid="stTextInput"] input,[data-testid="stTextArea"] textarea{font-size:1rem!important;min-height:46px!important;background:var(--card)!important;color:var(--text)!important;border-color:var(--line)!important}
div.stButton>button,div.stFormSubmitButton>button{font-size:.96rem!important;min-height:42px!important;border-radius:10px!important;background:var(--blue)!important;color:#fff!important;border:1px solid var(--blue)!important}
div.stButton>button:hover,div.stFormSubmitButton>button:hover{border-color:var(--neon)!important;color:var(--neon)!important}
[data-testid="stSidebar"] div.stButton>button{white-space:normal!important;text-align:left!important;line-height:1.28!important;padding:.36rem .58rem!important;font-size:.88rem!important;min-height:35px!important;background:var(--card)!important;color:var(--text)!important;border:1px solid var(--line)!important}
[data-testid="stSidebar"] div.stButton>button:hover{border-color:var(--neon)!important;color:var(--neon)!important}
.hero{padding:1.25rem 1.5rem;border-radius:18px;background:linear-gradient(120deg,#171C22,#11171D);border:1px solid #303943;border-left:4px solid var(--neon);margin-bottom:1rem}
.hero h1{font-size:2.05rem!important;margin:0 0 .4rem!important;color:var(--text);line-height:1.2}
.hero p{font-size:1rem!important;margin:0;color:var(--muted)}
.source-card{border:1px solid var(--line);border-left:4px solid var(--neon);border-radius:12px;padding:.85rem;margin:.65rem 0;background:var(--card);overflow-wrap:anywhere;box-sizing:border-box;width:100%}
.small-muted{font-size:.9rem;color:var(--muted)}
.empty-state{margin-top:2rem;padding:2.2rem 1.5rem;border:1px dashed #3b4651;border-radius:18px;background:var(--card);text-align:center}
.empty-state h3{font-size:1.35rem!important;color:var(--text);margin:.4rem 0}
.empty-state p{max-width:560px;margin:0 auto;color:var(--muted)}
.empty-icon{font-size:2rem;color:var(--neon)}
[data-testid="stMetric"]{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:.8rem 1rem}
[data-testid="stMetricLabel"] p{font-size:.88rem!important;color:var(--muted)!important}
[data-testid="stMetricValue"]{font-size:1.8rem!important;color:var(--neon)!important}
.question-card{padding:1rem 1.1rem;margin:.7rem 0 1rem;border-radius:15px;background:var(--card);border-left:4px solid var(--neon)}
.question-card span{display:block;font-size:.75rem;font-weight:700;letter-spacing:.08em;color:var(--muted);margin-bottom:.35rem}
.question-card strong{font-size:1.08rem;color:var(--text);line-height:1.45}
.quote-card{border:1px solid var(--line);border-radius:14px;padding:1rem 1.1rem;background:var(--card);line-height:1.6;color:var(--text)}
.upload-box{padding:.8rem;border:1px solid #3b4651;border-radius:14px;background:var(--card);margin:.25rem 0 .8rem;color:var(--text)}
.ref-number{color:var(--neon);font-weight:800;letter-spacing:.03em}
.references-title{position:relative;top:auto;z-index:auto;padding:.55rem .8rem .75rem;margin:.35rem 0 .65rem;background:#0B0E11;border-bottom:2px solid var(--neon);color:#fff;font-size:1.3rem;font-weight:800;line-height:1.35;letter-spacing:.02em}
[data-testid="stExpander"]{background:var(--card)!important;border:1px solid var(--line)!important;border-radius:12px!important}
[data-testid="stExpander"] summary,[data-testid="stExpander"] summary p{color:var(--text)!important}
[data-testid="stFileUploaderDropzone"]{background:var(--card)!important;border:1px dashed var(--neon)!important}
[data-testid="stFileUploaderDropzone"] button{background:var(--blue)!important;color:#fff!important}
[data-baseweb="notification"]{background:var(--card)!important;color:var(--text)!important}
a{color:var(--neon)!important}
hr{border-color:var(--line)!important}
@media(max-width:900px){.block-container{padding:1rem!important}[data-testid="stSidebar"]{min-width:250px!important;max-width:250px!important}.hero h1{font-size:1.7rem!important}}
</style>
""", unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def read_csv(path: str) -> list[dict]:
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def tokenize(text: str) -> list[str]:
    text = re.sub(r"auto[\s-]?pay", "autopay", text.lower())
    text = re.sub(r"auto[\s-]?debit", "autodebit", text)
    text = re.sub(r"e[\s-]?mandate", "emandate", text)
    text = re.sub(r"step[\s-]?up", "stepup", text)
    tokens = re.findall(r"[a-z0-9]+", text)
    normalized = []
    for token in tokens:
        if token.endswith("ies") and len(token) > 4:
            token = token[:-3] + "y"
        elif token.endswith(("ing", "ed")) and len(token) > 5:
            token = token[:-3]
        elif token.endswith("s") and not token.endswith("ss") and len(token) > 3:
            token = token[:-1]
        if len(token) > 1 and token not in STOP and not token.isdigit():
            normalized.append(token)
    return normalized


def row_text(row: dict) -> str:
    return " ".join(str(row.get(k, "") or "") for k in ("content", "matched_terms", "relevance_reason", "scope"))


@st.cache_resource(show_spinner=False)
def get_index() -> tuple[list[dict], list[Counter], Counter, float, int]:
    app_rows = read_csv(str(APP_REVIEWS_PATH))
    reddit_rows = read_csv(str(REDDIT_PATH))
    rows: list[dict] = []
    for raw in app_rows:
        if (raw.get("content") or "").strip():
            rows.append({"content": raw.get("content", ""), "source_id": raw.get("reviewId", ""), "source_url": GROWW_PLAY_STORE_URL, "source": "Groww app review dataset", "published_at": raw.get("at", ""), "rating": raw.get("score", ""), "app_version": raw.get("appVersion", ""), "subreddit": "", "matched_terms": raw.get("matched_terms", ""), "scope": "Groww review corpus", "_kind": "app"})
    for raw in reddit_rows:
        if (raw.get("content") or "").strip():
            rows.append({"content": raw.get("content", ""), "source_id": raw.get("source_id", ""), "source_url": raw.get("source_url", ""), "source": raw.get("subreddit", "Reddit"), "published_at": raw.get("published_at", ""), "rating": "", "app_version": "", "subreddit": raw.get("subreddit", "Reddit"), "matched_terms": raw.get("relevance_reason", ""), "scope": raw.get("scope", "Public discussion"), "_kind": "public"})
    docs = [Counter(tokenize(row_text(row))) for row in rows]
    df: Counter = Counter()
    for doc in docs:
        df.update(doc.keys())
    avg_len = sum(sum(doc.values()) for doc in docs) / max(len(docs), 1)
    return rows, docs, df, avg_len, len(docs)


def expand_query(question: str) -> list[str]:
    terms = tokenize(question)
    expanded: list[str] = []
    for term in terms:
        aliases = ALIASES.get(term, (term,))
        # Original words receive extra weight; aliases broaden wording without
        # allowing one synonym to dominate the ranking.
        expanded.extend([term, term])
        expanded.extend(alias for alias in aliases if alias != term)
    return list(dict.fromkeys(expanded))


def bm25_score(query: list[str], doc: Counter, df: Counter, total_docs: int, avg_len: float) -> float:
    k1, b = 1.5, 0.75
    doc_len = sum(doc.values())
    score = 0.0
    for term in query:
        tf = doc.get(term, 0)
        if not tf:
            continue
        freq = df.get(term, 0)
        idf = math.log(1.0 + (total_docs - freq + 0.5) / (freq + 0.5))
        denom = tf + k1 * (1 - b + b * doc_len / max(avg_len, 1))
        score += idf * (tf * (k1 + 1) / denom)
    return score


def upload_rows(upload) -> list[dict]:
    if upload is None:
        return []
    if upload.size > 20 * 1024 * 1024:
        raise ValueError("CSV must be 20 MB or smaller.")
    table = list(csv.DictReader(io.StringIO(upload.getvalue().decode("utf-8-sig", errors="replace"))))
    if not table:
        raise ValueError("The CSV has no data rows.")
    headers = {re.sub(r"[^a-z0-9]+", "_", k.lower()).strip("_"): k for k in table[0]}
    text_key = next((headers[k] for k in ("user_statement", "content", "text", "review", "review_text", "body", "comment") if k in headers), None)
    if not text_key:
        raise ValueError("Add a text column named user_statement, content, text, review, or comment.")
    id_key = next((headers[k] for k in ("id", "review_id", "source_id") if k in headers), None)
    url_key = next((headers[k] for k in ("url", "source_url", "review_url") if k in headers), None)
    source_key = next((headers[k] for k in ("source", "platform", "source_platform") if k in headers), None)
    date_key = next((headers[k] for k in ("date", "published_at", "created_at") if k in headers), None)
    rows = []
    for i, raw in enumerate(table[:5000]):
        text = (raw.get(text_key) or "").strip()
        if text:
            rows.append({"content": text, "source_id": (raw.get(id_key) or f"upload-{i+1}") if id_key else f"upload-{i+1}", "source_url": raw.get(url_key, "") if url_key else "", "source": raw.get(source_key, "Uploaded CSV") if source_key else "Uploaded CSV", "published_at": raw.get(date_key, "") if date_key else "", "rating": "", "app_version": "", "subreddit": "", "matched_terms": "", "scope": "User-uploaded feedback", "_kind": "custom"})
    return rows


def retrieve(question: str, custom: list[dict]) -> tuple[list[dict], int]:
    rows, docs, df, avg_len, total_docs = get_index()
    query = expand_query(question)
    if not query:
        return [], 0
    extra_docs = [Counter(tokenize(row_text(row))) for row in custom]
    all_rows = rows + custom
    all_docs = docs + extra_docs
    if extra_docs:
        extra_df: Counter = Counter()
        for doc in extra_docs:
            extra_df.update(doc.keys())
        combined_df = df + extra_df
        combined_total = total_docs + len(extra_docs)
        combined_avg = (avg_len * total_docs + sum(sum(d.values()) for d in extra_docs)) / max(combined_total, 1)
    else:
        combined_df, combined_total, combined_avg = df, total_docs, avg_len
    comparison_question = bool(re.search(r"\bpositive\b|\bdiffer\b|\bproblem reports\b", question, re.I))
    if comparison_question:
        sip_related = re.compile(r"\bsips?\b|systematic.{0,20}investment|mutual funds?|auto.?pay|mandate|instal?lment", re.I)
        positive_terms = tokenize("good great easy simple convenient reliable smooth excellent satisfied works well positive")
        problem_terms = tokenize("problem issue failed failure error delay difficult complaint poor unable missing not working debit")
        groups = [("higher-rated SIP-related reviews (4–5 stars)", "positive", 4, positive_terms), ("lower-rated SIP-related reviews (1–2 stars)", "problem", 2, problem_terms)]
        comparison_matches = []
        comparison_total = 0
        for label, group, threshold, extra_terms in groups:
            pool = []
            for row, doc in zip(rows, docs):
                rating = str(row.get("rating", ""))
                try:
                    rating_value = int(float(rating))
                except (TypeError, ValueError):
                    continue
                if (group == "positive" and rating_value < threshold) or (group == "problem" and rating_value > threshold):
                    continue
                if not sip_related.search(row.get("content", "")):
                    continue
                score = bm25_score(query + extra_terms, doc, df, total_docs, avg_len)
                if score >= MIN_SCORE:
                    item = dict(row)
                    item["_score"] = score
                    item["_sentiment_group"] = label
                    pool.append(item)
            pool.sort(key=lambda item: (item["_score"], str(item.get("published_at", ""))), reverse=True)
            comparison_total += len(pool)
            comparison_matches.extend(pool[:3])
        return comparison_matches, comparison_total

    matches = []
    for row, doc in zip(all_rows, all_docs):
        score = bm25_score(query, doc, combined_df, combined_total, combined_avg)
        if score >= MIN_SCORE:
            item = dict(row)
            item["_score"] = score
            matches.append(item)
    matches.sort(key=lambda item: (item["_score"], str(item.get("published_at", ""))), reverse=True)
    return matches[:TOP_K], len(matches)


def theme_counts(matches: list[dict]) -> list[tuple[str, int]]:
    found = []
    for label, pattern in THEMES:
        count = sum(bool(pattern.search(row.get("content", ""))) for row in matches)
        if count:
            found.append((label, count))
    return sorted(found, key=lambda item: (-item[1], item[0]))[:4]


def summary(question: str, matches: list[dict], total_matches: int) -> str:
    if not matches:
        return "I couldn't find clear matching customer evidence for this question in the available corpus. Try a specific SIP issue such as AutoPay, a missed debit, pausing, cancellation, unit allocation, or redemption."
    if any(row.get("_sentiment_group") for row in matches):
        higher = [row for row in matches if row.get("_sentiment_group", "").startswith("higher-rated")]
        lower = [row for row in matches if row.get("_sentiment_group", "").startswith("lower-rated")]
        lines = ["Comparison of retrieved SIP-related Groww app reviews:"]
        lines.append(f"• Higher-rated examples (4–5 stars): {len(higher)} selected")
        lines.append(f"• Lower-rated examples (1–2 stars): {len(lower)} selected")
        for label, group in (("Higher-rated example", higher), ("Lower-rated example", lower)):
            if group:
                excerpt = re.sub(r"\s+", " ", group[0].get("content", "")).strip()
                if len(excerpt) > 220:
                    excerpt = excerpt[:217].rsplit(" ", 1)[0] + "…"
                lines.append(f"\n{label} (rating {group[0].get('rating')}/5): “{excerpt}”")
        lines.append("\nStar ratings reflect each reviewer's overall app rating, not a verified rating of their SIP experience. These retrieved examples are illustrative, not a representative comparison or proof of why investors continue or stop.")
        return "\n".join(lines)
    themes = theme_counts(matches)
    lines = [f"Here are the {len(matches)} strongest evidence records retrieved for this question."]
    if themes:
        lines.append("\nSignals in these selected examples (counts are within this retrieved set, not all Groww customers):")
        lines.extend(f"• {label}: {count} record(s)" for label, count in themes)
    first = matches[0]
    excerpt = re.sub(r"\s+", " ", first.get("content", "")).strip()
    if len(excerpt) > 260:
        excerpt = excerpt[:257].rsplit(" ", 1)[0] + "…"
    source_kind = {"app": "Groww app review", "public": "public discussion", "custom": "uploaded feedback"}.get(first.get("_kind"), "feedback record")
    lines.append(f"\nRepresentative example (R01 · {source_kind}): “{excerpt}”")
    if themes and themes[0][0] in OPPORTUNITIES:
        lines.append(f"\nOpportunity to investigate (hypothesis): {OPPORTUNITIES[themes[0][0]]}")
    lines.append("\nThese are retrieved examples, not a representative sample or proof of cause.")
    return "\n".join(lines)


if "current_result" not in st.session_state:
    st.session_state.current_result = None
if "pending_question" not in st.session_state:
    st.session_state.pending_question = ""
if "question" not in st.session_state:
    st.session_state.question = ""

with st.sidebar:
    st.markdown("## ✳ Groww SIP Discovery")
    st.caption("AI Discovery Engine · customer evidence")
    if st.button("＋ New research", use_container_width=True):
        st.session_state.current_result = None
        st.session_state.pending_question = ""
        st.session_state.question = ""
        st.rerun()
    st.markdown("#### Upload your feedback CSV")
    st.caption("Try the engine with your own reviews. Upload is optional.")
    st.markdown("<div class='upload-box'><b>Choose or drop a CSV</b><br><span class='small-muted'>Text column: user_statement, content, text, or review.</span></div>", unsafe_allow_html=True)
    uploaded = st.file_uploader("Choose a CSV", type=["csv"], help="Up to 20 MB. Text column: user_statement, content, text, or review. Avoid sensitive personal information.")
    try:
        custom_rows = upload_rows(uploaded)
        if uploaded:
            st.success(f"Loaded {len(custom_rows):,} feedback rows for this browser session")
    except (ValueError, UnicodeError) as exc:
        custom_rows = []
        st.error(str(exc))
    st.caption("Your uploaded feedback stays in this browser session.")
    st.markdown("#### Research questions")
    for i, prompt in enumerate(PROMPTS):
        if st.button(prompt, key=f"prompt_{i}", use_container_width=True):
            st.session_state.question = prompt
            st.session_state.pending_question = prompt
            st.session_state.current_result = None

main, right = st.columns([2.7, 1.2], gap="large")
with main:
    st.markdown("<div class='hero'><h1>Groww SIP Discovery</h1><p>Explore customer feedback, spot recurring friction, and inspect the evidence behind each finding.</p></div>", unsafe_allow_html=True)
    try:
        app_n = sum(bool((row.get("content") or "").strip()) for row in read_csv(str(APP_REVIEWS_PATH)))
        public_n = sum(bool((row.get("content") or "").strip()) for row in read_csv(str(REDDIT_PATH)))
        st.caption(f"Evidence available: {app_n:,} Groww review records · {public_n} source-linked public discussions" + (f" · {len(custom_rows):,} uploaded records" if custom_rows else ""))
    except (OSError, csv.Error) as exc:
        st.error(f"Could not load the bundled evidence files: {exc}")
    question_from_form = ""
    with st.form("question_form", clear_on_submit=False):
        typed = st.text_input("Ask a research question", key="question", placeholder="Ask about SIP setup, AutoPay, missed payments, pausing, or redemption…")
        submitted = st.form_submit_button("Find evidence and summarize", use_container_width=True)
        if submitted:
            question_from_form = typed.strip()
    if question_from_form:
        st.session_state.pending_question = question_from_form
        st.session_state.current_result = None
    if st.session_state.pending_question:
        pending = st.session_state.pending_question
        if len(pending) > 500:
            st.error("Keep the question under 500 characters.")
        elif not pending:
            st.info("Type a research question first.")
        else:
            try:
                results, count = retrieve(pending, custom_rows)
                answer = summary(pending, results, count)
                st.session_state.current_result = {"question": pending, "answer": answer, "matches": results, "count": count}
                st.session_state.pending_question = ""
                st.rerun()
            except Exception as exc:
                st.error(f"Evidence search could not complete: {exc}")
    result = st.session_state.current_result
    if result:
        st.markdown("### Discovery brief")
        st.markdown(f"<div class='question-card'><span>RESEARCH QUESTION</span><strong>{html.escape(result['question'])}</strong></div>", unsafe_allow_html=True)
        matches = result["matches"]
        asks_retention = bool(re.search(r"\b(12\s*months?|12-month|one year|retention|churn|stay(?:ing)? active|active sip after)\b", result["question"], re.I))
        asks_positive_comparison = bool(re.search(r"\bpositive\b|\bdiffer\b|\bproblem reports\b", result["question"], re.I))
        if asks_retention:
            st.warning("Evidence limit: these reviews and public discussions do not track the same investors over time or report each person's SIP status after 12 months. They cannot show what separates retained investors from those who stop. The examples below are adjacent qualitative signals only.")
        app_matches = sum(row.get("_kind") == "app" for row in matches)
        public_matches = sum(row.get("_kind") == "public" for row in matches)
        custom_matches = sum(row.get("_kind") == "custom" for row in matches)
        m1, m2, m3 = st.columns(3)
        m1.metric("Evidence examples", len(matches))
        m2.metric("Public discussions", public_matches)
        m3.metric("Groww reviews / uploads", app_matches + custom_matches)
        if matches:
            themes = theme_counts(matches)
            if themes:
                st.markdown("#### Patterns in the retrieved examples")
                theme_cols = st.columns(min(3, len(themes)))
                for i, (label, count) in enumerate(themes):
                    theme_cols[i % len(theme_cols)].metric(label, f"{count} of {len(matches)}")
                st.caption("A record can appear in more than one theme. These counts describe only the examples shown.")
            first = matches[0]
            source_kind = {"app": "Groww app review", "public": "Public discussion", "custom": "Uploaded feedback"}.get(first.get("_kind"), "Feedback record")
            quote = html.escape(re.sub(r"\s+", " ", first.get("content", "")).strip())
            st.markdown("#### Representative feedback")
            st.markdown(f"<div class='quote-card'>“{quote}”<br><span class='small-muted'><b>R01</b> · {source_kind}</span></div>", unsafe_allow_html=True)
            if themes and themes[0][0] in OPPORTUNITIES and not asks_retention and not asks_positive_comparison:
                st.markdown("#### Opportunity to investigate")
                st.info(OPPORTUNITIES[themes[0][0]])
                st.caption("A hypothesis suggested by these examples—not a validated solution. Test it with users before prioritizing.")
            elif asks_retention:
                st.markdown("#### Data gap to close")
                st.info("To compare SIP continuation after 12 months, link a consented cohort's start date to later active, paused, or stopped status, then validate the reasons through interviews.")
        else:
            st.info(result["answer"])
        st.caption("These records are discovery signals, not a representative sample or proof of cause.")
    else:
        st.markdown("<div class='empty-state'><div class='empty-icon'>✳</div><h3>Start with a research question</h3><p>Upload your feedback from the left, choose a prompt, or ask about a specific SIP experience. Matching evidence and source links will appear here.</p></div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='references-title'>References</div>", unsafe_allow_html=True)
    if not result:
        st.caption("Evidence references appear here after a search.")
    else:
        latest = result
        matches = latest["matches"]
        st.caption(f"Top {len(matches)} evidence examples for this question")
        if not matches:
            st.caption("No customer evidence matched strongly enough to cite.")
        for i, row in enumerate(matches):
            kind = row.get("_kind")
            if kind == "app":
                label = "Groww app review"
                provenance = f"Original review ID: {row.get('source_id') or 'not provided'}"
            elif kind == "public":
                label = row.get("subreddit") or "Public discussion"
                provenance = f"Original post ID: {row.get('source_id') or 'not provided'}"
            else:
                label = row.get("source") or "Uploaded feedback"
                provenance = f"Uploaded record ID: {row.get('source_id') or 'not provided'}"
            source_id = str(row.get("source_id") or "not provided")
            short_id = source_id[:12] + ("…" if len(source_id) > 12 else "")
            ref_code = f"R{i + 1:02d}"
            with st.expander(f"{ref_code} · {label}", expanded=(i == 0)):
                st.caption(f"{ref_code} · {provenance}")
                st.write(row.get("content", ""))
                if row.get("rating"):
                    st.caption(f"Rating: {row['rating']} / 5")
                url = row.get("source_url", "")
                if kind == "public" and url.startswith(("https://", "http://")):
                    st.link_button("Open original Reddit post ↗", url, use_container_width=True)
                elif kind == "app":
                    st.link_button("Open Groww on Google Play ↗", GROWW_PLAY_STORE_URL, use_container_width=True)
                elif kind == "custom" and url.startswith(("https://", "http://")):
                    st.link_button("Open uploaded source ↗", url, use_container_width=True)
        question_terms = set(tokenize(latest["question"]))
        relevant = [g for g in GUIDES if any(term in question_terms or term in latest["question"].lower() for term in g[0])]
        if relevant:
            with st.expander("Official Groww guidance", expanded=False):
                for _, title, url in relevant:
                    st.markdown(f"[{title} ↗]({url})")

