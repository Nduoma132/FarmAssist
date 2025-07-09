import streamlit as st
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

# Validate API key on startup
validate_api_key()

# Initialize session state
if "name" not in st.session_state:
    st.session_state.name = ""
if "region" not in st.session_state:
    st.session_state.region = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# Handle user prompt and get AI response.
def handle_prompt(prompt):
    if not prompt.strip():
        return False
    
    with st.spinner("FarmAssist is thinking..."):
        try:
            # Build prompt with context
            full_prompt = build_prompt(
                st.session_state.name,
                st.session_state.region,
                prompt,
                st.session_state.chat_history
            )
            
            # Get AI response
            reply = get_gemini_response(full_prompt)
            
            # Add to chat history
            st.session_state.chat_history.append((prompt, reply))
            return True
            
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")
            return False


# Display a chat message pair.
def display_chat_message(user_msg, bot_reply, user_name):
    # User message
    st.markdown(
        f"""
        <div class="user-message">
            <div class="message-header">👤 {user_name}</div>
            <div class="message-content">{user_msg}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Bot response
    st.markdown(
        f"""
        <div class="bot-message">
            <div class="message-header">🌿 FarmAssist</div>
            <div class="message-content">{bot_reply}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    

# Main application logic.
def main():
    # Header
    st.title("🌿 FarmAssist 🌿")
    st.markdown("### Your Go-To Assistant for Farm Matters in Nigeria")
    
    # User information form (show only if name not set)
    if not st.session_state.name:
        st.markdown("---")
        with st.form("user_info", clear_on_submit=True):
            st.subheader("Welcome! Let's get FARMiliar! 😜")
            st.markdown("Please provide your information to get personalized farming advice:")
            
            name = st.text_input("Your Username *", placeholder="Enter your username")
            region = st.text_input("Your Region/State in Nigeria",  placeholder="e.g., Lagos, Kano, Ogun (optional)")
            submitted = st.form_submit_button("Start Chatting", type="primary")
            
            if submitted:
                if name.strip():
                    st.session_state.name = name.strip().title()
                    st.session_state.region = region.strip().title() if region.strip() else "Nigeria"
                    st.success(f"Welcome, {st.session_state.name}! I'm ready to serve you now.")
                    st.rerun()
                else:
                    st.error("Please enter your username to continue.")
    
    else:
        # Main chat interface
        st.markdown("---")
        
        # Display chat history
        if st.session_state.chat_history:
            st.subheader(f"Welcome back {st.session_state.name}! 😜")
            
            for user_msg, bot_reply in st.session_state.chat_history:
                display_chat_message(user_msg, bot_reply, st.session_state.name)
            
            st.markdown("---")
        
        # Chat input section
        if not st.session_state.chat_history:
            st.subheader(f"Hi {st.session_state.name}! How may I assist you today?")
        
        # Chat form
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_area(
                "What would you like to know about farming?",
                placeholder="Type your farming question here... (e.g., What crops grow best in the rainy season?)",
                height=100,
                label_visibility="collapsed"
            )
            
            submitted = st.form_submit_button("Send Message", type="primary")
            
            if submitted and user_input.strip():
                if handle_prompt(user_input):
                    st.rerun()
        
        # New session button
        col1, col2 = st.columns([1, 1])
        with col2:
            if st.button("Refresh page", help="Clear chat and start fresh"):
                for key in ["name", "region", "chat_history"]:
                    st.session_state.pop(key, None)
                st.rerun()

        # New session button (keep name and region)
        with col1:
            if st.button("New Session", help="Start a fresh chat but keep your name and region"):
                st.session_state["chat_history"] = []
                st.rerun()

        
        # Quick suggestions (only for new users)
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
            
            for i, (button_text, question) in enumerate(suggestions):
                col = col1 if i % 2 == 0 else col2
                with col:
                    if st.button(button_text, key=f"suggestion_{i}"):
                        if handle_prompt(question):
                            st.rerun()
    
    # Footer with GitHub link - MOVED TO BOTTOM OF MAIN FUNCTION
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; padding: 20px; color: #666;'>"
        "<a href='https://github.com/Sholz22/FarmAssist..git' target='_blank'>View Source Code on GitHub.</a>"
        "</div>",
        unsafe_allow_html=True
    )


# Run the main function
if __name__ == "__main__":
    with open("styles.css") as styles:
        st.markdown(
            f"<style>{styles.read()}</style>", 
            unsafe_allow_html=True
            )
    main()