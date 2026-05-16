"""
Tugas 4 - Pemerolehan Informasi dan Penambangan Teks
Search Engine + Peringkasan Teks Extractive (TF-IDF From Scratch)

"""

import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime
from html import escape
from pathlib import Path
from urllib.parse import quote

import streamlit as st


# ═══════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════

st.set_page_config(
    page_title="INFO Search",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ═══════════════════════════════════════════════════════════
# PATH CONFIG
# ═══════════════════════════════════════════════════════════

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CORPUS_FILE = DATA_DIR / "corpus.txt"

DATA_DIR.mkdir(parents=True, exist_ok=True)


# ═══════════════════════════════════════════════════════════
# APP CONFIG
# ═══════════════════════════════════════════════════════════

EXAMPLES = [
    "gula darah diabetes insulin",
    "vaksin campak imunisasi anak",
    "kanker kemoterapi tumor",
    "kolesterol jantung lemak",
]

TOP_K = 10
TOP_SUMMARIZE = 3
TOP_SENTENCES = 3


# ═══════════════════════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════════════════════

st.markdown(
    """
<style>
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"], .stApp {
    background: #fff !important;
    color: #202124;
    font-family: arial, sans-serif;
}

#MainMenu, footer, header { visibility: hidden; }
section[data-testid="stSidebar"] { display: none; }

.block-container {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}

/* Search input */
.stTextInput > label { display: none !important; }
.stTextInput > div { margin-bottom: 0 !important; }

.stTextInput > div > div {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}

.stTextInput > div > div > input {
    border: 1px solid #dfe1e5 !important;
    border-radius: 24px !important;
    padding: 10px 20px !important;
    font-size: 16px !important;
    color: #202124 !important;
    background: #fff !important;
    box-shadow: none !important;
    outline: none !important;
    font-family: arial, sans-serif !important;
    height: 44px !important;
}

.stTextInput > div > div > input:hover,
.stTextInput > div > div > input:focus {
    box-shadow: 0 1px 6px rgba(32,33,36,.28) !important;
    border-color: rgba(223,225,229,0) !important;
}

.stTextInput > div > div > input::placeholder {
    color: #9aa0a6 !important;
}

/* Button umum */
.stButton {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

.stButton > button {
    background: #f8f9fa !important;
    color: #3c4043 !important;
    border: 1px solid #dadce0 !important;
    border-radius: 6px !important;
    font-family: arial, sans-serif !important;
    font-size: 14px !important;
    font-weight: 400 !important;
    padding: 8px 18px !important;
    width: auto !important;
    min-width: 84px !important;
    height: 44px !important;
    margin-top: 0 !important;
    white-space: nowrap !important;
}

.stButton > button:hover {
    border-color: #dadce0 !important;
    box-shadow: 0 1px 3px rgba(60,64,67,.3) !important;
    color: #202124 !important;
    background: #f8f9fa !important;
}

/* Logo */
.logo {
    font-weight: 700;
    letter-spacing: -1px;
    line-height: 1;
    font-family: arial, sans-serif;
    text-align: center;
}

.logo a {
    text-decoration: none !important;
}

/* Contoh query chip: pakai anchor supaya browser Back bisa bekerja */
.example-chip-wrap {
    max-width: 720px;
    margin: 10px auto 0;
}

.example-chip-row {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 24px;
    flex-wrap: wrap;
    width: 100%;
}

.example-chip {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-height: 48px;
    padding: 0 28px;
    background: #fff;
    color: #202124 !important;
    border: 1px solid #dfe1e5;
    border-radius: 8px;
    font-size: 14px;
    text-decoration: none !important;
    white-space: nowrap;
}

.example-chip:hover {
    background: #f8f9fa;
    border-color: #dadce0;
    box-shadow: 0 1px 3px rgba(60,64,67,.15);
}

/* Footer */
.page-footer {
    font-size: 12px;
    color: #70757a;
    text-align: center;
    margin-top: 48px;
    padding-top: 12px;
    border-top: 1px solid #efefef;
    width: 100%;
}

/* Results */
.results-count { font-size: 13px; color: #70757a; margin: 12px 0 20px; }
.result-item { padding: 16px 0; }
.result-rank { font-size: 11px; color: #9aa0a6; margin-bottom: 2px; }
.result-url { font-size: 13px; color: #202124; margin-bottom: 2px; }

.result-title {
    font-size: 20px;
    color: #1a0dab;
    font-weight: 400;
    line-height: 1.3;
    margin-bottom: 4px;
    cursor: pointer;
}

.result-title:hover { text-decoration: underline; }

.result-score {
    display: inline-block;
    font-size: 11px;
    color: #70757a;
    background: #f1f3f4;
    border-radius: 10px;
    padding: 2px 8px;
    margin-bottom: 8px;
}

.result-snippet {
    font-size: 14px;
    color: #4d5156;
    line-height: 1.58;
}

.summary-label {
    font-size: 11px;
    color: #1a73e8;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .06em;
    margin-bottom: 8px;
    display: block;
}

.sent-row {
    display: grid;
    grid-template-columns: 34px 1fr;
    gap: 0 8px;
    margin-bottom: 8px;
    align-items: baseline;
}

.sent-num { font-size: 11px; color: #9aa0a6; text-align: right; }
.sent-body { font-size: 14px; color: #4d5156; line-height: 1.58; }
.sent-score { font-size: 11px; color: #9aa0a6; margin-left: 4px; }

.result-divider {
    border: none;
    border-top: 1px solid #efefef;
    margin: 0;
}

.no-results { font-size: 16px; color: #202124; padding: 24px 0 8px; }

.no-results-sub {
    font-size: 14px;
    color: #70757a;
    line-height: 1.7;
}
</style>
""",
    unsafe_allow_html=True,
)


# ═══════════════════════════════════════════════════════════
# ENGINE
# ═══════════════════════════════════════════════════════════

def clean_article_text(text: str) -> str:
    """Membersihkan artefak umum dari artikel berita."""
    noise_patterns = [
        r"ADVERTISEMENT\s+SCROLL TO CONTINUE WITH CONTENT",
        r"\[Gambas:.*?\]",
    ]

    for pattern in noise_patterns:
        text = re.sub(pattern, " ", text, flags=re.IGNORECASE | re.DOTALL)

    text = re.sub(r"\s+", " ", text)
    return text.strip()


def preprocess(text, sw, stem):
    """Lowercase, hapus karakter non-alfanumerik, stopword removal, stemming."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = sw.remove(text)
    text = stem.stem(text)
    return [token for token in text.split() if len(token) >= 3]


def split_sentences(text):
    """Memecah artikel menjadi kalimat. Indeks kalimat dimulai dari 0."""
    raw_sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [
        (idx, sentence.strip())
        for idx, sentence in enumerate(raw_sentences)
        if len(sentence.strip()) > 20
    ]


def parse_corpus(filepath):
    """Parsing corpus berformat tag <DOC>, <ID>, <NIM>, <TITLE>, <URL>, <TEXT>."""
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    docs = []

    for block in re.findall(r"<DOC>(.*?)</DOC>", content, re.DOTALL | re.IGNORECASE):
        def get_tag(tag):
            match = re.search(
                rf"<{tag}>(.*?)</{tag}>",
                block,
                re.DOTALL | re.IGNORECASE,
            )
            return match.group(1).strip() if match else ""

        doc_id = get_tag("ID")
        text = get_tag("TEXT")

        if doc_id and text:
            docs.append(
                {
                    "id": doc_id,
                    "nim": get_tag("NIM"),
                    "title": get_tag("TITLE"),
                    "url": get_tag("URL"),
                    "text": clean_article_text(text),
                }
            )

    if not docs:
        raise ValueError(
            "Corpus berhasil dibaca, tetapi tidak ada dokumen valid. "
            "Pastikan corpus memakai tag <DOC>, <ID>, dan <TEXT>."
        )

    return docs


def build_engine(docs, sw, stem):
    """Membangun inverted index, token dokumen, dan TF-IDF matrix from scratch."""
    inverted_index = defaultdict(dict)
    document_tokens = {}
    num_docs = len(docs)

    for doc in docs:
        tokens = preprocess(doc["title"] + " " + doc["text"], sw, stem)
        document_tokens[doc["id"]] = tokens

        for term, freq in Counter(tokens).items():
            inverted_index[term][doc["id"]] = freq

    inverted_index = dict(inverted_index)
    tfidf_matrix = {}

    for doc in docs:
        doc_id = doc["id"]
        tokens = document_tokens[doc_id]
        tfidf_matrix[doc_id] = {}

        for term in set(tokens):
            count = tokens.count(term)
            tf = 1 + math.log10(count) if count > 0 else 0.0
            df = len(inverted_index.get(term, {}))
            idf = math.log10(num_docs / df) if df > 0 else 0.0
            tfidf_matrix[doc_id][term] = tf * idf

    return inverted_index, document_tokens, tfidf_matrix


@st.cache_resource(show_spinner=False)
def load_engine_cached(corpus_path: str, modified_time: float):
    """
    Cache engine agar:
    - klik contoh query tidak perlu memuat indeks ulang;
    - browser Back/Forward tetap aman;
    - refresh halaman tidak langsung mengulang komputasi selama corpus tidak berubah.
    """
    from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
    from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

    sw = StopWordRemoverFactory().create_stop_word_remover()
    stem = StemmerFactory().create_stemmer()

    docs = parse_corpus(Path(corpus_path))
    inv, dtok, tfidf = build_engine(docs, sw, stem)

    with open(DATA_DIR / "inverted_index.json", "w", encoding="utf-8") as file:
        json.dump(inv, file, ensure_ascii=False, indent=2)

    with open(DATA_DIR / "tfidf_matrix.json", "w", encoding="utf-8") as file:
        json.dump(tfidf, file, ensure_ascii=False, indent=2)

    with open(DATA_DIR / "document_tokens.json", "w", encoding="utf-8") as file:
        json.dump(dtok, file, ensure_ascii=False, indent=2)

    return docs, inv, dtok, tfidf, sw, stem


def do_search(query, docs, dtok, tfidf, inv, sw, stem, top_k=10):
    """Pencarian dokumen dengan Vector Space Model dan cosine similarity."""
    num_docs = len(docs)
    query_tokens = preprocess(query, sw, stem)

    if not query_tokens:
        return []

    query_vector = {}

    for term in set(query_tokens):
        count = query_tokens.count(term)
        tf = 1 + math.log10(count) if count > 0 else 0.0
        df = len(inv.get(term, {}))
        idf = math.log10(num_docs / df) if df > 0 else 0.0
        query_vector[term] = tf * idf

    candidates = set()
    for term in query_tokens:
        candidates.update(inv.get(term, {}).keys())

    query_norm = math.sqrt(sum(value ** 2 for value in query_vector.values()))
    if query_norm == 0:
        return []

    scores = []

    for doc_id in candidates:
        doc_vector = tfidf.get(doc_id, {})
        common_terms = set(query_vector) & set(doc_vector)

        dot_product = sum(query_vector[t] * doc_vector[t] for t in common_terms)
        if dot_product == 0:
            continue

        doc_norm = math.sqrt(sum(value ** 2 for value in doc_vector.values()))
        if doc_norm == 0:
            continue

        scores.append((doc_id, dot_product / (query_norm * doc_norm)))

    scores.sort(key=lambda item: item[1], reverse=True)
    doc_map = {doc["id"]: doc for doc in docs}

    return [
        {
            "rank": idx + 1,
            "doc_id": doc_id,
            "score": score,
            "title": doc_map[doc_id].get("title", ""),
            "text": doc_map[doc_id].get("text", ""),
            "url": doc_map[doc_id].get("url", ""),
        }
        for idx, (doc_id, score) in enumerate(scores[:top_k])
    ]


def summarize(text, tfidf_vec, sw, stem, top_n=3):
    """Extractive summarization berbasis rata-rata skor TF-IDF kalimat."""
    sentences = split_sentences(text)

    if not sentences:
        return []

    scored_sentences = []

    for idx, sentence in sentences:
        tokens = preprocess(sentence, sw, stem)

        if not tokens:
            continue

        score = sum(tfidf_vec.get(token, 0) for token in tokens) / len(tokens)

        scored_sentences.append(
            {
                "index": idx,
                "sentence": sentence,
                "score": score,
            }
        )

    top_sentences = sorted(
        scored_sentences,
        key=lambda item: item["score"],
        reverse=True,
    )[:top_n]

    top_sentences.sort(key=lambda item: item["index"])
    return top_sentences


def save_search_summary_output(query, results, tfidf, sw, stem, output_path):
    """Menyimpan hasil pencarian dan ringkasan 3 dokumen teratas ke file TXT."""
    lines = []
    lines.append(f"Query: {query}")
    lines.append(f"Waktu generate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("HASIL PENCARIAN:")
    lines.append("")

    for result in results[:TOP_SUMMARIZE]:
        lines.append(f"{result['rank']}. {result['title']} | ID={result['doc_id']}")
        lines.append(f"Cosine Similarity: {result['score']:.6f}")

        summary = summarize(
            result["text"],
            tfidf.get(result["doc_id"], {}),
            sw,
            stem,
            TOP_SENTENCES,
        )

        if summary:
            for sentence in summary:
                lines.append(f"{sentence['sentence']} [{sentence['index']}]")
        else:
            lines.append("(Ringkasan tidak tersedia)")

        lines.append("")

    with open(output_path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))


# ═══════════════════════════════════════════════════════════
# UI HELPERS
# ═══════════════════════════════════════════════════════════

LOGO_COLORS = [
    ("#4285F4", "I"),
    ("#EA4335", "N"),
    ("#FBBC05", "F"),
    ("#4285F4", "O"),
]


def logo_html(size="72px", mb="32px", clickable=False):
    spans = "".join(
        f'<span style="color:{color}">{letter}</span>'
        for color, letter in LOGO_COLORS
    )

    if clickable:
        spans = f'<a href="/" target="_self">{spans}</a>'

    return (
        f'<div class="logo" style="font-size:{size};margin-bottom:{mb};">'
        f"{spans}</div>"
    )


def inject_center_css():
    st.markdown(
        """
<style>
.block-container {
    max-width: 920px !important;
    margin: 0 auto !important;
    padding: 0 20px !important;
    min-height: 100vh !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
}

.block-container > div,
.block-container > div > div[data-testid="stVerticalBlock"] {
    width: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
}

.block-container .stTextInput {
    width: 100% !important;
}
</style>
""",
        unsafe_allow_html=True,
    )


def render_footer():
    st.markdown(
        """
<div class="page-footer">
  PIPT · Tugas 4 · 2026 &nbsp;·&nbsp;
  Nicolas Gabriel Siahaan &nbsp;·&nbsp;
  Dzaky Rezandi &nbsp;·&nbsp;
  Rafly Januar Raharjo &nbsp;·&nbsp;
  M. Naufal Al Farizki
</div>
""",
        unsafe_allow_html=True,
    )


def set_query_param(query: str):
    st.query_params["q"] = query


def get_query_param() -> str:
    value = st.query_params.get("q", "")
    return value.strip() if isinstance(value, str) else ""


# ═══════════════════════════════════════════════════════════
# LOAD ENGINE
# ═══════════════════════════════════════════════════════════

if not CORPUS_FILE.exists():
    inject_center_css()
    st.markdown(logo_html(), unsafe_allow_html=True)
    st.error(
        f"File `{CORPUS_FILE}` tidak ditemukan. "
        "Taruh corpus.txt di folder data/corpus.txt lalu refresh."
    )
    st.stop()

with st.spinner("Memuat indeks TF-IDF dari corpus..."):
    docs, inv, dtok, tfidf, sw, stem = load_engine_cached(
        str(CORPUS_FILE),
        CORPUS_FILE.stat().st_mtime,
    )


# ═══════════════════════════════════════════════════════════
# ROUTING
# ═══════════════════════════════════════════════════════════

query = get_query_param()
mode = "results" if query else "home"


# ═══════════════════════════════════════════════════════════
# HOME PAGE
# ═══════════════════════════════════════════════════════════

if mode == "home":
    inject_center_css()

    st.markdown(logo_html("72px", "48px"), unsafe_allow_html=True)

    outer_cols = st.columns([1.4, 5.8, 1.4])

    with outer_cols[1]:
        inner_cols = st.columns([6, 1.2], gap="small")

        with inner_cols[0]:
            home_query_input = st.text_input(
                "q",
                placeholder="Cari apa saja…",
                label_visibility="collapsed",
                key="home_query_input",
            )

        with inner_cols[1]:
            home_search_clicked = st.button("Cari", key="go_home")

    if home_search_clicked and home_query_input.strip():
        set_query_param(home_query_input.strip())
        st.rerun()

    st.markdown(
        """
<div style="
    font-size:12px;
    color:#70757a;
    margin:36px 0 14px;
    text-align:center;
">
  Coba kueri ini:
</div>
""",
        unsafe_allow_html=True,
    )

    chip_1 = "".join(
        f'<a class="example-chip" href="/?q={quote(example)}" target="_self">{escape(example)}</a>'
        for example in EXAMPLES[:3]
    )

    chip_2 = (
        f'<a class="example-chip" href="/?q={quote(EXAMPLES[3])}" '
        f'target="_self">{escape(EXAMPLES[3])}</a>'
    )

    st.markdown(
        f"""
<div class="example-chip-wrap">
  <div class="example-chip-row">
    {chip_1}
  </div>
  <div class="example-chip-row" style="margin-top:16px;">
    {chip_2}
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div style="
            font-size:12px;
            color:#9aa0a6;
            margin-top:36px;
            text-align:center;
        ">
            ✓ {len(docs)} dokumen &nbsp;·&nbsp; {len(inv):,} unique terms
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_footer()


# ═══════════════════════════════════════════════════════════
# RESULTS PAGE
# ═══════════════════════════════════════════════════════════

else:
    st.markdown(
        """
<style>
.block-container {
    max-width: 720px !important;
    margin: 0 auto !important;
    padding: 0 24px 60px !important;
    min-height: unset !important;
    display: block !important;
}
</style>
""",
        unsafe_allow_html=True,
    )

    col_logo, col_search, col_btn = st.columns([1, 6, 1])

    with col_logo:
        st.markdown(
            f'<div style="padding-top:14px;">{logo_html("22px", "0", clickable=True)}</div>',
            unsafe_allow_html=True,
        )

    with col_search:
        results_query_input = st.text_input(
            "q",
            value=query,
            placeholder="Cari…",
            label_visibility="collapsed",
            key="results_query_input",
        )

    with col_btn:
        results_search_clicked = st.button("Cari", key="go_results")

    if results_search_clicked and results_query_input.strip():
        set_query_param(results_query_input.strip())
        st.rerun()

    st.markdown(
        '<hr style="border:none;border-top:1px solid #efefef;margin:4px 0 0;">',
        unsafe_allow_html=True,
    )

    results = do_search(query, docs, dtok, tfidf, inv, sw, stem, TOP_K)

    if results:
        save_search_summary_output(
            query=query,
            results=results,
            tfidf=tfidf,
            sw=sw,
            stem=stem,
            output_path=DATA_DIR / "search_summary_output.txt",
        )

    count_str = f"Sekitar {len(results)}" if results else "0"

    st.markdown(
        f'<div class="results-count">{count_str} hasil untuk '
        f'<strong>"{escape(query)}"</strong></div>',
        unsafe_allow_html=True,
    )

    if not results:
        st.markdown(
            """
<div class="no-results">Tidak ada hasil yang cocok dengan pencarian Anda.</div>
<div class="no-results-sub">
  Saran:<br>
  · Pastikan semua kata dieja dengan benar.<br>
  · Coba kata kunci yang berbeda.<br>
  · Coba kata kunci yang lebih umum.
</div>
""",
            unsafe_allow_html=True,
        )

    else:
        for result in results:
            rank = result["rank"]
            is_top = rank <= TOP_SUMMARIZE
            doc_id = escape(result["doc_id"])
            title = escape(result["title"] or "(Tanpa Judul)")
            url = escape(result["url"] or f"doc/{result['doc_id']}")

            if is_top:
                summary = summarize(
                    result["text"],
                    tfidf.get(result["doc_id"], {}),
                    sw,
                    stem,
                    TOP_SENTENCES,
                )

                rows = "".join(
                    f"""
<div class="sent-row">
  <span class="sent-num">[{sentence['index']}]</span>
  <span class="sent-body">{escape(sentence['sentence'])}
    <span class="sent-score">{sentence['score']:.3f}</span>
  </span>
</div>
"""
                    for sentence in summary
                )

                body = f'<span class="summary-label">Ringkasan extractive</span>{rows}'

            else:
                snippet = escape(result["text"][:220].strip())
                body = f'<div class="result-snippet">{snippet}…</div>'

            st.markdown(
                f"""
<div class="result-item">
  <div class="result-rank">#{rank} &nbsp;·&nbsp; ID: {doc_id}</div>
  <div class="result-url">{url[:70]}</div>
  <div class="result-title">{title}</div>
  <span class="result-score">cosine similarity: {result['score']:.6f}</span>
  {body}
</div>
<hr class="result-divider">
""",
                unsafe_allow_html=True,
            )

    output_file = DATA_DIR / "search_summary_output.txt"

    if output_file.exists():
        with open(output_file, "r", encoding="utf-8") as file:
            st.download_button(
                label="Download hasil pencarian (.txt)",
                data=file.read(),
                file_name="search_summary_output.txt",
                mime="text/plain",
            )

    render_footer()