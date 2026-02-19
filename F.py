import streamlit as st
from googleapiclient.discovery import build
import google.generativeai as genai
import os
import re

# API Keys
YOUTUBE_API_KEY = "AIzaSyBBLJgQJmeTJtNM5rQar0afnapTGtY3kM4"
GEMINI_API_KEY = "AIzaSyCgzvuTNBBZaeZCnF2YCSQSjco_CtrnoT8"

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="YouTube Link Finder", page_icon="🎬", layout="centered")

# Custom CSS
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@400;500;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'DM Sans', sans-serif;
        }

        h1, h2, h3 {
            font-family: 'Bebas Neue', sans-serif;
            letter-spacing: 1px;
        }

        .stApp {
            background: #0a0a0a;
            color: #f0f0f0;
        }

        .stButton > button {
            background: linear-gradient(135deg, #CC0000, #FF4444);
            color: white;
            font-weight: 700;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
            font-family: 'DM Sans', sans-serif;
            font-size: 1rem;
            transition: all 0.2s ease;
            box-shadow: 0 4px 15px rgba(204,0,0,0.4);
        }

        .stButton > button:hover {
            background: linear-gradient(135deg, #FF0000, #FF6666);
            box-shadow: 0 6px 20px rgba(255,0,0,0.5);
            transform: translateY(-1px);
        }

        .stTextArea textarea, .stTextInput input {
            background: #1a1a1a !important;
            color: #f0f0f0 !important;
            border: 1px solid #333 !important;
            border-radius: 8px !important;
        }

        .stSelectbox > div > div {
            background: #1a1a1a !important;
            color: #f0f0f0 !important;
            border: 1px solid #333 !important;
        }

        .stSlider > div > div > div > div {
            background: #CC0000 !important;
        }

        .ai-box {
            background: linear-gradient(135deg, #1a0a0a, #1a1a2e);
            border: 1px solid #CC0000;
            border-left: 4px solid #FF4444;
            border-radius: 10px;
            padding: 1rem 1.2rem;
            margin: 1rem 0;
        }

        .ai-label {
            color: #FF4444;
            font-weight: 700;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 0.4rem;
        }

        .ai-text {
            color: #e0e0e0;
            font-size: 0.95rem;
            line-height: 1.6;
        }

        a { color: #FF4444 !important; }

        .stMarkdown h4 a {
            color: #FF6666 !important;
            text-decoration: none;
        }

        .section-header {
            font-family: 'Bebas Neue', sans-serif;
            font-size: 1.4rem;
            color: #FF4444;
            letter-spacing: 2px;
            margin-bottom: 0.2rem;
        }

        .divider {
            border: none;
            border-top: 1px solid #222;
            margin: 1.2rem 0;
        }

        .radio-container .stRadio > label {
            color: #f0f0f0 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 style="text-align:center; color:#FF4444; font-size:3rem; margin-bottom:0;">🎬 YouTube Link Finder</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#888; margin-top:0; margin-bottom:1.5rem;">Powered by Gemini AI + YouTube Data API</p>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# Description input
st.markdown('<div class="section-header">🔎 Describe the video you\'re looking for</div>', unsafe_allow_html=True)

description = st.text_area(
    "",
    placeholder="e.g. A tutorial on how to make sourdough bread, or a funny cat compilation...",
    height=120,
    label_visibility="collapsed"
)

# ── AI Enhancement Radio ──────────────────────────────────────────────────────
st.markdown('<div class="section-header" style="margin-top:1.2rem;">✨ AI Description Enhancement</div>', unsafe_allow_html=True)
st.markdown('<p style="color:#aaa; font-size:0.9rem; margin-top:-0.3rem;">Let Gemini 2.5 Flash rewrite your description to get better YouTube search results.</p>', unsafe_allow_html=True)

use_ai = st.radio(
    "Use AI to enhance your search description?",
    options=["Yes — enhance with Gemini AI 🤖", "No — use my description as-is"],
    index=0,
    horizontal=True
)
use_ai_flag = use_ai.startswith("Yes")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Optional filters ──────────────────────────────────────────────────────────
st.markdown('<div class="section-header">⚙️ Filters & Options</div>', unsafe_allow_html=True)

channel_name = st.text_input(
    "Optional: search within a specific channel",
    placeholder='e.g. "MrBeast" (leave empty for any channel)'
)

video_style = st.selectbox(
    "Optional: choose a video type/style",
    ["Any", "Shorts", "Explainer", "Normal video", "Tutorial", "Podcast / Interview", "Review", "Cartoon for kids", "School"],
    index=0
)

shorts_max_seconds = None
if video_style == "Shorts":
    shorts_max_seconds = st.selectbox(
        "Shorts max length (filter)",
        [60, 90, 180],
        index=2
    )

max_results = st.slider("Number of results", min_value=1, max_value=10, value=5)

# ── Helper functions ──────────────────────────────────────────────────────────

def enhance_description_with_gemini(user_desc: str, style: str) -> str:
    """Use Gemini 2.5 Flash to rewrite the description into an optimised YouTube search query."""
    style_hint = f" The user prefers videos of type: {style}." if style != "Any" else ""
    prompt = (
        f"You are a YouTube search expert. A user wants to find a YouTube video and describes it as:\n\n"
        f'"{user_desc}"\n\n'
        f"{style_hint}\n"
        f"Rewrite this into a concise, keyword-rich YouTube search query (max 2 sentences) that will return the most relevant results. "
        f"Include important keywords, topic synonyms, and context that YouTube's algorithm responds well to. "
        f"Output ONLY the improved search query — no explanation, no quotes, no extra text."
    )
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()


def style_to_query_boost(style: str) -> str:
    mapping = {
        "Any": "",
        "Shorts": " shorts #shorts vertical",
        "Explainer": " explainer explained breakdown deep dive",
        "Tutorial": " tutorial how to step by step guide",
        "Podcast / Interview": " podcast interview episode longform",
        "Review": " review vs comparison honest",
        "Cartoon for kids": " cartoon animation kids children",
        "School": " school education lesson class",
        "Normal video": "",
    }
    return mapping.get(style, "")


def resolve_channel_id(youtube, name: str):
    if not name.strip():
        return None
    resp = youtube.search().list(q=name, part="snippet", type="channel", maxResults=1).execute()
    items = resp.get("items", [])
    return items[0]["id"].get("channelId") if items else None


def iso8601_to_seconds(duration: str) -> int:
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration)
    if not m:
        return 0
    return int(m.group(1) or 0) * 3600 + int(m.group(2) or 0) * 60 + int(m.group(3) or 0)


def fetch_durations_seconds(youtube, video_ids):
    if not video_ids:
        return {}
    resp = youtube.videos().list(part="contentDetails", id=",".join(video_ids), maxResults=len(video_ids)).execute()
    return {v["id"]: iso8601_to_seconds(v["contentDetails"]["duration"]) for v in resp.get("items", [])}


# ── Main search button ────────────────────────────────────────────────────────
st.markdown("")
if st.button("▶  Find Videos", use_container_width=True):
    if not description.strip():
        st.warning("Please enter a description first.")
    else:
        final_query = description.strip()

        # Step 1 — optionally enhance with Gemini
        if use_ai_flag:
            with st.spinner("✨ Gemini is enhancing your description..."):
                try:
                    enhanced = enhance_description_with_gemini(description.strip(), video_style)
                    final_query = enhanced

                    st.markdown(
                        f'<div class="ai-box">'
                        f'<div class="ai-label">🤖 Gemini-Enhanced Search Query</div>'
                        f'<div class="ai-text">{enhanced}</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                except Exception as e:
                    st.warning(f"Gemini enhancement failed ({e}). Using your original description.")
                    final_query = description.strip()

        # Step 2 — YouTube search
        with st.spinner("🔍 Searching YouTube..."):
            try:
                youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

                q = final_query + style_to_query_boost(video_style)

                channel_id = None
                if channel_name.strip():
                    channel_id = resolve_channel_id(youtube, channel_name.strip())
                    if channel_id is None:
                        st.warning("Couldn't find that channel. Searching across all channels instead.")

                request_kwargs = dict(
                    q=q,
                    part="snippet",
                    type="video",
                    maxResults=max_results,
                    relevanceLanguage="en"
                )
                if channel_id:
                    request_kwargs["channelId"] = channel_id

                items = youtube.search().list(**request_kwargs).execute().get("items", [])

                # Shorts duration filter
                if video_style == "Shorts" and items:
                    video_ids = [it["id"]["videoId"] for it in items]
                    durations = fetch_durations_seconds(youtube, video_ids)
                    items = [it for it in items if durations.get(it["id"]["videoId"], 999999) <= int(shorts_max_seconds)]

                if not items:
                    st.info("No videos found. Try a different description, style, or remove the channel filter.")
                else:
                    st.success(f"✅ Found {len(items)} video(s)!")
                    st.markdown('<hr class="divider">', unsafe_allow_html=True)

                    for item in items:
                        video_id = item["id"]["videoId"]
                        snippet = item["snippet"]
                        title = snippet["title"]
                        channel = snippet["channelTitle"]
                        desc_text = snippet.get("description", "No description available.")
                        thumbnail = snippet["thumbnails"]["medium"]["url"]

                        url = (
                            f"https://www.youtube.com/shorts/{video_id}"
                            if video_style == "Shorts"
                            else f"https://www.youtube.com/watch?v={video_id}"
                        )

                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.image(thumbnail, use_container_width=True)
                        with col2:
                            st.markdown(f"#### [{title}]({url})")
                            st.caption(f"📺 {channel}")
                            st.write(desc_text[:200] + "..." if len(desc_text) > 200 else desc_text)
                            st.markdown(f"🔗 **Link:** [{url}]({url})")

                        st.markdown('<hr class="divider">', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Make sure your API keys are valid and have the correct APIs enabled.")