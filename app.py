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

# App 2 — FLITO: AI Traveling Blogger
st.markdown("""
<div class="app-card">
    <div class="app-card-title">🌍 FLITO: AI Traveling Blogger</div>
    <div class="app-card-desc">
        Your AI-powered travel companion. Find hotels, restaurants, tourist attractions, and transportation.
        Plan your budget, convert currencies, translate languages, and build a premium day-by-day trip itinerary.
    </div>
</div>
""", unsafe_allow_html=True)
if st.button("Open FLITO →", key="btn_flito"):
    st.switch_page("pages/FLITO.py")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# App 3 — Blink Smart
st.markdown("""
<div class="app-card">
    <div class="app-card-title">👁️ Blink Smart: Eye Health Suite</div>
    <div class="app-card-desc">
        Monitor and analyse your eye health with AI. Capture webcam frames for a Gemini-powered blink pattern
        analysis with a downloadable PDF report, or run a live 5-minute blink-rate monitor to prevent digital
        eye strain.
    </div>
</div>
""", unsafe_allow_html=True)
if st.button("Open Blink Smart →", key="btn_blink"):
    st.switch_page("pages/BlinkSmart.py")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# App 4 — Gmail Sender
st.markdown("""
<div class="app-card">
    <div class="app-card-title">📧 Gmail Sender</div>
    <div class="app-card-desc">
        Send emails instantly via the Gmail API. Enter your Gmail address and compose your message —
        supports both plain text and HTML formatting. Powered by Google Service Account.
    </div>
</div>
""", unsafe_allow_html=True)
if st.button("Open Gmail Sender →", key="btn_gmail"):
    st.switch_page("pages/GmailSender.py")

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
Describe a video in plain English and let Gemini + YouTube Data API find it for you.
Filter by channel, video type (Shorts, Tutorial, Podcast, Review…), and length.

### 🌍 FLITO: AI Traveling Blogger
Hotels, restaurants, tourism, transport, shopping, budget tracking, currency conversion,
translation, and a premium AI trip-builder — all in one place.

### 👁️ Blink Smart: Eye Health Suite
Capture 120 webcam frames for an AI blink-pattern analysis (with PDF report), or run
a real-time 5-minute blink-rate monitor powered by MediaPipe Face Mesh.

### 📧 Gmail Sender
Send plain-text or HTML emails via the Gmail API using a Google Service Account.
Enter your Gmail address, your message, and hit send — that's it.

---

## 🗂️ Project Structure

```
web_stream/
├── app.py                      # 🏠 Main landing page (you are here)
├── pages/
│   ├── YLF.py                  # 🎬 YouTube Link Finder
│   ├── FLITO.py                # 🌍 AI Traveling Blogger
│   ├── BlinkSmart.py           # 👁️ Blink Smart hub
│   ├── Blink_Analysis.py       # 📸 AI blink analysis + PDF
│   ├── Blink_Monitor.py        # ⏱️ Real-time blink monitor
│   └── GmailSender.py          # 📧 Gmail Sender
├── countries.csv               # Country / city / currency data
├── requirements.txt            # Python dependencies
└── README.md
```

---

## ⚙️ Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

Add API keys to `.streamlit/secrets.toml`:

```toml
YOUTUBE_API_KEY = "..."
GEMINI_API_KEY  = "..."

[GMAIL_SERVICE_ACCOUNT]
type = "service_account"
project_id = "your-project-id"
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\\n...\\n-----END PRIVATE KEY-----\\n"
client_email = "your-sa@your-project.iam.gserviceaccount.com"
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
universe_domain = "googleapis.com"
```

---

## 🛠️ Adding a New App

1. Create `pages/my_app.py`
2. Add a card + button in `app.py`
3. Done — Streamlit picks it up automatically.

---

## 📄 License
MIT License — free to use, modify, and distribute.
    """)
