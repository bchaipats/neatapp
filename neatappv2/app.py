import os
import time
import json

import streamlit as st
from PIL import Image
from pdf2image import convert_from_bytes
from llama_index.core import SimpleDirectoryReader

from neatappv2.constants import DATA_EXTRACT_STR
from neatappv2.data import LLMClient, DataExtractor
from neatappv2.db import DatabaseManager
from neatappv2.utils import generate_unique_path


class AppUI:
    def __init__(self):
        if "all_data" not in st.session_state:
            self.db_manager = DatabaseManager()
            st.session_state["all_data"] = self.db_manager.load_all_data()

        self.db_manager = DatabaseManager()

        st.title("Image/PDF Data Extractor")
        st.markdown("This demo allows you to upload your image/pdf and extract data from it.")

        self.setup_tab, self.upload_tab, self.all_data_tab = st.tabs(
            ["Setup", "Upload/Extract Data", "All Saved Data"]
        )

        with self.setup_tab:
            self.api_key = st.text_input("Enter your OpenAI API key here", type="password")
            self.llm_name = st.selectbox("Which LLM?", ["gpt-4-vision-preview"])
            self.model_temperature = st.slider("LLM Temperature", 0.0, 1.0, 0.0, 0.1)
            self.data_extract_str = st.text_area("The query to extract data with.", value=DATA_EXTRACT_STR)

        with self.upload_tab:
            self.render_upload_tab()

        with self.all_data_tab:
            self.render_all_data_tab()

    def render_upload_tab(self):
        st.subheader("Extract Information")
        st.markdown("Upload an image/screenshot/pdf of a restaurant advertising media.")
        uploaded_file = st.file_uploader(
            "Upload an image/screenshot (PNG, JPG, JPEG) or PDF of a document:",
            type=["png", "jpg", "jpeg", "pdf"],
        )
        if uploaded_file:
            if uploaded_file.type == "application/pdf":
                image = convert_from_bytes(uploaded_file.read())[0]
            else:
                image = Image.open(uploaded_file).convert("RGB")

            show_image = st.toggle("Show uploaded image")
            if show_image:
                st.image(image)

            if st.button("Extract Information"):
                self.extract_and_show_result(image, uploaded_file.name)
        else:
            st.info("Please upload a supported file to extract data.")

    def extract_and_show_result(self, image: Image.Image, file_name: str):
        if not self.api_key:
            st.warning("You must insert an OpenAI API key in the Setup tab before extracting information.")
            return

        st.session_state["data"] = {}
        with st.spinner("Extracting..."):
            image.save("temp.png")
            image_documents = SimpleDirectoryReader(input_files=["temp.png"]).load_data()

            llm_client = LLMClient(self.llm_name, self.model_temperature, self.api_key)
            extractor = DataExtractor(llm_client, self.data_extract_str)
            try:
                response = extractor.extract(image_documents)
            finally:
                os.remove("temp.png")

            st.session_state["data"].update(response)

        self.show_extraction_result(image, file_name)

    def show_extraction_result(self, image: Image.Image, file_name: str):
        if "data" in st.session_state and st.session_state["data"]:
            edit_data = st.toggle("Edit data")
            if edit_data:
                st.markdown("Double click in a cell of the value column to edit the data.")
                updated_data = st.data_editor(st.session_state["data"])
                st.session_state["data"] = updated_data
            else:
                st.markdown("Extracted data")
                st.json(st.session_state["data"])

            confirm = st.checkbox("Confirm the result is correct.")
            if confirm:
                if st.button("Insert data?"):
                    with st.spinner("Inserting data..."):
                        save_path = generate_unique_path(file_name)
                        save_path.parent.mkdir(parents=True, exist_ok=True)
                        image.save(save_path)
                        payload = json.dumps(st.session_state["data"], indent=4)
                        self.db_manager.store_result(payload, save_path.as_posix())

                    st.session_state["all_data"] = self.db_manager.load_all_data()
                    st.session_state["data"] = {}

                    container = st.empty()
                    container.success("Successfully inserted data to the database.")
                    time.sleep(1)
                    container.empty()

                    st.experimental_rerun()

    def render_all_data_tab(self):
        st.subheader("All Saved Data")
        st.markdown("Double click in a cell to see the entire value.")
        st.dataframe(st.session_state["all_data"], use_container_width=True)


def main():
    AppUI()


if __name__ == "__main__":
    main()