import streamlit as st
from neatappv2.extractor import Extractor
from neatappv2.storage import StorageManager
from neatappv2.document import DocumentHandler
from neatappv2.config import Config

class NeatApp:
    def __init__(self):
        self.config = Config()
        self.extractor = Extractor()
        self.storage = StorageManager()
        self.doc_handler = DocumentHandler()
        if "all_data" not in st.session_state:
            st.session_state["all_data"] = self.storage.load_all_data()

    def run(self):
        st.title("Image/PDF Data Extractor")
        st.markdown("Upload your image/pdf and extract data from it.")
        setup_tab, upload_tab, all_data_tab = st.tabs([
            "Setup", "Upload/Extract Data", "All Saved Data"
        ])
        self.setup_ui(setup_tab)
        self.upload_ui(upload_tab)
        self.all_data_ui(all_data_tab)

    def setup_ui(self, tab):
        with tab:
            st.subheader("LLM Setup")
            api_key = st.text_input("OpenAI API Key", type="password", value=self.config.api_key)
            llm_model = st.selectbox("Which LLM?", self.config.llm_models, index=self.config.default_llm_index)
            temperature = st.slider("LLM Temperature", 0.0, 1.0, self.config.model_temperature)
            prompt = st.text_area("Extraction Prompt", value=self.config.prompt)
            self.config.api_key = api_key
            self.config.llm_model = llm_model
            self.config.model_temperature = temperature
            self.config.prompt = prompt

    def upload_ui(self, tab):
        with tab:
            st.subheader("Extract Information")
            st.markdown("Upload an image/screenshot/pdf of a restaurant advertising media.")
            uploaded_file = st.file_uploader(
                "Upload image (PNG/JPG/JPEG) or PDF", type=["png", "jpg", "jpeg", "pdf"])
            image = None
            if uploaded_file:
                image = self.doc_handler.get_image(uploaded_file)
                if st.toggle("Show uploaded image"):
                    st.image(image)
                if st.button("Extract Information"):
                    if not self.config.api_key:
                        st.warning("Insert an OpenAI API key in Setup tab.")
                        return
                    with st.spinner("Extracting..."):
                        result = self.extractor.extract(
                            image,
                            self.config.prompt,
                            self.config.llm_model,
                            self.config.model_temperature,
                            self.config.api_key
                        )
                        st.session_state["data"] = result
            # Edit & Confirm
            if st.session_state.get("data"):
                self.edit_and_save_ui(image, uploaded_file)

    def edit_and_save_ui(self, image, uploaded_file):
        edit_mode = st.toggle("Edit data")
        if edit_mode:
            st.data_editor(st.session_state["data"])
        else:
            st.json(st.session_state["data"])
        confirm = st.checkbox("Confirm the result is correct")
        if confirm and st.button("Insert data?"):
            with st.spinner("Saving data..."):
                save_path = self.doc_handler.generate_save_path(uploaded_file.name)
                image.save(save_path)
                self.storage.save_result(st.session_state["data"], str(save_path))
            st.success("Successfully inserted data.")
            st.session_state["all_data"] = self.storage.load_all_data()
            st.session_state["data"] = {}
            st.rerun()

    def all_data_ui(self, tab):
        with tab:
            st.subheader("All Saved Data")
            st.markdown("Double click in a cell to see the entire value.")
            st.dataframe(st.session_state["all_data"], use_container_width=True)

def main():
    app = NeatApp()
    app.run()

if __name__ == "__main__":
    main()