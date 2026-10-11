import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(
    page_title="SahayakAI - Multilingual Assistant", 
    page_icon="🤖", 
    layout="centered"
)

if "font_size" not in st.session_state:
    st.session_state.font_size = 14

st.markdown(f"""
    <style>
    html, body, [class*="css"] {{
        font-size: {st.session_state.font_size}px !important;
    }}
    
    .stApp {{
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        color: #ffffff !important;
    }}

    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }}
    section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] span {{
        color: #ffffff !important;
        font-weight: 500;
    }}

    /* Neon Glow for Warning & Info boxes */
    .stAlert {{
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(99, 102, 241, 0.5) !important;
        box-shadow: 0 0 15px rgba(99, 102, 241, 0.2);
        border-radius: 12px;
    }}

    .stButton>button {{
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 700;
        padding: 0.6rem 1rem;
        width: 100%;
        box-shadow: 0 8px 20px -4px rgba(99, 102, 241, 0.5);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .stButton>button:hover {{
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 12px 24px -4px rgba(168, 85, 247, 0.7);
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 100%);
    }}
    </style>
""", unsafe_allow_html=True)

ui_texts = {
    "English": {
        "sidebar_header": "⚙️ Controls & Settings",
        "title": "🤖 SahayakAI: Multilingual Assistant",
        "caption": "Professional, Fast & Accessible AI Powered by Gemini",
        "font_label": "🔤 Accessibility: Font Size",
        "current_size": "Current Size",
        "api_label": "🔑 Enter Gemini API Key",
        "api_connected": "API Connected 🟢",
        "api_required": "API Key Required 🔴",
        "api_warn": "⚠️ Please enter your Gemini API Key in the sidebar to begin.",
        "api_tip": "💡 Get a free key instantly from Google AI Studio.",
        "tab1": "💬 Text Solver",
        "tab2": "🎙️ Voice Helper",
        "tab3": "🖼️ Image Analyzer",
        "t1_sub": "Describe your problem or idea:",
        "t1_ph": "Type your question or issue here...",
        "t1_btn": "Generate Solution 🚀",
        "success": "Solution Ready!",
        "chips_title": "💡 Quick Suggestions:",
        "chips": ["🌾 Crop Disease Solution", "📜 Local Govt Schemes Info", "⚡ Energy Saving Tips"]
    },
    "Hindi (हिंदी)": {
        "sidebar_header": "⚙️ नियंत्रण और सेटिंग्स",
        "title": "🤖 सहायक-AI: बहुभाषी सहायक",
        "caption": "जेमिनी द्वारा संचालित पेशेवर, तेज़ और सुलभ एआई",
        "font_label": "🔤 दृश्यता: फ़ॉन्ट आकार",
        "current_size": "वर्तमान आकार",
        "api_label": "🔑 जेमिनी एपीआई कुंजी दर्ज करें",
        "api_connected": "एपीआई कनेक्टेड 🟢",
        "api_required": "एपीआई कुंजी आवश्यक है 🔴",
        "api_warn": "⚠️ आगे बढ़ने के लिए कृपया साइडबार में अपनी जेमिनी एपीआई कुंजी दर्ज करें।",
        "api_tip": "💡 Google AI Studio से तुरंत अपनी मुफ्त एपीआई कुंजी प्राप्त करें।",
        "tab1": "💬 टेक्स्ट समाधान",
        "tab2": "🎙️ आवाज़ सहायक",
        "tab3": "🖼️ चित्र विश्लेषक",
        "t1_sub": "अपनी समस्या या विचार यहाँ लिखें:",
        "t1_ph": "अपना प्रश्न या स्थानीय समस्या यहाँ टाइप करें...",
        "t1_btn": "समाधान प्राप्त करें 🚀",
        "success": "समाधान तैयार है!",
        "chips_title": "💡 त्वरित सुझाव:",
        "chips": ["🌾 फसल की बीमारी का समाधान", "📜 स्थानीय सरकारी योजना की जानकारी", "⚡ बिजली बचाने के उपाय"]
    },
    "Punjabi (ਪੰਜਾਬੀ)": {
        "sidebar_header": "⚙️ ਕੰਟਰੋਲ ਅਤੇ ਸੈਟਿੰਗਾਂ",
        "title": "🤖 ਸਹਾਇਕ-AI: ਬਹੁਭਾਸ਼ੀ ਸਹਾਇਕ",
        "caption": "ਜੇਮਿਨੀ ਦੁਆਰਾ ਸੰਚਾਲਿਤ ਪੇਸ਼ੇਵਰ ਅਤੇ ਸਰਲ ਏ.ਆਈ",
        "font_label": "🔤 ਫੋਂਟ ਆਕਾਰ ਕੰਟਰੋਲ",
        "current_size": "ਮੌਜੂਦਾ ਆਕਾਰ",
        "api_label": "🔑 API ਕੁੰਜੀ ਦਰਜ ਕਰੋ",
        "api_connected": "API ਕਨੈקט ਹੋ ਗਿਆ 🟢",
        "api_required": "API ਕੁੰਜੀ ਜ਼ਰੂਰੀ ਹੈ 🔴",
        "api_warn": "⚠️ ਸ਼ੁਰੂ ਕਰਨ ਲਈ ਆਪਣੀ API ਕੁੰਜੀ ਦਰਜ ਕਰੋ।",
        "api_tip": "💡 Google AI Studio ਤੋਂ ਮੁਫ਼ਤ ਵਿੱਚ ਪ੍ਰਾਪਤ ਕਰੋ।",
        "tab1": "💬 ਟੈਕਸਟ ਹੱਲ",
        "tab2": "🎙️ ਆਵਾਜ਼ ਸਹਾਇਕ",
        "tab3": "🖼️ ਤਸਵੀਰ ਵਿਸ਼ਲੇਸ਼ਕ",
        "t1_sub": "ਆਪਣੀ ਸਮੱਸਿਆ ਜਾਂ ਵਿਚਾਰ ਇੱਥੇ ਲਿਖੋ:",
        "t1_ph": "ਆਪਣਾ ਸਵਾਲ ਇੱਥੇ ਟਾਈਪ ਕਰੋ...",
        "t1_btn": "ਹੱਲ ਪ੍ਰਾਪਤ ਕਰੋ 🚀",
        "success": "ਹੱਲ ਤਿਆਰ ਹੈ!",
        "chips_title": "💡 ਤੁਰੰਤ ਸੁਝਾਅ:",
        "chips": ["🌾 ਫਸਲ ਦੀ ਬਿਮਾਰੀ ਦਾ ਹੱਲ", "📜 ਸਰਕਾਰੀ ਸਕੀਮਾਂ ਦੀ ਜਾਣਕਾਰੀ", "⚡ ਊਰਜਾ ਬਚਾਉਣ ਦੇ ਤਰੀਕੇ"]
    }
}

default_lang_choice = st.sidebar.selectbox(
    "🌐 Select Language / भाषा चुनें", 
    ["English", "Hindi (हिंदी)", "Punjabi (ਪੰਜਾਬੀ)"]
)

current_ui = ui_texts.get(default_lang_choice, ui_texts["English"])

st.sidebar.markdown(f"### {current_ui['sidebar_header']}")

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

st.sidebar.write(f"{current_ui['current_size']}: **{st.session_state.font_size}px**")
st.sidebar.markdown("---")

api_key = st.sidebar.text_input(current_ui['api_label'], type="password")

if api_key:
    st.sidebar.success(current_ui['api_connected'])
else:
    st.sidebar.error(current_ui['api_required'])

st.title(current_ui["title"])
st.caption(current_ui["caption"])

if not api_key:
    st.warning(current_ui["api_warn"])
    st.info(current_ui["api_tip"])
else:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-3.8-flash")

        if "user_prompt" not in st.session_state:
            st.session_state.user_prompt = ""

        tabs = st.tabs([current_ui["tab1"], current_ui["tab2"], current_ui["tab3"]])

        with tabs[0]:
            st.subheader(current_ui["t1_sub"])
            
            st.markdown(f"**{current_ui['chips_title']}**")
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button(current_ui["chips"][0]):
                    st.session_state.user_prompt = current_ui["chips"][0]
            with c2:
                if st.button(current_ui["chips"][1]):
                    st.session_state.user_prompt = current_ui["chips"][1]
            with c3:
                if st.button(current_ui["chips"][2]):
                    st.session_state.user_prompt = current_ui["chips"][2]

            user_prompt = st.text_area("", value=st.session_state.user_prompt, placeholder=current_ui["t1_ph"], height=100)
            
            if st.button(current_ui["t1_btn"], type="primary"):
                if user_prompt.strip():
                    with st.spinner("Generating..."):
                        try:
                            prompt = f"{user_prompt}\n\nProvide a natural, professional response strictly in {default_lang_choice} language."
                            response = model.generate_content(prompt)
                            st.success(current_ui["success"])
                            st.markdown("### Result / परिणाम:")
                            st.write(response.text)
                        except Exception as e:
                            st.error(f"Error: {e}")
                else:
                    st.warning("Please type something first!")

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
                            response = model.generate_content([f"Analyze this audio and respond naturally in {default_lang_choice}", audio_data])
                            st.success(current_ui["success"])
                            st.write(response.text)
                        except Exception as e:
                            st.error(f"Error: {e}")

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
                            response = model.generate_content([f"{img_prompt}. Respond naturally in {default_lang_choice}.", image])
                            st.success(current_ui["success"])
                            st.write(response.text)
                        except Exception as e:
                            st.error(f"Error: {e}")

    except Exception as err:
        st.error(f"Config Error: {err}")
