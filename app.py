"""
app.py  —  StoryVibe
====================
Run:  streamlit run app.py

File structure:
  storyvibe/
  ├── app.py            ← you are here
  ├── model.py          ← CNN architecture + inference helpers
  ├── recommender.py    ← Claude Vision API + YouTube Music URLs
  ├── styles.py         ← all CSS
  └── model.h5          ← pre-trained FER weights (place here)
"""

import numpy as np
import streamlit as st
import cv2

from styles import APP_CSS
from model import load_model, predict_emotions
from recommender import get_recommendations, youtube_music_url

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="StoryVibe",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(APP_CSS, unsafe_allow_html=True)


# ── Load model once ───────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading emotion model…")
def get_model():
    return load_model("./model.h5")


# ── Session state defaults ────────────────────────────────────────────────────
_DEFAULTS = {
    "page":        "upload",
    "image_bytes": None,
    "image_cv2":   None,
    "emotions":    [],
    "moods":       [],
    "confidences": {},
    "result":      None,
    "api_key":     "",
}
for k, v in _DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


def reset():
    for k, v in _DEFAULTS.items():
        st.session_state[k] = v


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  PAGE 1 — UPLOAD                                                         ║
# ╚══════════════════════════════════════════════════════════════════════════╝
def page_upload():
    # ── Header ───────────────────────────────────────────────────────────────
    st.markdown('<div class="sv-title">🎵 StoryVibe</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sv-subtitle">Upload any photo — we detect your vibe and find the perfect songs</div>',
        unsafe_allow_html=True,
    )

    # ── API key input ─────────────────────────────────────────────────────────
    st.markdown('<div class="api-key-wrap">', unsafe_allow_html=True)
    api_key = st.text_input(
        "🔑 Anthropic API Key",
        value=st.session_state.api_key,
        type="password",
        placeholder="sk-ant-...",
        help="Get your key at console.anthropic.com",
        key="api_key_input",
    )
    st.session_state.api_key = api_key
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── File uploader ─────────────────────────────────────────────────────────
    uploaded = st.file_uploader(
        "📸  Drop your photo here — selfie, landscape, party, nature, anything",
        type=["jpg", "jpeg", "png", "webp"],
        key="uploader",
        label_visibility="visible",
    )

    if uploaded is None:
        st.markdown(
            '<div class="upload-hint">Works with selfies · landscapes · parties · travel shots</div>',
            unsafe_allow_html=True,
        )
        return

    # ── Decode image ──────────────────────────────────────────────────────────
    raw = uploaded.read()
    arr = np.frombuffer(raw, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    if img is None:
        st.error("Could not decode the image. Please try a different file.")
        return

    st.session_state.image_bytes = raw
    st.session_state.image_cv2   = img

    # ── Preview ───────────────────────────────────────────────────────────────
    st.markdown('<div class="preview-label">Preview</div>', unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        st.image(img, channels="BGR", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Action button ─────────────────────────────────────────────────────────
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        clicked = st.button("🚀  GET MY BEST FIT SONGS", key="go_btn")

    if clicked:
        if not st.session_state.api_key.strip():
            st.error("Please enter your Anthropic API Key above.")
            return

        model = get_model()

        with st.spinner("🔍 Analysing your photo…"):
            emotions, moods, confidences = predict_emotions(model, img)

        st.session_state.emotions    = emotions
        st.session_state.moods       = moods
        st.session_state.confidences = confidences

        with st.spinner("🎵 Finding the perfect songs for your vibe…"):
            try:
                result = get_recommendations(
                    raw, emotions, moods,
                    api_key=st.session_state.api_key.strip()
                )
                st.session_state.result = result
                st.session_state.page   = "results"
                st.rerun()
            except Exception as exc:
                st.error(f"Recommendation failed: {exc}")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  PAGE 2 — RESULTS                                                         ║
# ╚══════════════════════════════════════════════════════════════════════════╝
def page_results():
    result      = st.session_state.result or {}
    songs       = result.get("songs", [])
    emotions    = st.session_state.emotions
    confidences = st.session_state.confidences

    # ── Back button ───────────────────────────────────────────────────────────
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_l:
        if st.button("← Back", key="back_btn"):
            reset()
            st.rerun()

    # ── Title ─────────────────────────────────────────────────────────────────
    st.markdown('<div class="sv-title" style="font-size:2.4rem;margin-top:10px;">Your Vibe 🎧</div>', unsafe_allow_html=True)

    # ── Uploaded photo ────────────────────────────────────────────────────────
    if st.session_state.image_cv2 is not None:
        col_l, col_c, col_r = st.columns([1, 2, 1])
        with col_c:
            st.image(st.session_state.image_cv2, channels="BGR", use_container_width=True)

    st.markdown('<hr class="sv-divider">', unsafe_allow_html=True)

    # ── Detected emotion badges ───────────────────────────────────────────────
    emoji_map = {
        "Angry": "😠", "Disgusted": "🤢", "Fearful": "😨",
        "Happy": "😊", "Neutral":   "😐", "Sad":     "😢", "Surprised": "😲",
    }
    if emotions:
        badges = " ".join(
            f'<span class="emotion-badge">{emoji_map.get(e,"😐")} {e}</span>'
            for e in emotions
        )
        st.markdown(f'<div class="emotion-row">{badges}</div>', unsafe_allow_html=True)

    # ── Confidence bars ───────────────────────────────────────────────────────
    if confidences:
        top3  = sorted(confidences.items(), key=lambda x: x[1], reverse=True)[:3]
        bars  = ""
        for label, score in top3:
            pct = int(score * 100)
            bars += (
                f'<div class="bar-row">'
                f'  <span class="bar-label">{label}</span>'
                f'  <div class="bar-bg"><div class="bar-fill" style="width:{max(pct,2)}%"></div></div>'
                f'  <span class="bar-pct">{pct}%</span>'
                f'</div>'
            )
        st.markdown(f'<div class="confidence-wrap">{bars}</div>', unsafe_allow_html=True)

    # ── Scene + mood analysis card ────────────────────────────────────────────
    scene    = result.get("scene", "")
    mood_lbl = result.get("mood_label", "")
    summary  = result.get("summary", "")
    tags     = result.get("vibe_tags", [])

    if scene or mood_lbl:
        st.markdown(f"""
        <div class="analysis-card">
            <div class="ac-row"><span class="ac-label">📍 Scene</span><span class="ac-value">{scene}</span></div>
            <div class="ac-row"><span class="ac-label">💫 Mood</span><span class="ac-value">{mood_lbl}</span></div>
            <div class="ac-summary">{summary}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Vibe tags ─────────────────────────────────────────────────────────────
    if tags:
        tag_html = " ".join(f'<span class="vibe-tag">{t}</span>' for t in tags)
        st.markdown(f'<div class="vibe-row">{tag_html}</div>', unsafe_allow_html=True)

    # ── Song list ─────────────────────────────────────────────────────────────
    st.markdown(
        '<div class="sv-section-title">🎵 Songs Made for This Moment</div>',
        unsafe_allow_html=True,
    )

    if not songs:
        st.warning("No songs returned. Please try again.")
        return

    for i, song in enumerate(songs, 1):
        title  = song.get("title",  "Unknown Title")
        artist = song.get("artist", "Unknown Artist")
        genre  = song.get("genre",  "")
        why    = song.get("why",    "")
        yt_url = youtube_music_url(title, artist)

        genre_html = f'<span class="song-genre">{genre}</span>' if genre else ""

        st.markdown(f"""
        <div class="song-card">
            <div class="song-num">#{i:02d}</div>
            <div class="song-info">
                <div class="song-title">{title}</div>
                <div class="song-artist">🎤 {artist}</div>
                {genre_html}
                <div class="song-why">{why}</div>
            </div>
            <a href="{yt_url}" target="_blank" class="yt-btn">▶ YouTube Music</a>
        </div>
        """, unsafe_allow_html=True)

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="sv-footer">
        🎶 StoryVibe &nbsp;·&nbsp; Your Vibe, Your Sound<br>
        Emotion by CNN &nbsp;·&nbsp; Scene analysis by Claude Vision
    </div>
    """, unsafe_allow_html=True)


# ── Router ────────────────────────────────────────────────────────────────────
if st.session_state.page == "upload":
    page_upload()
elif st.session_state.page == "results":
    page_results()
