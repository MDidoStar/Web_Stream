# 🌐 Web Stream

**Web Stream** is a growing collection of AI-powered single-purpose web applications, all living in one Streamlit repo and accessible from a single clean home page. Each app is self-contained, focused, and built to get things done fast.

---

## 🚀 Apps Included

### 🎬 YouTube Link Finder
Describe a video in plain English (e.g. *"a funny cat compilation"* or *"a deep-dive tutorial on neural networks"*) and the app finds it for you.

**Features:**
- ✨ Gemini 2.5 Flash AI rewrites your description into a YouTube-optimised search query
- 🔍 YouTube Data API v3 returns the best matching videos
- 📺 Filter by channel, video style (Shorts, Tutorial, Podcast, Review, etc.)
- ⏱️ Shorts duration filtering (60 / 90 / 180 seconds max)
- 🎛️ Choose how many results to return (1–10)

---

### 🌍 FLITO: AI Traveling Blogger
Your all-in-one AI travel companion. Find hotels, restaurants, tourist attractions, and transport options — then plan your budget, convert currencies, translate languages, and build a premium day-by-day trip itinerary.

**Features:**
- 🏨 Hotel search with star rating and price filters
- 🍝 Restaurant & cafe finder with cuisine and rating filters
- 🏝️ Tourist attraction discovery by type and activity preference
- 🚗 Transportation options between locations
- 🛍️ Shopping recommendations (malls, markets, boutiques)
- 💰 Trip budget tracker with expense management
- 💱 Real-time currency converter (ExchangeRate-API)
- 🗣️ Language translator powered by Gemini AI
- ✈️ Premium trip builder — full day-by-day itineraries with voice input support (code: `5555`)
- 🗺️ Interactive map with location search (Folium + Nominatim)
- 📄 PDF download for all AI-generated recommendations

---

### 👁️ Blink Smart: Eye Health Suite
Monitor and analyse your eye health with AI. Two tools in one:

#### 📸 Blink Analysis
- Capture 120 webcam frames with live preview
- AI-powered blink pattern analysis via Gemini 2.5 Flash
- Personalised recommendations based on country, city, and age
- Downloadable PDF report

#### ⏱️ Blink Monitor
- Real-time blink rate tracking using MediaPipe Face Mesh
- 5-minute monitoring sessions with countdown timer
- EAR (Eye Aspect Ratio) based blink detection
- Animated on-screen reminder when blink rate drops below 20/min
- Debug overlay showing live EAR values

---

### 📧 Contact Us
Send emails directly from the browser using Gmail SMTP. Enter your Gmail address, compose your message, and hit send — a confirmation copy is delivered to your inbox.

**Features:**
- ✉️ Send plain text or HTML-formatted emails
- 📬 Confirmation copy sent to the recipient's address
- 🔐 Credentials stored securely in Streamlit secrets (never committed to version control)
- 🎨 Clean, minimal interface matching the Web Stream design language

---

## 🗂️ Project Structure

```
web_stream/
├── app.py                      # 🏠 Main landing page
├── pages/
│   ├── YLF.py                  # 🎬 YouTube Link Finder
│   ├── FLITO.py                # 🌍 AI Traveling Blogger
│   ├── BlinkSmart.py           # 👁️ Blink Smart hub
│   ├── Blink_Analysis.py       # 📸 AI blink analysis + PDF report
│   ├── Blink_Monitor.py        # ⏱️ Real-time blink monitor
│   └── Contact_Us.py          # 📧 Contact Us via Gmail
├── countries.csv               # Country / city / currency data
├── requirements.txt            # Python dependencies
├── packages.txt                # System dependencies
├── runtime.txt                 # Python version
└── README.md                   # This file
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10 or higher
- A YouTube Data API v3 key
- A Google Gemini API key
- A Gmail account with an App Password (for Gmail Sender)

### Installation

```bash
git clone <your-repo-url>
cd web_stream
pip install -r requirements.txt
```

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web framework |
| `google-generativeai` | Gemini AI (YouTube Link Finder, FLITO, Blink Analysis) |
| `google-api-python-client` | YouTube Data API |
| `folium` + `streamlit-folium` | Interactive map in FLITO |
| `geopy` | Location geocoding in FLITO |
| `requests` | Currency exchange API calls |
| `SpeechRecognition` | Voice input in FLITO Trip Builder |
| `reportlab` | PDF generation (FLITO + Blink Analysis) |
| `pandas` | Country/city/currency data loading |
| `mediapipe` | Face mesh & EAR blink detection |
| `opencv-python-headless` | Webcam frame processing |

Install all with:
```bash
pip install -r requirements.txt
```

System dependencies (for Streamlit Cloud — `packages.txt`):
```
libgl1
libglib2.0-0
```

---

## 🧭 Navigation

All apps are accessible from the **Web Stream home page** (`app.py`). Each app has a **← Back to Web Stream** button to return home. The Blink Smart hub (`BlinkSmart.py`) also links to its two sub-tools, which each have a **← Back to Blink Smart** button.

```
app.py (Web Stream Home)
├── pages/YLF.py
├── pages/FLITO.py
├── pages/BlinkSmart.py
│   ├── pages/Blink_Analysis.py
│   └── pages/Blink_Monitor.py
└── pages/Contact_Us.py
```

---


## 📝 Notes

- API keys are stored in Streamlit secrets — never commit them to version control
- The YouTube search API has a daily quota; each search costs ~100 units (10,000 units/day free tier)
- Gemini AI enhancement is optional in the YouTube Link Finder — you can search with your raw description
- The FLITO Trip Builder is behind a premium code (I will say it later) — change this in `pages/FLITO.py` to suit your needs
- Blink Smart requires camera permissions; some browsers may block camera access inside iframes
- Gmail Sender requires a Gmail App Password — enable 2FA on your Google account and generate one at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)

---

## 🤝 Contributing

Pull requests are welcome! If you build a cool single-purpose app that fits the Web Stream vibe, open the contact us and it could be added to the collection.

---

## 📄 License

MIT License — free to use, modify, and distribute.
