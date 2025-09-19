import os
import time
import json
from pathlib import Path
from PIL import Image
import streamlit as st
from pdf2image import convert_from_bytes
from llama_index.core import SimpleDirectoryReader
from neatapp.neatappv2.config import AppConfig
from neatapp.neatappv2.database import Database
from neatapp.neatappv2.utils import generate_unique_path, build_openai_multimodal
from neatapp.neatappv2.llm import extract_data_with_llm

# Load/Create session database/cache
if "all_data" not in st.session_state:
    st.session_state["all_data"] = Database().load_all()

def main():
    st.title("Neatapp v2: AI Media Extractor")
    tabs = st.tabs(["Setup", "Upload/Extract", "All Data"])

    # --- SETUP TAB ---
    with tabs[0]:
        st.subheader("LLM & Extraction Settings")
        api_key = st.text_input("Enter your OpenAI API key", type="password")
        llm_name = st.selectbox("Vision LLM Model", [AppConfig.DEFAULT_LLM])
        temp = st.slider("Model temperature", 0.0, 1.0, AppConfig.DEFAULT_TEMPERATURE)
        prompt = st.text_area("Data extraction prompt", value=AppConfig.DATA_EXTRACT_PROMPT)

    # --- UPLOAD & EXTRACT TAB ---
    with tabs[1]:
        st.subheader("Upload Ad Media")
        file = st.file_uploader(
            "Upload restaurant image/pdf:",
            type=["png", "jpg", "jpeg", "pdf"]
        )
        image = None
        if file:
            if file.type == "application/pdf":
                image = convert_from_bytes(file.read())[0]
            else:
                image = Image.open(file).convert("RGB")

        if file and st.toggle("Show uploaded image"):
            st.image(image)

        if st.button("Extract Data"):
            if not api_key:
                st.warning("Please provide your OpenAI API key in Setup tab.")
            else:
                with st.spinner("Extracting using LLM..."):
                    temp_path = "temp_neatv2.png"
                    image.save(temp_path)
                    image_docs = SimpleDirectoryReader(input_files=[temp_path]).load_data()
                    llm = build_openai_multimodal(llm_name, temp, api_key)
                    try:
                        response = extract_data_with_llm(image_docs, prompt, llm)
                    except Exception as e:
                        st.error(f"Extraction failed: {e}")
                        os.remove(temp_path)
                        return
                    finally:
                        if Path(temp_path).exists():
                            os.remove(temp_path)
                    st.session_state["extracted"] = response

        if "extracted" in st.session_state and st.session_state["extracted"]:
            data = st.session_state["extracted"]
            edited = st.data_editor(vars(data))
            # Enable DB insert
            if st.checkbox("Save result to database"):
                if st.button("Save now!"):
                    save_path = generate_unique_path(file.name)
                    save_path.parent.mkdir(parents=True, exist_ok=True)
                    image.save(save_path)
                    Database().insert_result(edited, str(save_path))
                    st.success("Saved!")
                    # Reload for All Data tab
                    st.session_state["all_data"] = Database().load_all()
                    st.session_state.pop("extracted")
                    st.rerun()

    # --- ALL DATA TAB ---
    with tabs[2]:
        st.subheader("All Saved Extractions")
        df = st.session_state["all_data"]
        st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()