import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="SahayakAI - Multimodal Problem Solver", page_icon="🤖", layout="centered")

st.title("🤖 SahayakAI: Multimodal Problem Solver")
st.markdown("Your 24/7 AI companion for solving local problems, analyzing documents, and generating instant insights.")

# Sidebar for API key
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter your Gemini API Key", type="password")

if not api_key:
    st.warning("Please enter your Google Gemini API Key in the sidebar to proceed.")
    st.info("💡 Tip: You can get a free API key instantly in seconds from [Google AI Studio](https://aistudio.google.com/).")
else:
    try:
        genai.configure(api_key=api_key)
        
        # Updated working models for latest Gemini API
        model_name = st.sidebar.selectbox("Select AI Model", ["gemini-3.8-flash", "gemini-flash"])
        model = genai.GenerativeModel(model_name)

        tabs = st.tabs(["💬 Text & Problem Solver", "🖼️ Image & Document Analyzer"])

        with tabs[0]:
            st.subheader("Describe your problem or idea:")
            user_prompt = st.text_area("Type your question, local community issue, or project idea here...", height=120)
            
            if st.button("Generate Solution 🚀", type="primary"):
                if user_prompt.strip():
                    with st.spinner("AI is thinking..."):
                        try:
                            response = model.generate_content(user_prompt)
                            st.success("Solution Generated!")
                            st.markdown("### Result:")
                            st.write(response.text)
                        except Exception as e:
                            st.error(f"Execution Error: {e}")
                else:
                    st.warning("Please enter some text first!")

        with tabs[1]:
            st.subheader("Upload an Image, Document, or Screenshot:")
            uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
            image_prompt = st.text_input("What do you want the AI to do with this image?", "Explain what is in this image and provide a helpful solution.")

            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", use_column_width=True)

                if st.button("Analyze Image 🔍", type="primary"):
                    with st.spinner("Analyzing image..."):
                        try:
                            response = model.generate_content([image_prompt, image])
                            st.success("Analysis Complete!")
                            st.markdown("### Analysis Report:")
                            st.write(response.text)
                        except Exception as e:
                            st.error(f"Execution Error: {e}")

    except Exception as err:
        st.error(f"Configuration Error: {err}")
