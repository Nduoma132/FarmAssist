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

def handle_prompt(prompt):
    """Handle user prompt and get AI response."""
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

def display_chat_message(user_msg, bot_reply, user_name):
    """Display a chat message pair."""
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
    
    # Bot reply
    st.markdown(
        f"""
        <div class="bot-message">
            <div class="message-header">🌿 FarmAssist</div>
            <div class="message-content">{bot_reply}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def main():
    """Main application logic."""
    
    # Header
    st.title("🌿 FarmAssist 🌿")
    st.markdown("### Your Go-To Assistant for Farm Matters in Nigeria")
    
    # User information form (show only if name not set)
    if not st.session_state.name:
        st.markdown("---")
        with st.form("user_info", clear_on_submit=True):
            st.subheader("Welcome! Let's get FARMiliar! 😜")
            st.markdown("Please provide your information to get personalized farming advice:")
            
            name = st.text_input("Your First Name *", placeholder="Enter your first name")
            region = st.text_input(
                "Your Region/State in Nigeria", 
                placeholder="e.g., Lagos, Kano, Ogun (optional)"
            )
            
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
        # Main chat interface
        st.markdown("---")
        
        # Display chat history
        if st.session_state.chat_history:
            st.subheader("Let's get FARMiliar! 😜")
            
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
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Start a new session", help="Clear chat and start fresh"):
                for key in ["name", "region", "chat_history"]:
                    st.session_state.pop(key, None)
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
        "<a href='https://github.com/Sholz22/FarmAssist..git' target='_blank'>View Source Code on GitHub (Sholz22)</a>"
        "</div>",
        unsafe_allow_html=True
    )

# CSS Styling
def load_css():
    """Load custom CSS styling."""
    st.markdown("""
    <style>
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Main container styling */
        .main > div {
            padding-top: 2rem;
        }
        
        /* Chat message styling */
        .user-message {
            background: linear-gradient(135deg, #4CAF50, #45a049);
            color: white;
            padding: 15px 20px;
            border-radius: 20px 20px 5px 20px;
            margin: 10px 0 10px 20%;
            box-shadow: 0 2px 10px rgba(76, 175, 80, 0.3);
        }
        
        .bot-message {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            color: #333;
            padding: 15px 20px;
            border-radius: 20px 20px 20px 5px;
            margin: 10px 20% 10px 0;
            border-left: 4px solid #4CAF50;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        
        .message-header {
            font-weight: bold;
            font-size: 0.9em;
            margin-bottom: 8px;
            opacity: 0.9;
        }
        
        .message-content {
            line-height: 1.5;
            word-wrap: break-word;
        }
        
        /* Form styling */
        .stTextArea textarea {
            border: 2px solid #4CAF50;
            border-radius: 15px;
            padding: 15px;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        .stTextArea textarea:focus {
            border-color: #45a049;
            box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
        }
        
        .stTextInput input {
            border: 2px solid #4CAF50;
            border-radius: 10px;
            padding: 12px 15px;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        .stTextInput input:focus {
            border-color: #45a049;
            box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
        }
        
        /* Button styling */
        .stButton button {
            border-radius: 25px;
            border: none;
            font-weight: 600;
            padding: 12px 24px;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .stButton button[kind="primary"] {
            background: linear-gradient(135deg, #4CAF50, #45a049);
            color: white;
            box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
        }
        
        .stButton button[kind="primary"]:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
        }
        
        .stButton button[kind="secondary"] {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            color: #4CAF50;
            border: 2px solid #4CAF50;
            width: 100%;
            text-align: left;
            margin: 5px 0;
        }
        
        .stButton button[kind="secondary"]:hover {
            background: linear-gradient(135deg, #4CAF50, #45a049);
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
        }
        
        /* Form submit button */
        .stForm button {
            background: linear-gradient(135deg, #4CAF50, #45a049);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 12px 30px;
            font-weight: 600;
            font-size: 16px;
            width: 100%;
            transition: all 0.3s ease;
        }
        
        .stForm button:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
        }
        
        /* Title styling */
        h1 {
            color: #2E7D32;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        
        h3 {
            color: #4CAF50;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: 400;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .user-message, .bot-message {
                margin-left: 5%;
                margin-right: 5%;
            }
            
            .stButton button {
                font-size: 14px;
                padding: 10px 20px;
            }
        }
    </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    load_css()
    main()