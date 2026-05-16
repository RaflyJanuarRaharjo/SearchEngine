"""
Tugas 4 – Pemerolehan Informasi dan Penambangan Teks
Search Engine + Peringkasan Teks Extractive (TF-IDF From Scratch)

Jalankan dengan:
    streamlit run app.py
"""

import re
import math
import os
import streamlit as st
from collections import defaultdict, Counter

st.set_page_config(
    page_title="INFO Search",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed",
)

EXAMPLES = [
    "gula darah diabetes insulin",
    "vaksin campak imunisasi anak",
    "kanker kemoterapi tumor",
    "kolesterol jantung lemak",
]

# ─── CSS global ───────────────────────────────────────────
st.markdown("""
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

/* ── Search input ── */
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

/* ── Tombol standar ── */
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

/* ── Chip contoh query ───────────────────────── */
.example-chip-row {
    width: 100%;
    max-width: 860px;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 24px;
    flex-wrap: wrap;
    margin: 10px auto 0;
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

/* Tombol "Muat Indeks" biru */
.load-btn .stButton > button {
    background: #1a73e8 !important;
    color: #fff !important;
    border-color: #1a73e8 !important;
    padding: 10px 28px !important;
    font-size: 15px !important;
}

.load-btn .stButton > button:hover {
    background: #1557b0 !important;
    border-color: #1557b0 !important;
}

/* ── Logo ── */
.logo {
    font-weight: 700;
    letter-spacing: -1px;
    line-height: 1;
    font-family: arial, sans-serif;
    text-align: center;
}

/* ── Footer ── */
.page-footer {
    font-size: 12px;
    color: #70757a;
    text-align: center;
    margin-top: 48px;
    padding-top: 12px;
    border-top: 1px solid #efefef;
    width: 100%;
}

/* ── Results ── */
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
    grid-template-columns: 28px 1fr;
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
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# ENGINE
# ═══════════════════════════════════════════════════════════

def preprocess(text, sw, stem):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = sw.remove(text)
    text = stem.stem(text)
    return [t for t in text.split() if len(t) >= 3]


def split_sentences(text):
    raw = re.split(r'(?<=[.!?])\s+', text.strip())
    return [(i, s.strip()) for i, s in enumerate(raw) if len(s.strip()) > 20]


def parse_corpus(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    docs = []

    for block in re.findall(r'<DOC>(.*?)</DOC>', content, re.DOTALL | re.IGNORECASE):
        def g(tag):
            m = re.search(rf'<{tag}>(.*?)</{tag}>', block, re.DOTALL | re.IGNORECASE)
            return m.group(1).strip() if m else ''

        if g('ID') and g('TEXT'):
            docs.append({
                'id': g('ID'),
                'nim': g('NIM'),
                'title': g('TITLE'),
                'url': g('URL'),
                'text': g('TEXT')
            })

    return docs


def build_engine(docs, sw, stem, progress_cb=None):
    inv = defaultdict(dict)
    dtok = {}
    N = len(docs)

    for i, d in enumerate(docs):
        if progress_cb:
            progress_cb(i / (N * 2), f"Tokenisasi dokumen {i+1}/{N}…")

        tok = preprocess(d['title'] + ' ' + d['text'], sw, stem)
        dtok[d['id']] = tok

        for t, f in Counter(tok).items():
            inv[t][d['id']] = f

    inv = dict(inv)
    tfidf = {}

    for i, d in enumerate(docs):
        if progress_cb:
            progress_cb(0.5 + i / (N * 2), f"Menghitung TF-IDF dokumen {i+1}/{N}…")

        did = d['id']
        tok = dtok[did]
        tfidf[did] = {}

        for t in set(tok):
            c = tok.count(t)
            tf = (1 + math.log10(c)) if c > 0 else 0.0
            df = len(inv.get(t, {}))
            idf = math.log10(N / df) if df > 0 else 0.0
            tfidf[did][t] = tf * idf

    return inv, dtok, tfidf


def do_search(query, docs, dtok, tfidf, inv, sw, stem, top_k=10):
    N = len(docs)
    qtok = preprocess(query, sw, stem)

    if not qtok:
        return []

    qv = {}

    for t in set(qtok):
        c = qtok.count(t)
        tf = (1 + math.log10(c)) if c > 0 else 0.0
        df = len(inv.get(t, {}))
        idf = math.log10(N / df) if df > 0 else 0.0
        qv[t] = tf * idf

    cands = set()

    for t in qtok:
        cands.update(inv.get(t, {}).keys())

    scores = []

    for did in cands:
        dv = tfidf.get(did, {})
        common = set(qv) & set(dv)
        dot = sum(qv[t] * dv[t] for t in common)

        if dot == 0:
            continue

        ma = math.sqrt(sum(v ** 2 for v in qv.values()))
        mb = math.sqrt(sum(v ** 2 for v in dv.values()))

        if ma == 0 or mb == 0:
            continue

        scores.append((did, dot / (ma * mb)))

    scores.sort(key=lambda x: x[1], reverse=True)
    dm = {d['id']: d for d in docs}

    return [{
        'rank': i + 1,
        'doc_id': did,
        'score': s,
        'title': dm[did].get('title', ''),
        'text': dm[did].get('text', ''),
        'url': dm[did].get('url', '')
    } for i, (did, s) in enumerate(scores[:top_k])]


def summarize(text, tfidf_vec, sw, stem, top_n=3):
    sents = split_sentences(text)

    if not sents:
        return []

    scored = []

    for idx, s in sents:
        tok = preprocess(s, sw, stem)

        if not tok:
            continue

        sc = sum(tfidf_vec.get(t, 0) for t in tok) / len(tok)

        scored.append({
            'index': idx,
            'sentence': s,
            'score': sc
        })

    top = sorted(scored, key=lambda x: x['score'], reverse=True)[:top_n]
    top.sort(key=lambda x: x['index'])

    return top


# ═══════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════

CORPUS_FILE = "corpus.txt"
TOP_K = 10
TOP_SUMMARIZE = 3
TOP_SENTENCES = 3

for k, v in [
    ("engine_ready", False),
    ("docs", []),
    ("inv", {}),
    ("dtok", {}),
    ("tfidf", {}),
    ("sw", None),
    ("stem", None),
    ("q", ""),
]:
    if k not in st.session_state:
        st.session_state[k] = v


# ═══════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════

LOGO_COLORS = [
    ('#4285F4', 'I'),
    ('#EA4335', 'N'),
    ('#FBBC05', 'F'),
    ('#4285F4', 'O'),
]


def logo_html(size="72px", mb="32px"):
    spans = "".join(
        f'<span style="color:{c}">{ch}</span>'
        for c, ch in LOGO_COLORS
    )

    return (
        f'<div class="logo" style="font-size:{size};margin-bottom:{mb};">'
        f'{spans}</div>'
    )


def inject_center_css():
    st.markdown("""
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
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# CORPUS CHECK
# ═══════════════════════════════════════════════════════════

if not os.path.exists(CORPUS_FILE):
    inject_center_css()
    st.markdown(logo_html(), unsafe_allow_html=True)
    st.error(
        f"File `{CORPUS_FILE}` tidak ditemukan. "
        "Taruh corpus.txt satu folder dengan app.py lalu refresh."
    )
    st.stop()


# ═══════════════════════════════════════════════════════════
# LOAD ENGINE
# ═══════════════════════════════════════════════════════════

if not st.session_state.engine_ready:
    inject_center_css()
    st.markdown(logo_html("72px", "32px"), unsafe_allow_html=True)

    st.markdown("""
<div style="background:#f8f9fa;border-radius:8px;padding:28px 32px;
            text-align:center;max-width:440px;width:100%;margin:0 auto 24px;">
  <div style="font-size:18px;color:#202124;margin-bottom:8px;">Indeks belum dimuat</div>
  <div style="font-size:14px;color:#70757a;">
    Klik tombol di bawah untuk membangun indeks TF-IDF dari corpus.
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="load-btn">', unsafe_allow_html=True)

    if st.button("Muat Indeks", key="load_btn"):
        prog_bar = st.progress(0, text="Memulai…")
        prog_text = st.empty()

        def progress_cb(val, msg):
            prog_bar.progress(min(val, 0.99), text=msg)
            prog_text.caption(msg)

        prog_text.caption("Memuat Sastrawi…")

        from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
        from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

        sw = StopWordRemoverFactory().create_stop_word_remover()
        stem = StemmerFactory().create_stemmer()

        progress_cb(0.05, "Parsing corpus…")

        docs = parse_corpus(CORPUS_FILE)
        inv, dtok, tfidf = build_engine(docs, sw, stem, progress_cb=progress_cb)

        st.session_state.sw = sw
        st.session_state.stem = stem
        st.session_state.docs = docs
        st.session_state.inv = inv
        st.session_state.dtok = dtok
        st.session_state.tfidf = tfidf
        st.session_state.engine_ready = True

        prog_bar.progress(1.0, text="Selesai!")
        prog_text.empty()

        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()


# ═══════════════════════════════════════════════════════════
# ENGINE READY
# ═══════════════════════════════════════════════════════════

docs = st.session_state.docs
inv = st.session_state.inv
dtok = st.session_state.dtok
tfidf = st.session_state.tfidf
sw = st.session_state.sw
stem = st.session_state.stem

params = st.query_params
if "qchip" in params:
    try:
        idx = int(params["qchip"])
        if 0 <= idx < len(EXAMPLES):
            st.session_state.q = EXAMPLES[idx]
    except:
        pass

    st.query_params.clear()
    st.rerun()

query = st.session_state.get("q", "")
mode = "results" if query.strip() else "home"


# ───────────────────────── HOME ─────────────────────────

if mode == "home":
    inject_center_css()

    st.markdown(logo_html("72px", "48px"), unsafe_allow_html=True)

    # Search bar center
    outer_cols = st.columns([1.4, 5.8, 1.4])

    with outer_cols[1]:
        inner_cols = st.columns([6, 1.2], gap="small")

        with inner_cols[0]:
            query_input = st.text_input(
                "q",
                placeholder="Cari apa saja…",
                label_visibility="collapsed",
                key="q"
            )

        with inner_cols[1]:
            cari_clicked = st.button("Cari", key="go_home")

    if cari_clicked and query_input.strip():
        st.rerun()

    st.markdown("""
<div style="
    font-size:12px;
    color:#70757a;
    margin:36px 0 14px;
    text-align:center;
">
  Coba kueri ini:
</div>
""", unsafe_allow_html=True)

    chip_html = '<div class="example-chip-row">'

    for i, ex in enumerate(EXAMPLES):
        chip_html += f'<a class="example-chip" href="?qchip={i}">{ex}</a>'

    chip_html += '</div>'

    st.markdown(chip_html, unsafe_allow_html=True)

    st.markdown(
        f'''
        <div style="
            font-size:12px;
            color:#9aa0a6;
            margin-top:40px;
            text-align:center;
        ">
            ✓ {len(docs)} dokumen &nbsp;·&nbsp; {len(inv):,} unique terms
        </div>
        ''',
        unsafe_allow_html=True
    )

    st.markdown("""
<div class="page-footer">
  PIPT · Tugas 4 · 2026 &nbsp;·&nbsp;
  Nicolas Gabriel Siahaan &nbsp;·&nbsp;
  Dzaky Rezandi &nbsp;·&nbsp;
  Rafly Januar Raharjo &nbsp;·&nbsp;
  M. Naufal Al Farizki
</div>
""", unsafe_allow_html=True)


# ───────────────────────── RESULTS ─────────────────────────

else:
    st.markdown("""
<style>
.block-container {
    max-width: 720px !important;
    margin: 0 auto !important;
    padding: 0 24px 60px !important;
    min-height: unset !important;
    display: block !important;
}
</style>
""", unsafe_allow_html=True)

    col_logo, col_search, col_btn = st.columns([1, 6, 1])

    with col_logo:
        st.markdown(
            f'<div style="padding-top:14px;">{logo_html("22px", "0")}</div>',
            unsafe_allow_html=True
        )

    with col_search:
        query_input = st.text_input(
            "q",
            value=query,
            placeholder="Cari…",
            label_visibility="collapsed",
            key="q"
        )

    with col_btn:
        if st.button("Cari", key="go_results"):
            st.rerun()

    if query_input != query:
        st.rerun()

    st.markdown(
        '<hr style="border:none;border-top:1px solid #efefef;margin:4px 0 0;">',
        unsafe_allow_html=True
    )

    results = do_search(query, docs, dtok, tfidf, inv, sw, stem, TOP_K)

    count_str = f"Sekitar {len(results)}" if results else "0"

    st.markdown(
        f'<div class="results-count">{count_str} hasil untuk '
        f'<strong>"{query}"</strong></div>',
        unsafe_allow_html=True
    )

    if not results:
        st.markdown("""
<div class="no-results">Tidak ada hasil yang cocok dengan pencarian Anda.</div>
<div class="no-results-sub">
  Saran:<br>
  · Pastikan semua kata dieja dengan benar.<br>
  · Coba kata kunci yang berbeda.<br>
  · Coba kata kunci yang lebih umum.
</div>
""", unsafe_allow_html=True)

    else:
        for r in results:
            rank = r['rank']
            is_top = rank <= TOP_SUMMARIZE
            title = r['title'] or '(Tanpa Judul)'
            url = r['url'] or f"doc/{r['doc_id']}"

            if is_top:
                summ = summarize(
                    r['text'],
                    tfidf.get(r['doc_id'], {}),
                    sw,
                    stem,
                    TOP_SENTENCES
                )

                rows = "".join(f"""
<div class="sent-row">
  <span class="sent-num">[{s['index']+1}]</span>
  <span class="sent-body">{s['sentence']}
    <span class="sent-score">{s['score']:.3f}</span>
  </span>
</div>
""" for s in summ)

                body = f'<span class="summary-label">Ringkasan extractive</span>{rows}'

            else:
                snippet = (
                    r['text'][:220]
                    .strip()
                    .replace('<', '&lt;')
                    .replace('>', '&gt;')
                )

                body = f'<div class="result-snippet">{snippet}…</div>'

            st.markdown(f"""
<div class="result-item">
  <div class="result-rank">#{rank} &nbsp;·&nbsp; ID: {r['doc_id']}</div>
  <div class="result-url">{url[:70]}</div>
  <div class="result-title">{title}</div>
  <span class="result-score">cosine similarity: {r['score']:.6f}</span>
  {body}
</div>
<hr class="result-divider">
""", unsafe_allow_html=True)

    st.markdown("""
<div class="page-footer">
  PIPT · Tugas 4 · 2026 &nbsp;·&nbsp;
  Nicolas Gabriel Siahaan &nbsp;·&nbsp;
  Dzaky Rezandi &nbsp;·&nbsp;
  Rafly Januar Raharjo &nbsp;·&nbsp;
  M. Naufal Al Farizki
</div>
""", unsafe_allow_html=True)