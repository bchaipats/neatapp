import streamlit as st
from PIL import Image

from neatapp.constants import DATA_EXTRACT_STR

st.title("Image/PDF Data Extractor")
st.markdown(("This demo allows you to upload your image/pdf and extract data from it."))

setup_tab, upload_tab = st.tabs(["Setup", "Upload/Extract Data"])

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
