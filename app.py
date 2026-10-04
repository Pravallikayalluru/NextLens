import re
import smtplib

from email.mime.text import MIMEText

import streamlit as st

from google import genai
from google.genai import types

from prompts import (
    SUMMARY_REQUEST_PROMPT,
    SYSTEM_PROMPT,
    WELCOME_MESSAGE_TEMPLATE
)


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = "gemini-3.5-flash"

st.set_page_config(
    page_title="NextLens",
    page_icon="🔎",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0;
    }

    .tagline {
        text-align: center;
        font-size: 18px;
        margin-bottom: 25px;
    }

    .category-card {
        padding: 18px;
        border: 1px solid rgba(128,128,128,0.25);
        border-radius: 14px;
        margin-bottom: 10px;
        min-height: 130px;
    }

    .category-title {
        font-size: 20px;
        font-weight: 700;
    }

    .category-description {
        font-size: 14px;
        opacity: 0.8;
    }

    .user-info {
        padding: 10px 14px;
        border-radius: 10px;
        background: rgba(128,128,128,0.08);
        margin-bottom: 20px;
    }

    .supported-box {
        padding: 10px 14px;
        border-radius: 10px;
        background: rgba(128,128,128,0.06);
        margin-bottom: 15px;
        font-size: 14px;
    }

    .report-box {
        padding: 15px;
        border-radius: 12px;
        background: rgba(128,128,128,0.06);
        margin-bottom: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SECRETS
# ============================================================

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

GMAIL_ADDRESS = st.secrets["GMAIL_ADDRESS"]

GMAIL_APP_PASSWORD = st.secrets["GMAIL_APP_PASSWORD"]


# ============================================================
# GEMINI CLIENT
# ============================================================

@st.cache_resource
def get_gemini_client():

    return genai.Client(
        api_key=GEMINI_API_KEY
    )


gemini_client = get_gemini_client()


# ============================================================
# RESPONSE CLEANING
# ============================================================

def clean_response(text):
    """
    Remove unwanted HTML tags from Gemini responses
    while preserving useful line breaks.
    """

    if not text:
        return ""

    # Convert common HTML line breaks to new lines
    text = re.sub(
        r"<br\s*/?>",
        "\n",
        text,
        flags=re.IGNORECASE
    )

    # Remove common formatting tags
    text = re.sub(
        r"</?(b|strong|i|em|div|span|p|section|article)[^>]*>",
        "",
        text,
        flags=re.IGNORECASE
    )

    # Remove any remaining HTML tags
    text = re.sub(
        r"<[^>]+>",
        "",
        text
    )

    return text.strip()


# ============================================================
# MESSAGE RENDERING
# ============================================================

def render_message(message):

    with st.chat_message(message["role"]):

        if message["kind"] == "text":

            clean_text = clean_response(
                message["content"]
            )

            st.markdown(
                clean_text
            )

        elif message["kind"] == "image":

            st.image(
                message["content"],
                use_container_width=True
            )


def add_message(role, kind, content):

    st.session_state.messages.append(
        {
            "role": role,
            "kind": kind,
            "content": content
        }
    )

    render_message(
        st.session_state.messages[-1]
    )


# ============================================================
# GEMINI CHAT
# ============================================================

def ask_gemini(parts):

    try:

        response = st.session_state.chat.send_message(
            parts
        )

        return response.text

    except Exception as error:

        return (
            "Sorry, something went wrong:\n\n"
            f"{error}"
        )


# ============================================================
# EMAIL CLEANING
# ============================================================

def clean_email_text(text):

    if not text:

        return "No Action Report available."

    return clean_response(text).strip()


# ============================================================
# SEND EMAIL
# ============================================================

def send_email(
    to_address,
    user_name,
    summary
):

    try:

        body = (
            f"Hi {user_name},\n\n"
            f"Here is your NextLens Action Report:\n\n"
            f"{clean_email_text(summary)}\n\n"
            f"---\n"
            f"Generated by NextLens 🔎\n"
            f"See it. Understand it. Know what to do next."
        )

        message = MIMEText(
            body,
            "plain",
            "utf-8"
        )

        message["Subject"] = (
            "NextLens Action Report 🔎"
        )

        message["From"] = GMAIL_ADDRESS

        message["To"] = to_address

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        ) as server:

            server.login(
                GMAIL_ADDRESS,
                GMAIL_APP_PASSWORD
            )

            server.send_message(
                message
            )

        return True, "Email sent successfully"

    except Exception as error:

        return False, str(error)


# ============================================================
# STEP 1 — ONBOARDING
# ============================================================

if "onboarded" not in st.session_state:

    st.markdown(
        '<div class="main-title">🔎 NextLens</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="tagline">'
        'See it. Understand it. Know what to do next.'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Turn a photo into a clear next step."
    )

    st.write("### What can NextLens help with?")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="category-card">

            <div class="category-title">
            📄 Documents
            </div>

            <div class="category-description">
            Understand bills, receipts, warranty cards,
            notices, forms and labels.
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="category-card">

            <div class="category-title">
            🏠 Household Problems
            </div>

            <div class="category-description">
            Understand visible leaks, stains, damage,
            cracks and maintenance problems.
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
            <div class="category-card">

            <div class="category-title">
            🌱 Plants
            </div>

            <div class="category-description">
            Identify visible plant problems and get
            practical care suggestions.
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    with st.form("onboarding_form"):

        name = st.text_input(
            "Your name"
        )

        email_address = st.text_input(
            "Email address",
            placeholder="yourname@gmail.com",
            help=(
                "This is the email address where "
                "NextLens will send your Action Report."
            )
        )

        submitted = st.form_submit_button(
            "Let's go 🚀"
        )

    if submitted:

        if (
            not name.strip()
            or not email_address.strip()
        ):

            st.warning(
                "Please fill in both your name "
                "and email address."
            )

        else:

            st.session_state.name = (
                name.strip()
            )

            st.session_state.email_address = (
                email_address.strip()
            )

            # Create Gemini conversation
            st.session_state.chat = (
                gemini_client.chats.create(
                    model=MODEL_NAME,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT
                    ),
                )
            )

            st.session_state.messages = []

            st.session_state.onboarded = True

            st.rerun()

    st.stop()


# ============================================================
# STEP 2 — MAIN HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🔎 NextLens</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="tagline">'
    'See it. Understand it. Know what to do next.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# USER INFORMATION
# ============================================================

st.markdown(
    f"""
    <div class="user-info">
    👤 <b>{st.session_state.name}</b>
    &nbsp; • &nbsp;
    📧 Reports go to {st.session_state.email_address}
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SUPPORTED AREAS
# ============================================================

st.markdown(
    """
    <div class="supported-box">
    📄 Documents &nbsp;&nbsp;|&nbsp;&nbsp;
    🏠 Household Problems &nbsp;&nbsp;|&nbsp;&nbsp;
    🌱 Plants
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# STEP 3 — CHAT HISTORY
# ============================================================

if not st.session_state.messages:

    add_message(
        "assistant",
        "text",
        WELCOME_MESSAGE_TEMPLATE.format(
            name=st.session_state.name
        )
    )

else:

    for message in st.session_state.messages:

        render_message(message)


# ============================================================
# STEP 4 — USER INPUT
# ============================================================

user_input = st.chat_input(
    "📸 Upload a photo or ask NextLens a question...",
    accept_file=True,
    file_type=[
        "jpg",
        "jpeg",
        "png"
    ],
)


# ============================================================
# STEP 5 — PROCESS USER INPUT
# ============================================================

if user_input:

    photo = (
        user_input.files[0]
        if user_input.files
        else None
    )

    text = user_input.text

    parts = []


    # --------------------------------------------------------
    # IMAGE
    # --------------------------------------------------------

    if photo is not None:

        photo_bytes = photo.getvalue()

        add_message(
            "user",
            "image",
            photo_bytes
        )

        parts.append(
            types.Part.from_bytes(
                data=photo_bytes,
                mime_type=photo.type
            )
        )


    # --------------------------------------------------------
    # TEXT
    # --------------------------------------------------------

    if text:

        add_message(
            "user",
            "text",
            text
        )

        parts.append(text)


    # --------------------------------------------------------
    # IMAGE WITHOUT TEXT
    # --------------------------------------------------------

    elif photo is not None:

        parts.append(
            """
            Analyze this image using the NextLens guidelines.

            First determine which supported area best
            matches the image:

            1. 📄 Document
            2. 🏠 Household Problem
            3. 🌱 Plant

            Then explain:

            - What you can clearly observe
            - What it could possibly mean
            - What the user should do next
            - Any important safety consideration

            Do not invent information.

            If the exact cause cannot be determined from
            the image, clearly say that it is uncertain.

            Use plain Markdown only.

            IMPORTANT:
            Never use HTML tags such as <br>, <div>,
            <p>, <b>, <strong>, <span>, etc.

            Use:
            - Markdown headings
            - Bold text
            - Bullet points
            - Emojis
            - Clear spacing

            Keep the answer practical and concise.
            """
        )


    # --------------------------------------------------------
    # ASK GEMINI
    # --------------------------------------------------------

    with st.spinner(
        "NextLens is analyzing..."
    ):

        answer = ask_gemini(
            parts
        )


    # --------------------------------------------------------
    # DISPLAY GEMINI RESPONSE
    # --------------------------------------------------------

    add_message(
        "assistant",
        "text",
        answer
    )


# ============================================================
# STEP 6 — SEND ACTION REPORT
# ============================================================

st.divider()

has_user_message = any(
    message["role"] == "user"
    for message in st.session_state.messages
)

st.markdown(
    """
    <div class="report-box">

    📧 <b>Action Report</b><br>

    Get a concise summary of your NextLens analysis
    delivered to your email.

    </div>
    """,
    unsafe_allow_html=True
)

if st.button(
    "📧 Send My Action Report",
    disabled=not has_user_message,
    use_container_width=True,
    key="send_action_report"
):

    with st.spinner(
        "Preparing your Action Report..."
    ):

        summary = ask_gemini(
            [SUMMARY_REQUEST_PROMPT]
        )

    success, info = send_email(
        st.session_state.email_address,
        st.session_state.name,
        summary
    )

    if success:

        st.success(
            "Report sent! Check your email 📧"
        )

    else:

        st.error(
            f"Couldn't send the report: {info}"
        )