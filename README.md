# 🔎 NextLens

> **See it. Understand it. Know what to do next.**

NextLens is a visual problem-solving assistant powered by **Google Gemini**.  
Users can upload an image or ask a question, and NextLens analyzes the input to provide a clear interpretation and practical next steps.

## ✨ What NextLens Can Do

NextLens currently supports three visual problem-solving areas:

### 📄 Documents
Upload documents such as:

- Bills
- Receipts
- Warranty cards
- Notices
- Forms
- Product labels

NextLens extracts important information such as dates, amounts, names, warnings, and recommended actions.

### 🏠 Household Problems
Upload photos of visible household issues such as:

- Water leaks
- Damp or stained walls
- Cracks
- Damaged objects
- Visible maintenance problems

NextLens explains what can be observed, possible causes, practical next steps, and relevant safety considerations.

### 🌱 Plants
Upload a photo of a plant to get help understanding visible issues such as:

- Discoloration
- Leaf damage
- Wilting
- Possible environmental problems

NextLens provides possible explanations and practical plant-care suggestions.

---

## 💡 How It Works

```text
📸 Image / 💬 Question
        ↓
   Google Gemini
        ↓
🔎 Visual Understanding
        ↓
💡 Interpretation
        ↓
✅ Recommended Next Steps
        ↓
📧 Optional Action Report


Users can also send their analysis as a concise NextLens Action Report to their email using Gmail SMTP.
🛠️ Tech Stack
- Python
- Streamlit — Web interface
- Google Gemini — Vision and conversational AI
- Gmail SMTP — Action Report delivery

📁 Project Structure
NextLens/
│
├── .streamlit/
│   └── secrets.toml.example
│
├── app.py
├── prompts.py
├── requirements.txt
├── README.md
└── .gitignore

Important
The real .streamlit/secrets.toml file is intentionally excluded from GitHub.
Never commit API keys, passwords, or other credentials to the repository.

🚀 Run Locally
1. Clone the repository
git clone https://github.com/Pravallikayalluru/NextLens.git
cd NextLens

2. Create a virtual environment
Windows:
python -m venv venv

Activate it:
venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Configure secrets
Create:
.streamlit/secrets.toml

Use the provided example as a template:
GEMINI_API_KEY = "your-gemini-api-key"
GMAIL_ADDRESS = "your-gmail-address@gmail.com"
GMAIL_APP_PASSWORD = "your-gmail-app-password"

5. Run the application
streamlit run app.py

The application will open in your browser.
🔐 Security
The repository includes a .gitignore that excludes:
.streamlit/secrets.toml
venv/
__pycache__/

Only the safe template:
.streamlit/secrets.toml.example

is included in the repository.
Never upload your real Gemini API key or Gmail App Password to GitHub.
📧 Action Reports
After completing an analysis, users can select:
📧 Send My Action Report
NextLens generates a concise summary of the conversation and sends it to the user's registered email address through Gmail SMTP.
🎯 Project Goal
NextLens is designed around a simple idea:
Don't just tell users what they are looking at — help them understand what it means and what they can do next.
