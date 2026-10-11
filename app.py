import streamlit as st
import google.generativeai as genai
from PIL import Image

# Responsive Page Config
st.set_page_config(
    page_title="SahayakAI - Multimodal Problem Solver", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Font Resizing & Responsive Interface
if "font_size" not in st.session_state:
    st.session_state.font_size = 16

st.markdown(f"""
    <style>
    html, body, [class*="css"] {{
        font-size: {st.session_state.font_size}px !important;
    }}
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 95% !important;
    }}
    .font-box {{
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 10px;
    }}
    </style>
""", unsafe_allow_html=True)

# Sidebar Configuration & Language Control
st.sidebar.header("⚙️ Settings / सेटिंग्स")

# Language Selection First so UI can adapt
target_lang = st.sidebar.selectbox(
    "🌐 Choose Language / भाषा चुनें", 
    ["English", "Hindi (हिंदी)", "Mandayali / Himachali (मंडयाली)", "Punjabi (ਪੰਜਾਬੀ)", "Bengali (বাংলা)", "Marathi (मराठी)", "Tamil (தமிழ்)"]
)

# Dictionary for multi-lingual UI labels
ui_texts = {
    "English": {
        "title": "🤖 SahayakAI: Multimodal & Vernacular AI Assistant",
        "caption": "Your 24/7 Accessible, Voice-Enabled, Multi-lingual Problem Solver",
        "font_label": "🔤 Accessibility: Font Size",
        "api_header": "🔑 Gemini API Key",
        "api_input": "Enter Gemini API Key",
        "api_warning": "⚠️ Please enter your Google Gemini API Key in the sidebar to proceed.",
        "tab1": "💬 Text & Problem Solver",
        "tab2": "🎙️ Voice Input Helper",
        "tab3": "🖼️ Image Analyzer",
        "t1_sub": "Describe your problem or idea:",
        "t1_placeholder": "Type your question, local community issue, or project idea here...",
        "t1_btn": "Generate Solution 🚀",
        "success": "Solution Generated successfully!"
    },
    "Hindi (हिंदी)": {
        "title": "🤖 सहायक-AI: बहुभाषी और सुलभ समस्या समाधान सहायक",
        "caption": "आपकी 24/7 सुलभ, आवाज़-सक्षम, बहुभाषी समस्या समाधान सहायक",
        "font_label": "🔤 दृश्यता: फ़ॉन्ट आकार (अक्षर बड़ा/छोटा करें)",
        "api_header": "🔑 जेमिनी एपीआई कुंजी (API Key)",
        "api_input": "जेमिनी एपीआई कुंजी दर्ज करें",
        "api_warning": "⚠️ आगे बढ़ने के लिए कृपया साइडबार में अपनी Google Gemini API Key दर्ज करें।",
        "tab1": "💬 टेक्स्ट और समस्या समाधान",
        "tab2": "🎙️ आवाज़ (Voice) सहायक",
        "tab3": "🖼️ चित्र (Image) विश्लेषक",
        "t1_sub": "अपनी समस्या या विचार यहाँ लिखें:",
        "t1_placeholder": "अपना प्रश्न, स्थानीय सामुदायिक समस्या, या प्रोजेक्ट विचार यहाँ टाइप करें...",
        "t1_btn": "समाधान प्राप्त करें 🚀",
        "success": "सफलतापूर्वक समाधान उत्पन्न हुआ!"
    },
    "Mandayali / Himachali (मंडयाली)": {
        "title": "🤖 सहायक-AI: मंडयाली ते स्थानीय समस्या समाधान सहायक",
        "caption": "तुहारी अपनी भाषा मां हर समस्या दा हल",
        "font_label": "🔤 अक्षर बड़ा-छोटा करो (Font Size)",
        "api_header": "🔑 एपीआई की (API Key)",
        "api_input": "अपनी Gemini API Key इथे पायो",
        "api_warning": "⚠️ कृपया बक्से मां अपनी API Key दर्ज करो जी।",
        "tab1": "💬 लिखकरी समस्या हल करो",
        "tab2": "🎙️ बोलकरी सुणो",
        "tab3": "🖼️ फोटो दिखाइयो",
        "t1_sub": "अपनी समस्या या विचार इथे लिखो:",
        "t1_placeholder": "अपणा सवाल या समस्या इथे लिखो...",
        "t1_btn": "समाधान दिखाओ 🚀",
        "success": "समाधान तैयार होई गेया!"
    }
}

# Fallback to English if specific dictionary isn't fully loaded
current_ui = ui_texts.get(target_lang, ui_texts["English"])

# App Header
st.title(current_ui["title"])
st.caption(current_ui["caption"])

# Prominent Accessibility Font Resizer in Sidebar
st.sidebar.markdown(f"### {current_ui['font_label']}")
col_f1, col_f2, col_f3 = st.sidebar.columns(3)
with col_f1:
    if st.button("A- (Chota)"):
        if st.session_state.font_size > 12:
            st.session_state.font_size -= 2
            st.rerun()
with col_f2:
    if st.button("A (Normal)"):
        st.session_state.font_size = 16
        st.rerun()
with col_f3:
    if st.button("A+ (Bada)"):
        if st.session_state.font_size < 28:
            st.session_state.font_size += 2
            st.rerun()

st.sidebar.markdown(f"Current Size: **{st.session_state.font_size}px**")
st.sidebar.markdown("---")

# API Key Input
st.sidebar.header(current_ui["api_header"])
api_key = st.sidebar.text_input(current_ui["api_input"], type="password")

if not api_key:
    st.warning(current_ui["api_warning"])
    st.info("💡 Tip: Get a free key instantly from [Google AI Studio](https://aistudio.google.com/).")
else:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-3.8-flash")

        tabs = st.tabs([current_ui["tab1"], current_ui["tab2"], current_ui["tab3"]])

        # Tab 1: Text Solver
        with tabs[0]:
            st.subheader(current_ui["t1_sub"])
            user_prompt = st.text_area("", placeholder=current_ui["t1_placeholder"], height=120)
            
            if st.button(current_ui["t1_btn"], type="primary"):
                if user_prompt.strip():
                    with st.spinner("AI is thinking..."):
                        try:
                            full_query = f"{user_prompt}\n\nIMPORTANT: Provide the complete explanation strictly in {target_lang} language."
                            response = model.generate_content(full_query)
                            st.success(current_ui["success"])
                            st.markdown("### Result / परिणाम:")
                            st.write(response.text)
                        except Exception as e:
                            st.error(f"Error: {e}")
                else:
                    st.warning("Please enter some text!")

        # Tab 2: Voice Helper
        with tabs[1]:
            st.subheader("🎙️ Voice & Audio Recording Assistant")
            audio_file = st.file_uploader("Upload Audio file (WAV, MP3)", type=["wav", "mp3", "m4a"])
            if audio_file is not None:
                st.audio(audio_file)
                if st.button("Analyze Audio 🚀", type="primary"):
                    with st.spinner("Processing audio..."):
                        try:
                            audio_bytes = audio_file.read()
                            audio_data = {"mime_type": audio_file.type, "data": audio_bytes}
                            response = model.generate_content([f"Analyze this audio and respond in {target_lang}", audio_data])
                            st.success(current_ui["success"])
                            st.write(response.text)
                        except Exception as e:
                            st.error(f"Error: {e}")

        # Tab 3: Image Analyzer
        with tabs[2]:
            st.subheader("🖼️ Image & Document Analyzer")
            uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
            img_prompt = st.text_input("What do you want to ask about this image?", "Explain this image.")

            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                st.image(image, use_column_width=True)
                if st.button("Analyze Image 🔍", type="primary"):
                    with st.spinner("Analyzing..."):
                        try:
                            response = model.generate_content([f"{img_prompt}. Respond in {target_lang}.", image])
                            st.success(current_ui["success"])
                            st.write(response.text)
                        except Exception as e:
                            st.error(f"Error: {e}")

    except Exception as err:
        st.error(f"Config Error: {err}")
