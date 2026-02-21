import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="Contact Us",
    page_icon="📧",
    layout="centered"
)

# ---------------------------
# Styling
# ---------------------------
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@400;500;600&display=swap');
        html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
        .stApp { background: #ffffff; color: #111111; }
        .hero-title {
            font-family: 'Bebas Neue', sans-serif;
            font-size: 3.5rem; color: #111111;
            text-align: center; letter-spacing: 3px;
            margin-bottom: 0.2rem; line-height: 1;
        }
        .hero-subtitle { text-align: center; color: #666666; font-size: 1rem; margin-bottom: 2rem; }
        .divider { border: none; border-top: 1px solid #e0e0e0; margin: 1.5rem 0; }
        .stButton > button {
            background: #111111; color: #ffffff; font-weight: 600;
            border: none; border-radius: 8px; padding: 0.6rem 1.4rem;
            font-family: 'DM Sans', sans-serif; font-size: 1rem;
            transition: all 0.2s ease; width: 100%;
        }
        .stButton > button:hover { background: #333333; transform: translateY(-1px); }
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
st.markdown('<div class="hero-title">📧 Send Us a Message</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Fill in your email and message — we\'ll get back to you!</div>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ---------------------------
# Load credentials from secrets
# ---------------------------
try:
    SENDER_EMAIL    = st.secrets["GMAIL_SENDER"]
    SENDER_PASSWORD = st.secrets["GMAIL_APP_PASSWORD"]
except KeyError:
    st.error("⚠️ Gmail credentials not configured. Add GMAIL_SENDER and GMAIL_APP_PASSWORD to Streamlit secrets.")
    st.stop()

# ---------------------------
# Send function
# ---------------------------
def send_email(recipient: str, user_message: str) -> tuple[bool, str]:
    try:
        msg = MIMEMultipart("alternative")
        msg["From"]     = SENDER_EMAIL
        msg["To"]       = recipient
        msg["Subject"]  = "📩 We received your message!"
        msg["Reply-To"] = recipient

        plain = f"Hi!\n\nThanks for reaching out. Here's a copy of your message:\n\n{user_message}\n\n— Web Stream Team"

        html = f"""
        <html>
          <body style="font-family:Arial,sans-serif;color:#333;max-width:600px;margin:auto;padding:20px;">
            <h2 style="color:#111;border-bottom:2px solid #eee;padding-bottom:10px;">
              📩 We received your message!
            </h2>
            <p style="color:#555;">Hi there,</p>
            <p style="color:#555;">Thanks for reaching out. Here's a copy of what you sent us:</p>
            <div style="background:#f8f8f8;border-left:4px solid #111;border-radius:6px;
                        padding:16px 20px;margin:20px 0;color:#333;white-space:pre-wrap;">{user_message}</div>
            <p style="color:#555;">We'll get back to you as soon as possible.</p>
            <hr style="border:none;border-top:1px solid #eee;margin:24px 0;">
            <p style="color:#aaa;font-size:12px;text-align:center;">Sent via 🌐 Web Stream</p>
          </body>
        </html>
        """

        msg.attach(MIMEText(plain, "plain"))
        msg.attach(MIMEText(html,  "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient, msg.as_string())

        return True, ""

    except smtplib.SMTPAuthenticationError:
        return False, "Authentication failed. Check GMAIL_SENDER and GMAIL_APP_PASSWORD in Streamlit secrets."
    except smtplib.SMTPRecipientsRefused:
        return False, "The recipient email address was refused. Please double-check it."
    except Exception as e:
        return False, str(e)

# ---------------------------
# Form
# ---------------------------
st.subheader("✍️ Compose Your Message")

recipient_email = st.text_input(
    "Your Email Address",
    placeholder="yourname@example.com",
    help="A confirmation copy will be sent to this address."
)

message_body = st.text_area(
    "Your Message",
    placeholder="Type your message here...",
    height=220
)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ---------------------------
# Send Button
# ---------------------------
if st.button("📤 Send Message", use_container_width=True):
    errors = []
    if not recipient_email or "@" not in recipient_email or "." not in recipient_email:
        errors.append("Please enter a valid email address.")
    if not message_body.strip():
        errors.append("Please write a message before sending.")

    if errors:
        for err in errors:
            st.error(err)
    else:
        with st.spinner("Sending your message..."):
            success, error_msg = send_email(recipient_email.strip(), message_body.strip())

        if success:
            st.success(f"✅ Message sent! Check **{recipient_email}** for your confirmation copy.")
            st.balloons()
        else:
            st.error(f"❌ Failed to send: {error_msg}")

# ---------------------------
# Footer
# ---------------------------
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.caption("📧 Powered by Gmail SMTP · Web Stream")
