import streamlit as st
import joblib
import base64
from pathlib import Path

# =====================================
# PAGE CONFIGURATION
# =====================================
st.set_page_config(
    page_title="AI Customer Support Chatbot",
    page_icon="🤖",
    layout="wide"
)

# =====================================
# PROJECT PATHS
# =====================================
PROJECT_DIR = Path(r"D:\AI Engineer\Task 2 AI Customer Support Chatbot")
BACKGROUND_PATH = PROJECT_DIR / "chatbot_bg.png.png"

# =====================================
# LOAD TRAINED MODEL
# =====================================
@st.cache_resource
def load_model():
    model = joblib.load(PROJECT_DIR / "outputs" / "intent_model.pkl")
    vectorizer = joblib.load(PROJECT_DIR / "outputs" / "tfidf_vectorizer.pkl")
    return model, vectorizer

try:
    model, vectorizer = load_model()
except Exception as e:
    st.error("Unable to load the trained model.")
    st.code(str(e))
    st.stop()

# =====================================
# FUTURISTIC BACKGROUND AND UI
# =====================================
if BACKGROUND_PATH.exists():
    encoded_image = base64.b64encode(
        BACKGROUND_PATH.read_bytes()
    ).decode("utf-8")

    background_css = f"""
        background-image:
            linear-gradient(
                rgba(7, 12, 28, 0.78),
                rgba(7, 12, 28, 0.88)
            ),
            url("data:image/png;base64,{encoded_image}");
    """
else:
    background_css = """
        background: linear-gradient(135deg, #080c1c, #11152b, #17102c);
    """

st.markdown(
    f"""
    <style>
    .stApp {{
        {background_css}
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    [data-testid="stSidebar"] {{
        background: rgba(16, 21, 40, 0.96);
        border-right: 1px solid rgba(80, 150, 255, 0.25);
    }}

    h1 {{
        color: #f4f7ff;
        text-shadow: 0 0 18px rgba(45, 160, 255, 0.35);
    }}

    [data-testid="stChatMessage"] {{
        background: rgba(20, 29, 53, 0.78);
        border: 1px solid rgba(75, 150, 255, 0.25);
        border-radius: 16px;
        padding: 14px;
    }}

    [data-testid="stChatInput"] {{
        border: 1px solid #4c8dff;
        border-radius: 16px;
    }}

    [data-testid="stChatInput"] textarea {{
        color: white;
    }}

    [data-testid="stCaptionContainer"] {{
        color: #b9c8e8;
    }}

    div.stButton > button {{
        border-radius: 10px;
        border: 1px solid #557dff;
        transition: all 0.2s ease;
    }}

    div.stButton > button:hover {{
        border-color: #00d4ff;
        color: #00d4ff;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# =====================================
# CUSTOMER SUPPORT RESPONSES
# =====================================
responses = {
    "yesNode": "Thank you for confirming! How else can I assist you?",
    "noNode": "No problem. Please let me know if you need help.",
    "playOtherGame": "I'd be happy to help. Could you share more details?",
    "volumeDown": "Please describe your issue so I can help you find a solution.",
    "volumeUp": "Welcome to customer support! How can I help you today?",
    "listOfGames": "I can guide you with account, order, payment, and general enquiries.",
    "maybeNode": "Take your time. I'm here if you need assistance.",
    "stop": "Your support conversation has ended. Feel free to return anytime.",
    "Repeat": "Of course! Please tell me which information you'd like repeated.",
    "timesPlayed": "Please provide more details about your support request.",
    "gamesCounter": "I'm here to help with your customer support questions.",
    "wait": "Of course. Take your time!",
    "stillThere": "Yes, I'm here and ready to help! 😊",
    "totalStop": "Thank you for contacting support. Have a great day!",
    "greeting": "Hello! 👋 Welcome to AI Customer Support. How can I help you today?",
    "unknown": "Sorry, I couldn't understand your request. Please explain your issue another way."
}

# =====================================
# CHATBOT LOGIC
# =====================================
def chatbot(user_input):
    text = user_input.lower().strip()

    # Greetings
    if text in ["hi", "hello", "hey", "hi there", "hello bot"]:
        return "greeting", responses["greeting"]

    # Chatbot identity
    if any(p in text for p in [
        "what is your name", "what's your name",
        "who are you", "tell me your name"
    ]):
        return "greeting", "I'm your AI Customer Support Assistant! 🤖"

    # Account and password help
    if any(p in text for p in [
        "password", "forgot password", "login", "log in",
        "account access", "locked account"
    ]):
        return "account_support", (
            "For account access issues, try the 'Forgot Password' option "
            "on the sign-in page. If the issue continues, contact the service's support team."
        )

    # Order and delivery
    if any(p in text for p in [
        "order", "delivery", "shipping", "track my parcel",
        "where is my package"
    ]):
        return "order_support", (
            "To check your order, open your order history and select the order "
            "to view its status. Contact the seller if tracking is unavailable."
        )

    # Refunds and cancellations
    if any(p in text for p in [
        "refund", "money back", "return my order",
        "cancel order", "cancellation"
    ]):
        return "refund_support", (
            "For refunds or cancellations, open your order details and check "
            "the available options. Eligibility and processing times depend on the service's policy."
        )

    # Payments and billing
    if any(p in text for p in [
        "payment", "billing", "charged", "transaction",
        "invoice", "payment failed"
    ]):
        return "payment_support", (
            "Check your payment history and transaction status. If you notice "
            "an incorrect charge, contact your payment provider or support team."
        )

    # Contact support
    if any(p in text for p in [
        "contact support", "customer service", "human agent",
        "talk to agent", "speak to someone"
    ]):
        return "contact_support", (
            "Please use the Help or Contact Us section of the service "
            "to reach its customer-support team."
        )

    # Original dataset commands
    if any(w in text for w in ["lower", "decrease", "reduce", "quieter"]):
        return "volumeDown", responses["volumeDown"]

    if any(w in text for w in ["increase", "raise", "louder", "turn up"]):
        return "volumeUp", responses["volumeUp"]

    if "stop" in text:
        return "stop", responses["stop"]

    if "wait" in text:
        return "wait", responses["wait"]

    if "still there" in text or "are you there" in text:
        return "stillThere", responses["stillThere"]

    # ML model fallback
    probabilities = model.predict_proba(
        vectorizer.transform([user_input])
    )[0]

    predicted_intent = model.classes_[probabilities.argmax()]

    if probabilities.max() < 0.25:
        return "unknown", responses["unknown"]

    return predicted_intent, responses.get(
        predicted_intent, responses["unknown"]
    )

# =====================================
# SIDEBAR
# =====================================
with st.sidebar:
    st.title("🤖 AI Assistant")
    st.write("Your virtual customer-support helper.")
    st.divider()

    st.subheader("✨ Supported topics")
    st.markdown(
        "- 🔐 Account and password help\n"
        "- 📦 Orders and delivery\n"
        "- 💰 Refunds and cancellations\n"
        "- 💳 Payments and billing\n"
        "- 👨‍💼 Contact support"
    )

    st.divider()
    st.caption("Prototype built with Streamlit and NLP.")

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# =====================================
# MAIN CHAT INTERFACE
# =====================================
st.title("🤖 AI Customer Support Chatbot")
st.caption("Smart assistance for your everyday customer-support questions.")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! 👋 Welcome to AI Customer Support. "
                "You can ask me about passwords, orders, refunds, or payments."
            ),
            "intent": "greeting"
        }
    ]

# Show chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

        if message["role"] == "assistant" and message.get("intent"):
            st.caption(
                "Topic: " + message["intent"].replace("_", " ").title()
            )

# Accept user input
user_input = st.chat_input("How can I help you today?")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    intent, response = chatbot(user_input)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "intent": intent
    })

    with st.chat_message("assistant"):
        st.write(response)
        st.caption("Topic: " + intent.replace("_", " ").title())
