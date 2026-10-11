import streamlit as st
import google.generativeai as genai
from PIL import Image

# Page Configuration
st.set_page_config(
    page_title="SahayakAI - Multilingual Problem Solver", 
    page_icon="🤖", 
    layout="centered"
)

# Initialize Session State for Font Size to 14px default
if "font_size" not in st.session_state:
    st.session_state.font_size = 14

# Stunning 3D Neon Glassmorphism & Smooth Animation CSS
st.markdown(f"""
    <style>
    html, body, [class*="css"] {{
        font-size: {st.session_state.font_size}px;
    }}
    
    /* Dark Gradient Background */
    .stApp {{
        background: linear-gradient(135deg, #090d16 0%, #171f33 50%, #090d16 100%);
        color: #f1f5f9;
    }}

    /* Sidebar Styling with Glow */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #131b2e 0%, #0b101b 100%);
        border-right: 1px solid rgba(99, 102, 241, 0.2);
    }}

    /* 3D Animated Gradient Buttons */
    .stButton>button {{
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 700;
        padding: 0.6rem 1.2rem;
        width: 100%;
        box-shadow: 0 8px 20px -4px rgba(99, 102, 241, 0.5);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}
    .stButton>button:hover {{
        transform: translateY(-4px) scale(1.03);
        box-shadow: 0 14px 28px -4px rgba(168, 85, 247, 0.7);
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 100%);
    }}
    .stButton>button:active {{
        transform: translateY(1px);
    }}

    /* Glassmorphism Cards for Controls */
    .glass-card {{
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 16px;
        border-radius: 16px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 15px;
    }}

    /* Inputs Styling with Glow on Focus */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {{
        background-color: rgba(255, 255, 255, 0.06) !important;
        color: #f8fafc !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        transition: all 0.3s ease;
    }}

    /* Sleek Tab Navigation Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        background-color: rgba(255, 255, 255, 0.03);
        padding: 8px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: transparent;
        border-radius: 10px;
        color: #94a3b8;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.5);
    }}
    </style>
""", unsafe_allow_html=True)

# Fully Localized UI Dictionary
ui_texts = {
    "English": {
        "sidebar_header": "⚙️ Controls & Settings",
        "lang_label": "🌐 Output & UI Language",
        "title": "🤖 SahayakAI: Multilingual Assistant",
        "caption": "Professional, Fast & Accessible AI Powered by Gemini",
        "font_label": "🔤 Font Size (Accessibility)",
        "api_label": "🔑 Enter Gemini API Key",
        "api_warn": "⚠️ Please enter your Gemini API Key in the sidebar to begin.",
        "api_tip": "💡 Get a free key instantly from Google AI Studio.",
        "tab1": "💬 Text Solver",
        "tab2": "🎙️ Voice Helper",
        "tab3": "🖼️ Image Analyzer",
        "t1_sub": "Describe your problem or idea:",
        "t1_ph": "Type your question or issue here...",
        "t1_btn": "Generate Solution 🚀",
        "success": "Solution Ready!"
    },
    "Hindi (हिंदी)": {
        "sidebar_header": "⚙️ नियंत्रण और सेटिंग्स",
        "lang_label": "🌐 आउटपुट और यूआई भाषा",
        "title": "🤖 सहायक-AI: बहुभाषी सहायक",
        "caption": "जेमिनी द्वारा संचालित पेशेवर, तेज़ और सुलभ एआई",
        "font_label": "🔤 फ़ॉन्ट आकार (अक्षर बड़ा/छोटा करें)",
        "api_label": "🔑 जेमिनी एपीआई कुंजी दर्ज करें",
        "api_warn": "⚠️ आगे बढ़ने के लिए कृपया साइडबार में अपनी जेमिनी एपीआई कुंजी दर्ज करें।",
        "api_tip": "💡 Google AI Studio से तुरंत अपनी मुफ्त एपीआई कुंजी प्राप्त करें।",
        "tab1": "💬 टेक्स्ट समाधान",
        "tab2": "🎙️ आवाज़ सहायक",
        "tab3": "🖼️ चित्र विश्लेषक",
        "t1_sub": "अपनी समस्या या विचार यहाँ लिखें:",
        "t1_ph": "अपना प्रश्न या स्थानीय समस्या यहाँ टाइप करें...",
        "t1_btn": "समाधान प्राप्त करें 🚀",
        "success": "समाधान तैयार है!"
    },
    "Punjabi (ਪੰਜਾਬੀ)": {
        "sidebar_header": "⚙️ ਕੰਟਰੋਲ ਅਤੇ ਸੈਟਿੰਗਾਂ",
        "lang_label": "🌐 ਆਉਟਪੁੱਟ ਅਤੇ ਯੂ.ਆਈ ਭਾਸ਼ਾ",
        "title": "🤖 ਸਹਾਇਕ-AI: ਬਹੁਭਾਸ਼ੀ ਸਹਾਇਕ",
        "caption": "ਜੇਮਿਨੀ ਦੁਆਰਾ ਸੰਚਾਲਿਤ ਪੇਸ਼ੇਵਰ ਅਤੇ ਸਰਲ ਏ.ਆਈ",
        "font_label": "🔤 ਫੋਂਟ ਆਕਾਰ ਕੰਟਰੋਲ",
        "api_label": "🔑 API ਕੁੰਜੀ ਦਰਜ ਕਰੋ",
        "api_warn": "⚠️ ਸ਼ੁਰੂ ਕਰਨ ਲਈ ਆਪਣੀ API ਕੁੰਜੀ ਦਰਜ ਕਰੋ।",
        "api_tip": "💡 Google AI Studio ਤੋਂ ਮੁਫ਼ਤ ਵਿੱਚ ਪ੍ਰਾਪਤ ਕਰੋ।",
        "tab1": "💬 ਟੈਕਸਟ ਹੱਲ",
        "tab2": "🎙️ ਆਵਾਜ਼ ਸਹਾਇਕ",
        "tab3": "🖼️ ਤਸਵੀਰ ਵਿਸ਼ਲੇਸ਼ਕ",
        "t1_sub": "ਆਪਣੀ ਸਮੱਸਿਆ ਜਾਂ ਵਿਚਾਰ ਇੱਥੇ ਲਿਖੋ:",
        "t1_ph": "ਆਪਣਾ ਸਵਾਲ ਇੱਥੇ ਟਾਈਪ ਕਰੋ...",
        "t1_btn": "ਹੱਲ ਪ੍ਰਾਪਤ ਕਰੋ 🚀",
        "success": "ਹੱਲ ਤਿਆਰ ਹੈ!"
    }
}

# Sidebar Language Selection First
selected_lang = st.sidebar.selectbox(
    "🌐 Output & UI Language", 
    ["English", "Hindi (हिंदी)", "Punjabi (ਪੰਜਾਬੀ)"]
)

# Fetch corresponding UI strings dynamically
current_ui = ui_texts.get(selected_lang, ui_texts["English"])

# Sidebar Header Localized
st.sidebar.header(current_ui["sidebar_header"])

# 3D Glassmorphism Font Resizer Section in Sidebar
st.sidebar.markdown(f"**{current_ui['font_label']}**")
with st.sidebar.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        if st.button("➖ A-"):
            if st.session_state.font_size > 10:
                st.session_state.font_size -= 2
                st.rerun()
    with f_col2:
        if st.button("🔄 14px"):
            st.session_state.font_size = 14
            st.rerun()
    with f_col3:
        if st.button("➕ A+"):
            if st.session_state.font_size < 24:
                st.session_state.font_size += 2
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.sidebar.write(f"Current Size: **{st.session_state.font_size}px**")
st.sidebar.markdown("---")

api_key = st.sidebar.text_input(current_ui['api_label'], type="password")

# Main App Header Localized
st.title(current_ui["title"])
st.caption(current_ui["caption"])

if not api_key:
    st.warning(current_ui["api_warn"])
    st.info(current_ui["api_tip"])
else:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-3.8-flash")

        # Localized Tabs
        tabs = st.tabs([current_ui["tab1"], current_ui["tab2"], current_ui["tab3"]])

        # Tab 1: Text Solver
        with tabs[0]:
            st.subheader(current_ui["t1_sub"])
            user_prompt = st.text_area("", placeholder=current_ui["t1_ph"], height=100)
            
            if st.button(current_ui["t1_btn"], type="primary"):
                if user_prompt.strip():
                    with st.spinner("Generating..."):
                        try:
                            prompt = f"{user_prompt}\n\nProvide a natural, professional response strictly in {selected_lang} language."
                            response = model.generate_content(prompt)
                            st.success(current_ui["success"])
                            st.markdown("### Result / परिणाम:")
                            st.write(response.text)
                        except Exception as e:
                            st.error(f"Error: {e}")
                else:
                    st.warning("Please type something first!")

        # Tab 2: Voice Helper
        with tabs[1]:
            st.subheader("🎙️ Voice & Audio Assistant")
            audio_file = st.file_uploader("Upload audio recording (WAV, MP3)", type=["wav", "mp3", "m4a"])
            if audio_file is not None:
                st.audio(audio_file)
                if st.button("Analyze Audio 🚀", type="primary"):
                    with st.spinner("Processing..."):
                        try:
                            audio_bytes = audio_file.read()
                            audio_data = {"mime_type": audio_file.type, "data": audio_bytes}
                            response = model.generate_content([f"Analyze this audio and respond naturally in {selected_lang}", audio_data])
                            st.success(current_ui["success"])
                            st.write(response.text)
                        except Exception as e:
                            st.error(f"Error: {e}")

        # Tab 3: Image Analyzer
        with tabs[2]:
            st.subheader("🖼️ Image & Document Analyzer")
            uploaded_file = st.file_uploader("Upload image...", type=["jpg", "jpeg", "png"])
            img_prompt = st.text_input("What should AI do with this image?", "Explain this image and give solutions.")

            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                st.image(image, use_column_width=True)
                if st.button("Analyze Image 🔍", type="primary"):
                    with st.spinner("Analyzing..."):
                        try:
                            response = model.generate_content([f"{img_prompt}. Respond naturally in {selected_lang}.", image])
                            st.success(current_ui["success"])
                            st.write(response.text)
                        except Exception as e:
                            st.error(f"Error: {e}")

    except Exception as err:
        st.error(f"Config Error: {err}")
