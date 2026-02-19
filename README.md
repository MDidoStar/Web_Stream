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

## 🗂️ Project Structure

```
web_stream/
├── app.py                  # 🏠 Main landing page
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

- API keys are stored in the source files by default — move them to Streamlit secrets before deploying publicly
- The YouTube search API has a daily quota; each search costs ~100 units (10,000 units/day free tier)
- Gemini AI enhancement is optional — you can skip it and search with your raw description

---

## 🤝 Contributing

Pull requests are welcome! If you build a cool single-purpose app that fits the Web Stream vibe, open a PR and it could be added to the collection.

---

## 📄 License

MIT License — free to use, modify, and distribute.
