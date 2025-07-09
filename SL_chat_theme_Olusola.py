import streamlit as st
from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class ThemeConfig:
    """Configuration class for theme customization."""
    primary_color: str = "#4CAF50"
    secondary_color: str = "#45a049"
    accent_color: str = "#2E7D32"
    background_light: str = "#f8f9fa"
    background_dark: str = "#e9ecef"
    text_color: str = "#333"
    border_radius: str = "15px"
    button_radius: str = "25px"
    shadow_color: str = "rgba(76, 175, 80, 0.3)"

class StreamlitChatTheme:
    """A reusable CSS theme class for Streamlit chat applications."""
    
    def __init__(self, config: Optional[ThemeConfig] = None):
        """Initialize the theme with custom configuration."""
        self.config = config or ThemeConfig()
    
    def apply_theme(self, hide_streamlit_branding: bool = True) -> None:
        """Apply the complete theme to the Streamlit app."""
        css = self._build_css(hide_streamlit_branding)
        st.markdown(css, unsafe_allow_html=True)
    
    def _build_css(self, hide_branding: bool) -> str:
        """Build the complete CSS string."""
        css_parts = []
        
        if hide_branding:
            css_parts.append(self._get_branding_css())
        
        css_parts.extend([
            self._get_main_container_css(),
            self._get_chat_message_css(),
            self._get_form_css(),
            self._get_button_css(),
            self._get_title_css(),
            self._get_responsive_css()
        ])
        
        return f"<style>{''.join(css_parts)}</style>"
    
    def _get_branding_css(self) -> str:
        """CSS to hide Streamlit branding."""
        return """
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        """
    
    def _get_main_container_css(self) -> str:
        """CSS for main container styling."""
        return """
        /* Main container styling */
        .main > div {
            padding-top: 1rem;
        }
        """
    
    def _get_chat_message_css(self) -> str:
        """CSS for chat message styling."""
        return f"""
        /* Chat message styling */
        .user-message {{
            background: linear-gradient(135deg, {self.config.primary_color}, {self.config.secondary_color});
            color: white;
            padding: 15px 20px;
            border-radius: 20px 20px 5px 20px;
            margin: 10px 0 10px 20%;
            box-shadow: 0 2px 10px {self.config.shadow_color};
        }}
        
        .bot-message {{
            background: linear-gradient(135deg, {self.config.background_light}, {self.config.background_dark});
            color: {self.config.text_color};
            padding: 15px 20px;
            border-radius: 20px 20px 20px 5px;
            margin: 10px 20% 10px 0;
            border-left: 4px solid {self.config.primary_color};
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }}
        
        .message-header {{
            font-weight: bold;
            font-size: 0.9em;
            margin-bottom: 8px;
            opacity: 0.9;
        }}
        
        .message-content {{
            line-height: 1.5;
            word-wrap: break-word;
        }}
        """
    
    def _get_form_css(self) -> str:
        """CSS for form styling."""
        return f"""
        /* Form styling */
        .stTextArea textarea {{
            border: 2px solid {self.config.primary_color};
            border-radius: {self.config.border_radius};
            padding: 15px;
            font-size: 16px;
            transition: all 0.3s ease;
        }}
        
        .stTextArea textarea:focus {{
            border-color: {self.config.secondary_color};
            box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
        }}
        
        .stTextInput input {{
            border: 2px solid {self.config.primary_color};
            border-radius: 10px;
            padding: 12px 15px;
            font-size: 16px;
            transition: all 0.3s ease;
        }}
        
        .stTextInput input:focus {{
            border-color: {self.config.secondary_color};
            box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
        }}
        """
    
    def _get_button_css(self) -> str:
        """CSS for button styling."""
        return f"""
        /* Button styling */
        .stButton button {{
            border-radius: {self.config.button_radius};
            border: none;
            font-weight: 600;
            padding: 12px 24px;
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        
        .stButton button[kind="primary"] {{
            background: linear-gradient(135deg, {self.config.primary_color}, {self.config.secondary_color});
            color: white;
            box-shadow: 0 4px 15px {self.config.shadow_color};
        }}
        
        .stButton button[kind="primary"]:hover {{
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
        }}
        
        .stButton button[kind="secondary"] {{
            background: linear-gradient(135deg, {self.config.background_light}, {self.config.background_dark});
            color: {self.config.primary_color};
            border: 2px solid {self.config.primary_color};
            width: 100%;
            text-align: left;
            margin: 5px 0;
        }}
        
        .stButton button[kind="secondary"]:hover {{
            background: linear-gradient(135deg, {self.config.primary_color}, {self.config.secondary_color});
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 4px 15px {self.config.shadow_color};
        }}
        
        /* Form submit button */
        .stForm button {{
            background: linear-gradient(135deg, {self.config.primary_color}, {self.config.secondary_color});
            color: white;
            border: none;
            border-radius: {self.config.button_radius};
            padding: 12px 30px;
            font-weight: 600;
            font-size: 16px;
            width: 100%;
            transition: all 0.3s ease;
        }}
        
        .stForm button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
        }}
        """
    
    def _get_title_css(self) -> str:
        """CSS for title styling."""
        return f"""
        /* Title styling */
        h1 {{
            color: {self.config.accent_color};
            text-align: center;
            margin-bottom: 0.5rem;
        }}
        
        h3 {{
            color: {self.config.primary_color};
            text-align: center;
            margin-bottom: 2rem;
            font-weight: 400;
        }}
        """
    
    def _get_responsive_css(self) -> str:
        """CSS for responsive design."""
        return """
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
        """
    
    def display_chat_message(self, user_msg: str, bot_reply: str, user_name: str, bot_name: str = "Assistant") -> None:
        """Display a chat message pair with the theme styling."""
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
                <div class="message-header">🤖 {bot_name}</div>
                <div class="message-content">{bot_reply}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Predefined theme configurations
class ThemePresets:
    """Predefined theme configurations for different use cases."""
    
    @staticmethod
    def green_farm_theme() -> ThemeConfig:
        """Original green farm theme."""
        return ThemeConfig(
            primary_color="#4CAF50",
            secondary_color="#45a049",
            accent_color="#2E7D32"
        )
    
    @staticmethod
    def blue_tech_theme() -> ThemeConfig:
        """Blue tech theme."""
        return ThemeConfig(
            primary_color="#2196F3",
            secondary_color="#1976D2",
            accent_color="#0D47A1",
            shadow_color="rgba(33, 150, 243, 0.3)"
        )
    
    @staticmethod
    def purple_creative_theme() -> ThemeConfig:
        """Purple creative theme."""
        return ThemeConfig(
            primary_color="#9C27B0",
            secondary_color="#7B1FA2",
            accent_color="#4A148C",
            shadow_color="rgba(156, 39, 176, 0.3)"
        )
    
    @staticmethod
    def orange_energy_theme() -> ThemeConfig:
        """Orange energy theme."""
        return ThemeConfig(
            primary_color="#FF9800",
            secondary_color="#F57C00",
            accent_color="#E65100",
            shadow_color="rgba(255, 152, 0, 0.3)"
        )

# Usage example
def example_usage():
    """Example of how to use the StreamlitChatTheme class."""
    
    # Option 1: Use default green theme
    theme = StreamlitChatTheme()
    theme.apply_theme()
    
    # Option 2: Use a preset theme
    blue_theme = StreamlitChatTheme(ThemePresets.blue_tech_theme())
    blue_theme.apply_theme()
    
    # Option 3: Create custom theme
    custom_config = ThemeConfig(
        primary_color="#E91E63",
        secondary_color="#C2185B",
        accent_color="#880E4F",
        border_radius="10px",
        button_radius="15px"
    )
    custom_theme = StreamlitChatTheme(custom_config)
    custom_theme.apply_theme()
    
    # Display chat messages
    theme.display_chat_message(
        "Hello, how can I help you today?",
        "Hi! I'm here to assist you with any questions you might have.",
        "John Doe"
    )

if __name__ == "__main__":
    example_usage()