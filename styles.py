"""
styles.py  —  All CSS for StoryVibe in one place.
Import APP_CSS and inject: st.markdown(APP_CSS, unsafe_allow_html=True)
"""

APP_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;900&display=swap');

/* ── Reset & global ─────────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    background: linear-gradient(135deg, #0a0010 0%, #0d0020 50%, #000d1a 100%) !important;
    font-family: 'Poppins', sans-serif !important;
    color: #ffffff !important;
}

/* Force centered narrow column */
[data-testid="stMainBlockContainer"] {
    max-width: 660px !important;
    margin: 0 auto !important;
    padding: 0 20px 60px !important;
}

/* Remove Streamlit chrome */
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
#MainMenu, footer { display: none !important; }

/* ── App title ──────────────────────────────────────────────────────────── */
.sv-title {
    font-size: 3rem;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #ff006e, #fb5607, #ffbe0b, #8338ec, #3a86ff);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: rainbow 5s ease infinite;
    letter-spacing: 2px;
    margin: 32px 0 8px;
    line-height: 1.2;
}
.sv-subtitle {
    text-align: center;
    font-size: 0.95rem;
    color: rgba(255,255,255,0.45);
    margin-bottom: 32px;
}
@keyframes rainbow {
    0%   { background-position: 0%   50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0%   50%; }
}

/* ── API key input ──────────────────────────────────────────────────────── */
[data-testid="stTextInput"] label {
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    color: rgba(255,255,255,0.55) !important;
    letter-spacing: 0.5px !important;
}
[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.06) !important;
    border: 1.5px solid rgba(255,190,11,0.35) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
    font-family: 'Poppins', monospace !important;
    font-size: 0.88rem !important;
    padding: 10px 14px !important;
    transition: border-color .25s, box-shadow .25s !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #ffbe0b !important;
    box-shadow: 0 0 0 3px rgba(255,190,11,0.15) !important;
    outline: none !important;
}

/* ── File uploader ──────────────────────────────────────────────────────── */
[data-testid="stFileUploader"] {
    width: 100% !important;
}
[data-testid="stFileUploader"] section {
    background: rgba(255,255,255,0.04) !important;
    border: 2px dashed rgba(255,190,11,0.6) !important;
    border-radius: 20px !important;
    padding: 40px 28px !important;
    text-align: center !important;
    transition: border-color .3s, box-shadow .3s !important;
    box-shadow: 0 0 24px rgba(255,190,11,0.08) !important;
}
[data-testid="stFileUploader"] section:hover {
    border-color: #ff006e !important;
    box-shadow: 0 0 40px rgba(255,0,110,0.18) !important;
}
[data-testid="stFileUploader"] section > div > div > span {
    color: #ffbe0b !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
}
[data-testid="stFileUploader"] section button {
    background: linear-gradient(135deg, #ff006e, #fb5607) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 8px 22px !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
    margin-top: 12px !important;
    transition: transform .2s !important;
}
[data-testid="stFileUploader"] section button:hover { transform: scale(1.05) !important; }
[data-testid="stFileUploaderFileName"] { color: rgba(255,255,255,0.75) !important; }

/* ── Upload hint ────────────────────────────────────────────────────────── */
.upload-hint {
    text-align: center;
    color: rgba(255,255,255,0.22);
    font-size: 0.8rem;
    margin: 20px 0 0;
}

/* ── Preview label ──────────────────────────────────────────────────────── */
.preview-label {
    text-align: center;
    font-size: 0.75rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.35);
    margin: 20px 0 8px;
}

/* ── st.image centering & styling ───────────────────────────────────────── */
[data-testid="stImage"] { display: block; text-align: center; }
[data-testid="stImage"] img {
    border-radius: 18px !important;
    border: 2px solid rgba(255,190,11,0.45) !important;
    box-shadow: 0 0 40px rgba(255,190,11,0.18) !important;
    max-width: 100% !important;
    display: block !important;
    margin: 0 auto !important;
}

/* ── Action button ──────────────────────────────────────────────────────── */
div.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #ff006e, #fb5607, #ffbe0b) !important;
    background-size: 300% 300% !important;
    animation: rainbow 5s ease infinite !important;
    color: #fff !important;
    font-size: 1rem !important;
    font-weight: 900 !important;
    letter-spacing: 1.5px !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 15px 28px !important;
    box-shadow: 0 8px 28px rgba(255,0,110,0.35) !important;
    transition: transform .2s, box-shadow .2s !important;
    text-transform: uppercase !important;
    cursor: pointer !important;
}
div.stButton > button:hover {
    transform: scale(1.03) !important;
    box-shadow: 0 12px 44px rgba(255,0,110,0.55) !important;
}

/* ── Divider ────────────────────────────────────────────────────────────── */
.sv-divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.07);
    margin: 24px 0;
}

/* ── Emotion badges ─────────────────────────────────────────────────────── */
.emotion-row { text-align: center; margin: 4px 0 16px; }
.emotion-badge {
    display: inline-block;
    background: rgba(255,255,255,0.07);
    border: 1.5px solid rgba(255,190,11,0.4);
    color: #ffbe0b;
    padding: 6px 18px;
    border-radius: 50px;
    margin: 4px;
    font-size: 0.85rem;
    font-weight: 700;
}

/* ── Confidence bars ────────────────────────────────────────────────────── */
.confidence-wrap {
    background: rgba(255,255,255,0.04);
    border-radius: 14px;
    padding: 16px 20px;
    margin: 0 0 22px;
}
.bar-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 6px 0;
}
.bar-label {
    font-size: 0.78rem;
    color: rgba(255,255,255,0.55);
    min-width: 80px;
}
.bar-bg {
    flex: 1;
    background: rgba(255,255,255,0.08);
    border-radius: 6px;
    height: 6px;
    overflow: hidden;
}
.bar-fill {
    height: 100%;
    border-radius: 6px;
    background: linear-gradient(90deg, #8338ec, #3a86ff);
    transition: width .6s ease;
}
.bar-pct {
    font-size: 0.75rem;
    color: rgba(255,255,255,0.4);
    min-width: 32px;
    text-align: right;
}

/* ── Analysis card ──────────────────────────────────────────────────────── */
.analysis-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,190,11,0.2);
    border-radius: 18px;
    padding: 18px 22px;
    margin: 0 0 20px;
}
.ac-row {
    display: flex;
    align-items: baseline;
    gap: 10px;
    margin-bottom: 10px;
}
.ac-label {
    font-size: 0.72rem;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.35);
    white-space: nowrap;
    min-width: 64px;
}
.ac-value {
    font-size: 0.95rem;
    font-weight: 600;
    color: #ffffff;
}
.ac-summary {
    font-size: 0.82rem;
    color: rgba(255,255,255,0.45);
    border-top: 1px solid rgba(255,255,255,0.07);
    padding-top: 12px;
    margin-top: 4px;
    line-height: 1.6;
}

/* ── Vibe tags ──────────────────────────────────────────────────────────── */
.vibe-row { text-align: center; margin: 0 0 28px; }
.vibe-tag {
    display: inline-block;
    background: linear-gradient(135deg, rgba(131,56,236,0.3), rgba(58,134,255,0.3));
    border: 1px solid rgba(131,56,236,0.45);
    color: #c4aaff;
    padding: 5px 16px;
    border-radius: 50px;
    margin: 4px;
    font-size: 0.78rem;
    font-weight: 600;
}

/* ── Section title ──────────────────────────────────────────────────────── */
.sv-section-title {
    font-size: 1.35rem;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg, #ffbe0b, #ff006e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 28px 0 16px;
}

/* ── Song card ──────────────────────────────────────────────────────────── */
.song-card {
    display: flex;
    align-items: center;
    gap: 14px;
    background: rgba(255,255,255,0.05);
    border-radius: 16px;
    border-left: 4px solid #ffbe0b;
    padding: 14px 18px;
    margin: 10px 0;
    transition: transform .25s, box-shadow .25s, border-color .25s, background .25s;
    text-decoration: none;
}
.song-card:hover {
    transform: translateX(5px);
    border-left-color: #ff006e;
    background: rgba(255,255,255,0.09);
    box-shadow: 0 6px 28px rgba(255,0,110,0.2);
}
.song-num {
    font-size: 1.1rem;
    font-weight: 900;
    color: rgba(255,190,11,0.3);
    min-width: 34px;
    text-align: center;
}
.song-info { flex: 1; min-width: 0; }
.song-title {
    font-size: 0.96rem;
    font-weight: 700;
    color: #ffffff;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-bottom: 2px;
}
.song-artist {
    font-size: 0.76rem;
    color: rgba(255,255,255,0.42);
    margin-bottom: 4px;
}
.song-genre {
    display: inline-block;
    background: rgba(255,190,11,0.1);
    color: #ffbe0b;
    font-size: 0.67rem;
    font-weight: 600;
    padding: 2px 10px;
    border-radius: 50px;
    margin-bottom: 4px;
}
.song-why {
    font-size: 0.75rem;
    color: rgba(255,255,255,0.32);
    line-height: 1.4;
    font-style: italic;
}
.yt-btn {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #ff0000;
    color: #fff !important;
    text-decoration: none !important;
    padding: 8px 14px;
    border-radius: 50px;
    font-size: 0.75rem;
    font-weight: 700;
    white-space: nowrap;
    flex-shrink: 0;
    transition: transform .2s, box-shadow .2s;
    box-shadow: 0 3px 12px rgba(255,0,0,0.28);
}
.yt-btn:hover {
    transform: scale(1.08);
    box-shadow: 0 6px 22px rgba(255,0,0,0.48);
}

/* ── Footer ─────────────────────────────────────────────────────────────── */
.sv-footer {
    text-align: center;
    color: rgba(255,255,255,0.18);
    font-size: 0.72rem;
    margin: 56px 0 24px;
    line-height: 1.7;
}
</style>
"""
