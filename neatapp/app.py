import os

import streamlit as st
from llama_index.core import SimpleDirectoryReader
from PIL import Image

from neatapp.constants import DATA_EXTRACT_STR
from neatapp.data import extract_data
from neatapp.db import load_data_as_dataframe

if "all_data" not in st.session_state:
    st.session_state["all_data"] = load_data_as_dataframe()

st.title("Image/PDF Data Extractor")
st.markdown(("This demo allows you to upload your image/pdf and extract data from it."))

setup_tab, upload_tab, all_data_tab = st.tabs(["Setup", "Upload/Extract Data", "All Saved Data"])

with setup_tab:
    st.subheader("LLM Setup")
    api_key = st.text_input("Enter your OpenAI API key here", type="password")
    llm_name = st.selectbox("Which LLM?", ["gpt-4-vision-preview"])
    model_temperature = st.slider("LLM Temperature", min_value=0.0, max_value=1.0, step=0.1)
    data_extract_str = st.text_area("The query to extract data with.", value=DATA_EXTRACT_STR)

with upload_tab:
    st.subheader("Extract Information")
    st.markdown("Either upload an image/screenshot of a document, or enter the text manually.")
    uploaded_file = st.file_uploader(
        "Upload an image/screenshot of a document:", type=["png", "jpg", "jpeg"]
    )

    show_image = st.toggle("Show uploaded image")
    if show_image and uploaded_file:
        st.image(Image.open(uploaded_file).convert("RGB"))

    if st.button("Extract Information"):
        if not uploaded_file:
            st.warning("Please upload a PDF/PNG file.")
        elif not api_key:
            st.warning(
                "You must insert an OpenAI API key in the Setup tab before extracting information."
            )
        else:
            st.session_state["data"] = {}
            data = {}
            with st.spinner("Extracting..."):
                if uploaded_file:
                    Image.open(uploaded_file).convert("RGB").save("temp.png")
                    image_documents = SimpleDirectoryReader(input_files=["temp.png"]).load_data()
                    response = extract_data(
                        image_documents,
                        data_extract_str,
                        llm_name,
                        model_temperature,
                        api_key,
                    )
                    data.update(response)
                    os.remove("temp.png")
            st.session_state["data"].update(data)
            st.session_state["filename"] = uploaded_file.name

    if "data" in st.session_state and st.session_state["data"]:
        st.markdown("Extracted data")
        st.json(st.session_state["data"])

with all_data_tab:
    st.subheader("All Saved Data")
    st.dataframe(st.session_state["all_data"])
