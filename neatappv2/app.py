import os
import streamlit as st
from PIL import Image
from pdf2image import convert_from_bytes

from neatappv2.constants import DATA_EXTRACT_PROMPT
from neatappv2.data import extract_data
from neatappv2.db import store_result, load_all_data
from neatappv2.utils import generate_unique_image_path, get_multimodal_llm

st.title("Neatappv2: Clean Image/PDF Data Extractor")

# Initialize session state
if "data" not in st.session_state:
    st.session_state["data"] = load_all_data()

# File uploader
uploaded_file = st.file_uploader("Upload an image or PDF", type=["png", "jpg", "jpeg", "pdf"])

if uploaded_file:
    file_bytes = uploaded_file.read()

    # Convert PDF to images if needed
    if uploaded_file.type == "application/pdf":
        images = convert_from_bytes(file_bytes)
    else:
        images = [Image.open(uploaded_file)]

    st.image(images[0], caption="Uploaded Image", use_column_width=True)

    # User inputs for LLM
    llm_name = st.text_input("OpenAI Model Name", value="gpt-4-vision-preview")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.0, 0.1)
    api_key = st.text_input("OpenAI API Key", type="password")

    if st.button("Extract Data"):
        if not api_key:
            st.error("Please provide your OpenAI API Key.")
        else:
            # Prepare multimodal LLM
            llm = get_multimodal_llm(llm_name, temperature, api_key)

            # Extract data
            st.info("Extracting data... This might take some time.")
            data = extract_data(images, DATA_EXTRACT_PROMPT, llm)

            # Show extracted data
            st.json(data)

            # Save result
            unique_image_path = generate_unique_image_path(uploaded_file.name)
            images[0].save(unique_image_path)
            store_result(data, unique_image_path)

            # Reload all data
            st.session_state["data"] = load_all_data()
            st.success("Data extracted and saved successfully.")

# Display data table
st.header("Extracted Data Records")
st.dataframe(st.session_state["data"])