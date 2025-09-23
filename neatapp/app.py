import json
import os
import time

import streamlit as st
from llama_index.core import SimpleDirectoryReader
from pdf2image import convert_from_bytes
from PIL import Image

from neatapp.constants import DATA_EXTRACT_STR
from neatapp.data import extract_data
from neatapp.db import load_data_as_dataframe, store_result
from neatapp.utils import generate_unique_path

if "all_data" not in st.session_state:
    st.session_state["all_data"] = load_data_as_dataframe()

st.title("Simple App")
st.markdown(("AI This demo allows you to upload your image/pdf and extract data from it."))

setup_tab, upload_tab, all_data_tab = st.tabs(["Setup", "Upload/Extract Data", "All Saved Data"])

with setup_tab:
    st.subheader("LLM Setup")
    api_key = st.text_input("Enter your OpenAI API key here", type="password")
    llm_name = st.selectbox("Which LLM?", ["gpt-4-vision-preview"])
    model_temperature = st.slider("LLM Temperature", min_value=0.0, max_value=1.0, step=0.1)
    data_extract_str = st.text_area("The query to extract data with.", value=DATA_EXTRACT_STR)

with upload_tab:

    st.subheader("Extract Information")
    st.markdown("Upload an image/screenshot/pdf of a restaurant advertising media.")
    uploaded_file = st.file_uploader(
        "Upload an image/screenshot (PNG, JPG, JPEG) or PDF of a document:",
        type=["png", "jpg", "jpeg", "pdf"],
    )

    if uploaded_file:
        if uploaded_file.type == "application/pdf":