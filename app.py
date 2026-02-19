import streamlit as st

st.set_page_config(page_title="Web Stream", page_icon="🌐", layout="centered")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@400;500;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'DM Sans', sans-serif;
        }

        .stApp {
            background: #ffffff;
            color: #111111;
        }

        .hero-title {
            font-family: 'Bebas Neue', sans-serif;
            font-size: 5rem;
            color: #111111;
            text-align: center;
            letter-spacing: 3px;
            margin-bottom: 0.2rem;
            line-height: 1;
        }

        .hero-subtitle {
            text-align: center;
            color: #666666;
            font-size: 1.1rem;
            margin-bottom: 2.5rem;
        }

        .divider {
            border: none;
            border-top: 1px solid #e0e0e0;
            margin: 1.5rem 0;
        }

        .app-card {
            background: #f8f8f8;
            border: 1px solid #e8e8e8;
            border-radius: 14px;
            padding: 1.4rem 1.6rem;
            margin-bottom: 1rem;
            transition: all 0.2s ease;
        }

        .app-card:hover {
            border-color: #cccccc;
            box-shadow: 0 4px 16px rgba(0,0,0,0.07);
        }

        .app-card-title {
            font-family: 'Bebas Neue', sans-serif;
            font-size: 1.5rem;
            color: #111111;
            letter-spacing: 1.5px;
            margin-bottom: 0.2rem;
        }

        .app-card-desc {
            color: #555555;
            font-size: 0.92rem;
            line-height: 1.5;
            margin-bottom: 1rem;
        }

        .stButton > button {
            background: #111111;
            color: #ffffff;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            padding: 0.55rem 1.3rem;
            font-family: 'DM Sans', sans-serif;
            font-size: 0.95rem;
            transition: all 0.2s ease;
            width: 100%;
        }

        .stButton > button:hover {
            background: #333333;
            transform: translateY(-1px);
        }

        .section-label {
            font-family: 'Bebas Neue', sans-serif;
            font-size: 1.1rem;
            color: #aaaaaa;
            letter-spacing: 3px;
            text-align: center;
            margin-bottom: 1.2rem;
        }

        footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">🌐 Web Stream</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">A collection of AI-powered web apps — pick one and dive in.</div>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Available Apps</div>', unsafe_allow_html=True)

# ── App Cards ─────────────────────────────────────────────────────────────────

# App 1 — YouTube Link Finder
st.markdown("""
<div class="app-card">
    <div class="app-card-title">🎬 YouTube Link Finder</div>
    <div class="app-card-desc">
        Describe a video in plain English and let Gemini AI + YouTube Data API find the perfect match.
        Filter by channel, video type, length, and more.
    </div>
</div>
""", unsafe_allow_html=True)
if st.button("Open YouTube Link Finder →", key="btn_yt"):
    st.switch_page("pages/YLF.py")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── README section ────────────────────────────────────────────────────────────
with st.expander("📖 About Web Stream — README"):
    st.markdown("""
# 🌐 Web Stream

**Web Stream** is a growing collection of AI-powered single-purpose web applications,
all living in one Streamlit repo and accessible from a single clean home page.
Each app is self-contained, focused, and built to get things done fast.

---

## 🚀 Apps Included

### 🎬 YouTube Link Finder
Describe a video in plain English (e.g. *"a funny cat compilation"* or
*"a deep-dive tutorial on neural networks"*) and the app finds it for you.

**Features:**
- ✨ Gemini 2.5 Flash AI rewrites your description into a YouTube-optimised search query
- 🔍 YouTube Data API v3 returns the best matching videos
- 📺 Filter by channel, video style (Shorts, Tutorial, Podcast, Review, etc.)
- ⏱️ Shorts duration filtering (60 / 90 / 180 seconds max)
- 🎛️ Choose how many results to return (1–10)

---

## 🗂️ Project Structure

```
web_stream/
├── app.py                  # 🏠 Main landing page (you are here)
├── pages/
│   └── YLF.py               # 🎬 YouTube Link Finder
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.8 or higher
- A YouTube Data API v3 key
- A Google Gemini API key

### Installation

```bash
git clone <your-repo-url>
cd web_stream
pip install -r requirements.txt
```

### API Keys

Open `pages/YLF.py` and replace the placeholder values at the top:

```python
YOUTUBE_API_KEY = "your-youtube-api-key"
GEMINI_API_KEY  = "your-gemini-api-key"
```

Or use Streamlit secrets — create `.streamlit/secrets.toml`:

```toml
YOUTUBE_API_KEY = "your-youtube-api-key"
GEMINI_API_KEY  = "your-gemini-api-key"
```

### Running the App

```bash
streamlit run app.py
```

The home page will open at `http://localhost:8501`.

---

## ☁️ Deploying to Streamlit Cloud

1. Push the repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo
3. Set `app.py` as the main file
4. Add your API keys under **Secrets** in the Streamlit Cloud dashboard
5. Deploy!

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web framework |
| `google-api-python-client` | YouTube Data API |
| `google-generativeai` | Gemini AI |

Install with:
```bash
pip install -r requirements.txt
```

---

## 🛠️ Adding a New App

1. Create a new file inside `pages/` (e.g. `pages/my_app.py`)
2. Add a card + button for it in `app.py`
3. That's it — Streamlit automatically picks it up as a page

---

## 📝 Notes

- API keys are stored in the source files by default — move them to secrets before deploying publicly
- The YouTube search API has a daily quota; each search costs ~100 units (10,000 units/day free)
- Gemini enhancement is optional — you can skip it and search with your raw description

---

## 🤝 Contributing

Pull requests are welcome! If you build a cool single-purpose app that fits the Web Stream vibe,
open a PR and it could be added to the collection.

---

## 📄 License

MIT License — free to use, modify, and distribute.
    """)
