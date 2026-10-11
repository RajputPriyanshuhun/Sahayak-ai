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

# Custom CSS for Font Resizing & Responsive Mobile/Desktop Interface
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
    stButton > button {{
        width: 100%;
        border-radius: 8px;
    }}
    </style>
""", unsafe_allow_html=True)

# App Header
st.title("🤖 SahayakAI: Multimodal & Vernacular AI Assistant")
st.caption("Your 24/7 Accessible, Voice-Enabled, Multi-lingual Problem Solver")

# Sidebar Configuration
st.sidebar.header("⚙️ App Controls & Accessibility")

# Accessibility: Font Resizer
st.sidebar.subheader("🔤 Font Size (Accessibility)")
col_font1, col_font2, col_font3 = st.sidebar.columns(3)
with col_font1:
    if st.button("A-"):
        if st.session_state.font_size > 12:
            st.session_state.font_size -= 2
            st.rerun()
with col_font2:
    if st.button("A"):
        st.session_state.font_size = 16
        st.rerun()
with col_font3:
    if st.button("A+"):
        if st.session_state.font_size < 26:
            st.session_state.font_size += 2
            st.rerun()

st.sidebar.write(f"Current Font Size: **{st.session_state.font_size}px**")

# Language Selection
st.sidebar.subheader("🌐 Language Options")
target_lang = st.sidebar.selectbox(
    "Preferred Output Language", 
    ["English", "Hindi (हिंदी)", "Mandayali / Himachali (मंडयाली)", "Punjabi (ਪੰਜਾਬੀ)", "Bengali (বাংলা)", "Marathi (मराठी)", "Tamil (தமிழ்)"]
)

# API Key Input
st.sidebar.subheader("🔑 API Key")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if not api_key:
    st.warning("⚠️ Please enter your Google Gemini API Key in the sidebar to proceed.")
    st.info("💡 You can get a free API key instantly from [Google AI Studio](https://aistudio.google.com/).")
else:
    try:
        genai.configure(api_key=api_key)
        model_name = st.sidebar.selectbox("AI Model", ["gemini-3.8-flash", "gemini-flash"])
        model = genai.GenerativeModel(model_name)

        tabs = st.tabs(["💬 Text & Problem Solver", "🎙️ Voice Input Helper", "🖼️ Image & Document Analyzer"])

        # Tab 1: Text & Problem Solver
        with tabs[0]:
            st.subheader("Describe your problem or idea:")
            user_prompt = st.text_area("Type your question, local community issue, or project idea here...", height=120)
            
            if st.button("Generate Solution 🚀", type="primary"):
                if user_prompt.strip():
                    with st.spinner("AI is thinking & translating..."):
                        try:
                            prompt_with_lang = f"{user_prompt}\n\nIMPORTANT: Please provide the entire response clearly in {target_lang} language."
                            response = model.generate_content(prompt_with_lang)
                            st.success(f"Solution Generated in {target_lang}!")
                            st.markdown("### Result:")
                            st.write(response.text)
                        except Exception as e:
                            st.error(f"Execution Error: {e}")
                else:
                    st.warning("Please enter some text first!")

        # Tab 2: Voice Input Helper
        with tabs[1]:
            st.subheader("🎙️ Voice & Speech Assistant")
            st.info("Use your device microphone or upload a voice recording to ask AI directly!")
            audio_file = st.file_uploader("Upload Audio / Speech recording (WAV, MP3, M4A)", type=["wav", "mp3", "m4a"])
            
            voice_prompt = st.text_input("Additional Instructions for Audio (Optional)", f"Listen to this audio, summarize the issue, and provide a clear solution in {target_lang}.")

            if audio_file is not None:
                st.audio(audio_file)
                if st.button("Analyze Audio Solution 🚀", type="primary"):
                    with st.spinner("Processing audio with AI..."):
                        try:
                            # Gemini can process audio directly
                            audio_bytes = audio_file.read()
                            audio_data = {
                                "mime_type": audio_file.type,
                                "data": audio_bytes
                            }
                            response = model.generate_content([voice_prompt, audio_data])
                            st.success(f"Audio Analyzed in {target_lang}!")
                            st.markdown("### Result from Voice:")
                            st.write(response.text)
                        except Exception as e:
                            st.error(f"Voice Processing Error: {e}")

        # Tab 3: Image & Document Analyzer
        with tabs[3-1]:
            st.subheader("Upload an Image, Document, or Screenshot:")
            uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
            image_prompt = st.text_input("What do you want the AI to do with this image?", f"Explain what is in this image and provide a helpful solution in {target_lang}.")

            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", use_column_width=True)

                if st.button("Analyze Image 🔍", type="primary"):
                    with st.spinner("Analyzing image..."):
                        try:
                            response = model.generate_content([image_prompt, image])
                            st.success(f"Analysis Complete in {target_lang}!")
                            st.markdown("### Analysis Report:")
                            st.write(response.text)
                        except Exception as e:
                            st.error(f"Execution Error: {e}")

    except Exception as err:
        st.error(f"Configuration Error: {err}")
