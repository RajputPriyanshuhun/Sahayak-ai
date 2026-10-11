import streamlit as st
import google.generativeai as genai
from PIL import Image

# Page Configuration for Fast & Smooth Performance
st.set_page_config(
    page_title="SahayakAI - Multilingual Problem Solver", 
    page_icon="🤖", 
    layout="centered"
)

# Initialize Session State for Font Size
if "font_size" not in st.session_state:
    st.session_state.font_size = 16

# Clean & Professional CSS (No Lag)
st.markdown(f"""
    <style>
    html, body, [class*="css"] {{
        font-size: {st.session_state.font_size}px;
    }}
    .stButton>button {{
        width: 100%;
        border-radius: 6px;
        font-weight: bold;
    }}
    </style>
""", unsafe_allow_html=True)

# App Title & Header
st.title("🤖 SahayakAI: Multimodal Assistant")
st.caption("Professional, Fast & Accessible AI Powered by Gemini")

# Sidebar Controls (Clean & Fast)
st.sidebar.header("⚙️ Controls & Settings")

# Font Size Accessibility Control
st.sidebar.subheader("🔤 Font Size (Accessibility)")
col1, col2, col3 = st.sidebar.columns(3)
with col1:
    if st.button("A-"):
        if st.session_state.font_size > 12:
            st.session_state.font_size -= 2
            st.rerun()
with col2:
    if st.button("Normal"):
        st.session_state.font_size = 16
        st.rerun()
with col3:
    if st.button("A+"):
        if st.session_state.font_size < 24:
            st.session_state.font_size += 2
            st.rerun()

st.sidebar.write(f"Size: **{st.session_state.font_size}px**")
st.sidebar.markdown("---")

# Language Selection for Output
target_lang = st.sidebar.selectbox(
    "🌐 Output Language", 
    ["English", "Hindi (हिंदी)", "Mandayali / Himachali (मंडयाली)", "Punjabi (ਪੰਜਾਬੀ)", "Bengali (বাংলা)"]
)

st.sidebar.markdown("---")
api_key = st.sidebar.text_input("🔑 Enter Gemini API Key", type="password")

if not api_key:
    st.warning("⚠️ Please enter your Gemini API Key in the sidebar to begin.")
    st.info("💡 Get a free key instantly from [Google AI Studio](https://aistudio.google.com/).")
else:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-3.8-flash")

        # Tabs for different features
        tabs = st.tabs(["💬 Text Solver", "🎙️ Voice Helper", "🖼️ Image Analyzer"])

        # Tab 1: Text Solver
        with tabs[0]:
            st.subheader("Describe your problem or idea:")
            user_prompt = st.text_area("Type your question or issue here...", height=100)
            
            if st.button("Generate Solution 🚀", type="primary"):
                if user_prompt.strip():
                    with st.spinner("AI is generating solution..."):
                        try:
                            prompt = f"{user_prompt}\n\nProvide the complete response in {target_lang} language."
                            response = model.generate_content(prompt)
                            st.success("Solution Ready!")
                            st.markdown("### Result:")
                            st.write(response.text)
                        except Exception as e:
                            st.error(f"Error: {e}")
                else:
                    st.warning("Please type something first!")

        # Tab 2: Voice Helper
        with tabs[1]:
            st.subheader("🎙️ Audio / Voice Assistant")
            audio_file = st.file_uploader("Upload audio recording (WAV, MP3)", type=["wav", "mp3", "m4a"])
            
            if audio_file is not None:
                st.audio(audio_file)
                if st.button("Analyze Audio 🚀", type="primary"):
                    with st.spinner("Processing audio..."):
                        try:
                            audio_bytes = audio_file.read()
                            audio_data = {"mime_type": audio_file.type, "data": audio_bytes}
                            response = model.generate_content([f"Analyze this audio and respond in {target_lang}", audio_data])
                            st.success("Audio Analyzed!")
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
                    with st.spinner("Analyzing image..."):
                        try:
                            response = model.generate_content([f"{img_prompt}. Respond in {target_lang}.", image])
                            st.success("Analysis Complete!")
                            st.write(response.text)
                        except Exception as e:
                            st.error(f"Error: {e}")

    except Exception as err:
        st.error(f"Configuration Error: {err}")
