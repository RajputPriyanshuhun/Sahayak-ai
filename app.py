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

# Clean & Professional CSS with 14px default
st.markdown(f"""
    <style>
    html, body, [class*="css"] {{
        font-size: {st.session_state.font_size}px;
    }}
    .stButton>button {{
        border-radius: 6px;
        font-weight: 600;
        width: 100%;
    }}
    </style>
""", unsafe_allow_html=True)

# Clean Localized UI Dictionary
ui_texts = {
    "English": {
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
        "title": "🤖 सहायक-AI: बहुभाषी सहायक",
        "caption": "जेमिनी द्वारा संचालित पेशेवर, तेज़ और सुलभ एआई",
        "font_label": "🔤 फ़ॉन्ट आकार (फ़ॉन्ट साइज़)",
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
        "title": "🤖 ਸਹਾਇਕ-AI: ਬਹੁਭਾਸ਼ੀ ਸਹਾਇਕ",
        "caption": "ਜੇਮਿਨੀ ਦੁਆਰਾ ਸੰਚਾਲਿਤ ਪੇਸ਼ੇਵਰ ਅਤੇ ਸਰਲ ਏ.ਆਈ",
        "font_label": "🔤 ਫੋਂਟ ਆਕਾਰ (Font Size)",
        "api_label": "🔑 API ਕੁੰਜੀ ਦਰਜ ਕਰੋ",
        "api_warn": "⚠️ ਸ਼ुरू करने के लिए अपनी API कुंजी दर्ज करो।",
        "api_tip": "💡 Google AI Studio से मुफ्त की प्राप्त करें।",
        "tab1": "💬 ਟੈਕਸਟ ਹੱਲ",
        "tab2": "🎙️ ਆਵਾਜ਼ ਸਹਾਇਕ",
        "tab3": "🖼️ ਤਸਵੀਰ ਵਿਸ਼ਲੇਸ਼ਕ",
        "t1_sub": "ਆਪਣੀ ਸਮੱਸਿਆ ਜਾਂ ਵਿਚਾਰ ਇੱਥੇ ਲਿਖੋ:",
        "t1_ph": "ਆਪਣਾ ਸਵਾਲ ਇੱਥੇ ਟਾਈਪ ਕਰੋ...",
        "t1_btn": "ਹੱਲ ਪ੍ਰਾਪਤ ਕਰੋ 🚀",
        "success": "ਹੱਲ ਤਿਆਰ ਹੈ!"
    }
}

# Sidebar Controls & Settings
st.sidebar.header("⚙️ Controls & Settings")

selected_lang = st.sidebar.selectbox(
    "🌐 Output & UI Language", 
    ["English", "Hindi (हिंदी)", "Punjabi (ਪੰਜਾਬੀ)"]
)

current_ui = ui_texts.get(selected_lang, ui_texts["English"])

# Font Resizer Section in Sidebar
st.sidebar.markdown(f"**{current_ui['font_label']}**")
f_col1, f_col2, f_col3 = st.sidebar.columns(3)
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

st.sidebar.write(f"Current Size: **{st.session_state.font_size}px**")
st.sidebar.markdown("---")

api_key = st.sidebar.text_input(current_ui['api_label'], type="password")

# Main App Header
st.title(current_ui["title"])
st.caption(current_ui["caption"])

if not api_key:
    st.warning(current_ui["api_warn"])
    st.info(current_ui["api_tip"])
else:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-3.8-flash")

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
