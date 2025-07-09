import streamlit as st
import numpy as np
import tensorflow as tf
from PIL import Image
from SL_chat_theme_Olusola import StreamlitChatTheme, ThemeConfig # Custom theme for Streamlit chat

from config import APP_TITLE, APP_ICON
from prompts import build_prompt
from gemini_client import get_gemini_response, validate_api_key

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Validate API key
validate_api_key()

# Load CNN model
model = tf.keras.models.load_model("crop_disease_model.h5")

# Class names for disease prediction
class_names = [
    'Cashew anthracnose', 'Cashew gumosis', 'Cashew healthy', 'Cashew leaf miner', 'Cashew red rust',
    'Cassava bacterial blight', 'Cassava brown spot', 'Cassava green mite', 'Cassava healthy', 'Cassava mosaic',
    'Maize fall armyworm', 'Maize grasshoper', 'Maize healthy', 'Maize leaf beetle', 'Maize leaf blight',
    'Maize leaf spot', 'Maize streak virus',
    'Tomato healthy', 'Tomato leaf blight', 'Tomato leaf curl',
    'Tomato septoria leaf spot', 'Tomato verticulium wilt'
]

# Initialize session state
if "name" not in st.session_state:
    st.session_state.name = ""
if "region" not in st.session_state:
    st.session_state.region = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Preprocess image for CNN
def preprocess_image(image):
    image = image.resize((128, 128))
    image = np.array(image) / 255.0
    return np.expand_dims(image, axis=0)

# Build disease explanation prompt for Gemini
def build_disease_prompt(disease_label, user_name, user_region):
    prompt = f"""
You are FarmAssist, a trusted agricultural extension officer helping Nigerian farmers like {user_name} in {user_region}.

A farmer uploaded a crop leaf image. The disease was identified as **{disease_label}**.

Please explain:
- The common symptoms of this disease
- The likely causes
- Practical treatment or solution

Use markdown format. Stay warm, helpful, and specific to Nigerian farming conditions.
"""
    return prompt.strip()

# Display a chat-style message
def display_chat_message(user_msg, bot_reply, user_name):
    st.markdown(
        f"""
        <div class="user-message">
            <div class="message-header">👤 {user_name}</div>
            <div class="message-content">{user_msg}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="bot-message">
            <div class="message-header">🌿 FarmAssist</div>
            <div class="message-content">{bot_reply}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Handle text-based prompt
def handle_prompt(prompt):
    if not prompt.strip():
        return False
    with st.spinner("FarmAssist is thinking..."):
        try:
            full_prompt = build_prompt(
                st.session_state.name,
                st.session_state.region,
                prompt,
                st.session_state.chat_history
            )
            reply = get_gemini_response(full_prompt)
            st.session_state.chat_history.append((prompt, reply))
            return True
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")
            return False

# Main app
def main():
    # Custom chat theme
    theme = StreamlitChatTheme()
    theme.apply_theme()

    st.title("🌿 FarmAssist 🌿")
    st.markdown("### Your Go-To Assistant for Farm Matters in Nigeria")

    if not st.session_state.name:
        st.markdown("---")
        with st.form("user_info", clear_on_submit=True):
            st.subheader("Welcome! Let's get FARMiliar! 😜")
            st.markdown("Please provide your information to get personalized farming advice:")
            name = st.text_input("Your First Name *", placeholder="Enter your first name")
            region = st.text_input("Your Region/State in Nigeria", placeholder="e.g., Lagos, Kano, Ogun (optional)")
            submitted = st.form_submit_button("Start Chatting", type="primary")
            if submitted:
                if name.strip():
                    st.session_state.name = name.strip().title()
                    st.session_state.region = region.strip().title() if region.strip() else "Nigeria"
                    st.success(f"Welcome, {st.session_state.name}! Ready to help with your farming questions.")
                    st.rerun()
                else:
                    st.error("Please enter your name to continue.")
    else:
        st.markdown("---")

        # Chat history display
        if st.session_state.chat_history:
            st.subheader("Let's get FARMiliar! 😜")
            for user_msg, bot_reply in st.session_state.chat_history:
                display_chat_message(user_msg, bot_reply, st.session_state.name)
            st.markdown("---")

        # Chat input form
        if not st.session_state.chat_history:
            st.subheader(f"Hi {st.session_state.name}! How may I assist you today?")
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_area(
                "What would you like to know about farming?",
                placeholder="Type your farming question here...",
                height=100,
                label_visibility="collapsed"
            )
            submitted = st.form_submit_button("Send Message", type="primary")
            if submitted and user_input.strip():
                if handle_prompt(user_input):
                    st.rerun()

        # Image upload for disease detection
        st.markdown("---")
        st.subheader("🖼️ Upload a Crop Leaf Image for Disease Detection")
        uploaded_file = st.file_uploader("Choose a leaf image...", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            image = Image.open(uploaded_file).convert("RGB")
            st.image(image, caption="Uploaded Image", width=200)

            with st.spinner("Analyzing image..."):
                processed = preprocess_image(image)
                prediction = model.predict(processed)
                class_index = np.argmax(prediction)
                confidence = prediction[0][class_index]
                label = class_names[class_index]

                st.markdown(f"### 🧪 Prediction: `{label}`")
                st.markdown(f"**Confidence:** {confidence:.2%}")

                disease_prompt = build_disease_prompt(label, st.session_state.name, st.session_state.region)
                response = get_gemini_response(disease_prompt)

                st.session_state.chat_history.append((f"(Uploaded leaf image — predicted: {label})", response))
                st.markdown(response)

        # Start new session
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Start a new session", help="Clear chat and start fresh"):
                for key in ["name", "region", "chat_history"]:
                    st.session_state.pop(key, None)
                st.rerun()

        # Quick suggestions for new users
        if not st.session_state.chat_history:
            st.markdown("---")
            st.subheader("Frequently Asked Questions")
            st.markdown("Here are some common questions to get you started:")
            col1, col2 = st.columns(2)
            suggestions = [
                ("🌱 Best crops for my region", "What are the best crops to grow in my region considering the climate and soil?"),
                ("💧 Irrigation methods", "What are the most effective irrigation methods for small-scale farming in Nigeria?"),
                ("🐛 Pest control strategies", "How can I protect my crops from common pests and diseases?"),
                ("💰 Crop market information", "What are the current market trends and prices for agricultural products?")
            ]
            for i, (btn_text, q) in enumerate(suggestions):
                col = col1 if i % 2 == 0 else col2
                with col:
                    if st.button(btn_text, key=f"suggestion_{i}"):
                        if handle_prompt(q):
                            st.rerun()

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; padding: 20px; color: #666;'>"
        "<a href='https://github.com/Sholz22/FarmAssist..git' target='_blank'>View Source Code on GitHub (Sholz22)</a>"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    load_css()
    main()
