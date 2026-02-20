import streamlit as st
import json
import base64
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="Gmail Sender",
    page_icon="📧",
    layout="centered"
)

# ---------------------------
# Styling (matches Web Stream theme)
# ---------------------------
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
            font-size: 3.5rem;
            color: #111111;
            text-align: center;
            letter-spacing: 3px;
            margin-bottom: 0.2rem;
            line-height: 1;
        }

        .hero-subtitle {
            text-align: center;
            color: #666666;
            font-size: 1rem;
            margin-bottom: 2rem;
        }

        .divider {
            border: none;
            border-top: 1px solid #e0e0e0;
            margin: 1.5rem 0;
        }

        .stButton > button {
            background: #111111;
            color: #ffffff;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.4rem;
            font-family: 'DM Sans', sans-serif;
            font-size: 1rem;
            transition: all 0.2s ease;
            width: 100%;
        }

        .stButton > button:hover {
            background: #333333;
            transform: translateY(-1px);
        }

        .success-box {
            background: #f0fdf4;
            border: 1px solid #86efac;
            border-left: 4px solid #22c55e;
            border-radius: 8px;
            padding: 1rem 1.2rem;
            margin: 1rem 0;
        }

        .error-box {
            background: #fef2f2;
            border: 1px solid #fca5a5;
            border-left: 4px solid #ef4444;
            border-radius: 8px;
            padding: 1rem 1.2rem;
            margin: 1rem 0;
        }

        footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# Back button
# ---------------------------
if st.button("← Back to Web Stream"):
    st.switch_page("app.py")

# ---------------------------
# Header
# ---------------------------
st.markdown('<div class="hero-title">📧 Gmail Sender</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Send emails instantly via Gmail API</div>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ---------------------------
# Load service account credentials
# ---------------------------
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), "gmail_service_account.json")
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def get_gmail_service(sender_email: str):
    """Build Gmail service using service account with domain-wide delegation."""
    try:
        # Try loading from secrets first, fallback to local file
        if "GMAIL_SERVICE_ACCOUNT" in st.secrets:
            sa_info = dict(st.secrets["GMAIL_SERVICE_ACCOUNT"])
        elif os.path.exists(SERVICE_ACCOUNT_FILE):
            with open(SERVICE_ACCOUNT_FILE, "r") as f:
                sa_info = json.load(f)
        else:
            return None, "Service account credentials not found. Add GMAIL_SERVICE_ACCOUNT to Streamlit secrets."

        credentials = service_account.Credentials.from_service_account_info(
            sa_info,
            scopes=SCOPES
        )
        # Delegate to the sender's Gmail account
        delegated_credentials = credentials.with_subject(sender_email)
        service = build("gmail", "v1", credentials=delegated_credentials)
        return service, None

    except Exception as e:
        return None, f"Credentials error: {str(e)}"


def create_message(sender: str, recipient: str, subject: str, body: str, is_html: bool = False):
    """Create a MIME email message encoded for the Gmail API."""
    msg = MIMEMultipart("alternative")
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject

    if is_html:
        part = MIMEText(body, "html")
    else:
        part = MIMEText(body, "plain")
    msg.attach(part)

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
    return {"raw": raw}


def send_email(service, sender: str, recipient: str, subject: str, body: str, is_html: bool = False):
    """Send an email via the Gmail API."""
    try:
        message = create_message(sender, recipient, subject, body, is_html)
        sent = service.users().messages().send(userId="me", body=message).execute()
        return sent.get("id"), None
    except HttpError as e:
        error_detail = json.loads(e.content.decode()).get("error", {})
        return None, f"Gmail API error {e.resp.status}: {error_detail.get('message', str(e))}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"


# ---------------------------
# ⚠️  Domain-wide delegation note
# ---------------------------
with st.expander("ℹ️ How this works — Setup info"):
    st.markdown("""
    This page uses a **Google Service Account** with **Gmail API** to send emails on your behalf.

    **Requirements for this to work:**
    1. The service account must have **Domain-Wide Delegation** enabled in Google Workspace Admin Console.
    2. The Gmail API scope (`https://www.googleapis.com/auth/gmail.send`) must be authorized for the service account client ID in the Admin Console under *Security → API Controls → Domain-wide Delegation*.
    3. The **sender email** you enter must belong to the same Google Workspace domain as the service account.

    **Service Account in use:** `gmail-api@norse-blade-487920-u5.iam.gserviceaccount.com`

    If you get a `403` or delegation error, check that domain-wide delegation is properly configured.
    """)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ---------------------------
# Email Form
# ---------------------------
st.subheader("✍️ Compose Your Email")

col1, col2 = st.columns(2)
with col1:
    sender_email = st.text_input(
        "Your Gmail Address (sender)",
        placeholder="you@yourdomain.com",
        help="Must be a Gmail / Google Workspace account in the same domain as the service account."
    )
with col2:
    recipient_email = st.text_input(
        "Recipient Email",
        placeholder="recipient@example.com"
    )

subject = st.text_input(
    "Subject",
    placeholder="Enter email subject...",
    value="Hello from Web Stream!"
)

# Message type toggle
msg_type = st.radio(
    "Message Format",
    options=["Plain Text", "HTML"],
    horizontal=True,
    help="HTML lets you use bold, links, colors etc."
)

is_html = msg_type == "HTML"

if is_html:
    message_body = st.text_area(
        "Message (HTML)",
        placeholder="<h2>Hello!</h2><p>This is an <b>HTML</b> email from Web Stream 🌐</p>",
        height=220
    )
    with st.expander("📋 HTML Template"):
        st.code("""<html>
  <body style="font-family: Arial, sans-serif; color: #333;">
    <h2 style="color: #111;">Hello!</h2>
    <p>This is an email sent via <b>Web Stream</b> 🌐</p>
    <hr>
    <p style="color: #888; font-size: 12px;">Sent with Gmail API</p>
  </body>
</html>""", language="html")
else:
    message_body = st.text_area(
        "Message",
        placeholder="Type your message here...",
        height=220
    )

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ---------------------------
# Send Button
# ---------------------------
if st.button("📤 Send Email", use_container_width=True):
    # Validate inputs
    errors = []
    if not sender_email or "@" not in sender_email:
        errors.append("Please enter a valid sender email address.")
    if not recipient_email or "@" not in recipient_email:
        errors.append("Please enter a valid recipient email address.")
    if not subject.strip():
        errors.append("Please enter a subject.")
    if not message_body.strip():
        errors.append("Please enter a message.")

    if errors:
        for err in errors:
            st.error(err)
    else:
        with st.spinner("Connecting to Gmail API and sending..."):
            service, err = get_gmail_service(sender_email)

            if err:
                st.markdown(
                    f'<div class="error-box">❌ <b>Connection failed:</b> {err}</div>',
                    unsafe_allow_html=True
                )
            else:
                msg_id, send_err = send_email(
                    service,
                    sender=sender_email,
                    recipient=recipient_email,
                    subject=subject,
                    body=message_body,
                    is_html=is_html
                )

                if send_err:
                    st.markdown(
                        f'<div class="error-box">❌ <b>Failed to send:</b> {send_err}</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<div class="success-box">✅ <b>Email sent successfully!</b><br>'
                        f'<span style="color:#555; font-size:0.88rem;">Message ID: <code>{msg_id}</code></span></div>',
                        unsafe_allow_html=True
                    )
                    st.balloons()

# ---------------------------
# Footer
# ---------------------------
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.caption("📧 Powered by Gmail API + Google Service Account")
