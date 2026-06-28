"""
recommender.py
--------------
Sends photo + detected emotion/mood to Claude Vision API.
Claude analyses the full scene combined with emotion → 10 song recommendations.
Each song gets a YouTube Music search URL (no API key needed for YT).
"""

import base64
import json
import urllib.parse
import requests

CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"
CLAUDE_MODEL   = "claude-sonnet-4-6"

SYSTEM_PROMPT = """You are StoryVibe, an expert AI music curator.

You receive:
- A photo → detect the SCENE (beach, mountain, city, forest, gym, party, café, rainy window, etc.)
- Detected face EMOTION from a CNN model (Happy, Sad, Neutral, Angry, etc.)

Recommend 10 songs that feel PERFECT for BOTH the scene AND the emotion together.
Think like a DJ setting the mood for a specific place + feeling combo:
- Happy + Beach    → upbeat tropical, summer anthems
- Sad + Rain       → lo-fi, melancholic indie
- Neutral + Gym    → motivational hip-hop, EDM
- Angry + City     → hard rap, intense rock
- Happy + Mountain → folk, acoustic, adventure anthems

Rules:
- Recommend globally — mix Hindi, English, Spanish, Korean etc.
- NO repeated artists
- Each song must genuinely fit BOTH scene and emotion
- Return ONLY valid JSON — no markdown, no extra text

Required JSON format:
{
  "scene": "2-4 word scene label",
  "mood_label": "2-4 word mood label",
  "vibe_tags": ["tag1", "tag2", "tag3", "tag4"],
  "summary": "One sentence why these songs fit this photo perfectly.",
  "songs": [
    {
      "title": "Song Title",
      "artist": "Artist Name",
      "genre": "Genre",
      "why": "One short sentence why it fits this exact photo."
    }
  ]
}"""


def _encode_image(image_bytes: bytes) -> tuple:
    """Return (base64_data, mime_type)."""
    sig = image_bytes[:4]
    if sig[:3] == b'\xff\xd8\xff':
        mime = "image/jpeg"
    elif sig == b'\x89PNG':
        mime = "image/png"
    elif image_bytes[8:12] == b'WEBP':
        mime = "image/webp"
    else:
        mime = "image/jpeg"
    return base64.standard_b64encode(image_bytes).decode(), mime


def get_recommendations(image_bytes: bytes,
                        detected_emotions: list,
                        moods: list,
                        api_key: str = "") -> dict:
    """
    Call Claude Vision with the photo + emotion context.

    Parameters
    ----------
    image_bytes        : raw bytes of the uploaded image
    detected_emotions  : raw labels from CNN  e.g. ["Happy", "Surprised"]
    moods              : mood buckets          e.g. ["Happy"]
    api_key            : Anthropic API key (passed from UI input)
    """
    if not api_key:
        raise ValueError(
            "Anthropic API Key is missing.\n"
            "Enter your key (sk-ant-...) in the field on the upload page."
        )

    b64, mime = _encode_image(image_bytes)
    emotion_context = (
        f"CNN detected emotion(s): {', '.join(detected_emotions)}. "
        f"Mood bucket(s): {', '.join(moods)}."
    )

    payload = {
        "model": CLAUDE_MODEL,
        "max_tokens": 1800,
        "system": SYSTEM_PROMPT,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": mime,
                            "data": b64,
                        },
                    },
                    {
                        "type": "text",
                        "text": (
                            f"{emotion_context}\n\n"
                            "Carefully look at this photo. Identify the scene and setting. "
                            "Then recommend 10 songs that perfectly match both the scene and the emotion. "
                            "Return ONLY the JSON object."
                        ),
                    },
                ],
            }
        ],
    }

    headers = {
        "Content-Type":      "application/json",
        "x-api-key":         api_key,
        "anthropic-version": "2023-06-01",
    }

    resp = requests.post(CLAUDE_API_URL, json=payload, headers=headers, timeout=45)
    resp.raise_for_status()

    raw = ""
    for block in resp.json().get("content", []):
        if block.get("type") == "text":
            raw += block["text"]

    # Strip accidental markdown fences
    clean = raw.strip()
    if clean.startswith("```"):
        clean = clean.split("\n", 1)[-1]
        clean = clean.rsplit("```", 1)[0].strip()

    return json.loads(clean)


def youtube_music_url(title: str, artist: str) -> str:
    """Return a YouTube Music search URL for a song."""
    query = urllib.parse.quote_plus(f"{title} {artist}")
    return f"https://music.youtube.com/search?q={query}"
