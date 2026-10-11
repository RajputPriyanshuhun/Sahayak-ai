import streamlit as st
import google.generativeai as genai
from PIL import Image

# Page Configuration
st.set_page_config(
    page_title="SahayakAI - Multilingual Assistant", 
    page_icon="🤖", 
    layout="centered"
)

# Baseline Default Font Size 14px
if "font_size" not in st.session_state:
    st.session_state.font_size = 14

# Clean High-Contrast CSS Styling (Readable & Clean)
st.markdown(f"""
    <style>
    html, body, [class*="css"] {{
        font-size: {st.session_state.font_size}px !important;
        color: #1e293b;
    }}
    
    /* Light Clean Background */
    .stApp {{
        background-color: #f8fafc;
    }}

    /* Sidebar Clean Layout */
    section[data-testid="stSidebar"] {{
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }}

    /* Professional Button Styling */
    .stButton>button {{
        background-color: #4f46e5;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        width: 100%;
        transition: all 0.2s ease;
    }}
    .stButton>button:hover {{
        background-color: #4338ca;
    }}

    /* Accessible Card Container */
    .control-card {{
        background-color: #f1f5f9;
        border: 1px solid #cbd5e1;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 12px;
    }}
    </style>
""", unsafe_allow_html=True)

# Fully Localized UI Dictionary (100% Strings Dynamic)
ui_texts = {
    "English": {
        "sidebar_header": "⚙️ Controls & Settings",
        "lang_label": "🌐 Output & UI Language",
        "title": "🤖 SahayakAI: Multilingual Assistant",
        "caption": "Professional, Fast & Accessible AI Powered by Gemini",
        "font_label": "🔤 Accessibility: Font Size",
        "current_size": "Current Size",
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
        "font_label": "🔤 दृश्यता: फ़ॉन्ट आकार",
        "current_size": "वर्तमान फ़ॉन्ट आकार",
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
        "current_size": "ਮੌਜੂਦਾ ਆਕਾਰ",
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

# 1. Language Selection (First element in Sidebar)
selected_lang = st.sidebar.selectbox(
    "🌐 Select Language / भाषा चुनें", 
    ["English", "Hindi (हिंदी)", "Punjabi (ਪੰਜਾਬੀ)"]
)

# Fetch current UI text dictionary
current_ui = ui_texts.get(selected_lang, ui_texts["English"])

# 2. Localized Sidebar Header
st.sidebar.header(current_ui["sidebar_header"])

# 3. Localized Font Resizer Section
st.sidebar.markdown(f"**{current_ui['font_label']}**")
with st.sidebar.container():
    st.markdown('<div class="control-card">', unsafe_allow_html=True)
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

st.sidebar.write(f"{current_ui['current_size']}: **{st.session_state.font_size}px**")
st.sidebar.markdown("---")

# 4. Localized API Key Input
api_key = st.sidebar.text_input(current_ui['api_label'], type="password")

# Main Header
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
