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
    st.markdown("Upload an image/screenshot/pdf of a restaurant advertising media.")
    uploaded_file = st.file_uploader(
        "Upload an image/screenshot (PNG, JPG, JPEG) or PDF of a document:",
        type=["png", "jpg", "jpeg", "pdf"],
    )

    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            # Convert a pdf to image and only use the first page.
            image = convert_from_bytes(uploaded_file.read())[0]
        else:
            image = Image.open(uploaded_file).convert("RGB")

    show_image = st.toggle("Show uploaded image")
    if show_image and uploaded_file:
        st.image(image)

    # Extract data
    if st.button("Extract Information"):
        if not uploaded_file:
            st.warning("Please upload a PDF/PNG file.")
        elif not api_key:
            st.warning(
                "You must insert an OpenAI API key in the Setup tab before extracting information."
            )
        else:
            st.session_state["data"] = {}
            with st.spinner("Extracting..."):
                image.save("temp.png")
                image_documents = SimpleDirectoryReader(input_files=["temp.png"]).load_data()
                try:
                    response = extract_data(
                        image_documents,
                        data_extract_str,
                        llm_name,
                        model_temperature,
                        api_key,
                    )
                except Exception as e:
                    raise e
                finally:
                    os.remove("temp.png")
            st.session_state["data"].update(response)

    if "data" in st.session_state and st.session_state["data"]:
        # Edit result
        edit_data = st.toggle("Edit data")
        if edit_data:
            st.markdown("Double click in a cell of the value column to edit the data.")
            updated_data = st.data_editor(st.session_state["data"])
            st.session_state["data"] = updated_data
        else:
            st.markdown("Extracted data")
            st.json(st.session_state["data"])

        # Confirm and save result
        confirm = st.checkbox("Confirm the result is correct.")
        if confirm:
            if st.button("Insert data?"):
                with st.spinner("Inserting data..."):
                    save_path = generate_unique_path(uploaded_file.name)
                    save_path.parent.mkdir(parents=True, exist_ok=True)
                    image.save(save_path)
                    payload = json.dumps(st.session_state["data"], indent=4)
                    store_result(payload, save_path.as_posix())

                st.session_state["all_data"] = load_data_as_dataframe()
                st.session_state["data"] = {}

                # Notify user that he has successfully inserted the data.
                container = st.empty()
                container.success("Successfully inserted data to the database.")
                time.sleep(1)
                container.empty()

                st.rerun()

with all_data_tab:
    # Show all data in the database (for verification purpose)
    st.subheader("All Saved Data")
    st.markdown("Double click in a cell to see the entire value.")
    st.dataframe(st.session_state["all_data"], use_container_width=True)
