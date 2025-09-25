from llama_index.core import SimpleDirectoryReader
from neatapp.data import extract_data
from PIL import Image
import tempfile

class Extractor:
    def extract(self, image: Image.Image, query: str, model_name: str, temperature: float, api_key: str):
        # Save temp image so that SimpleDirectoryReader works as before
        with tempfile.NamedTemporaryFile(suffix='.png', delete=True) as temp:
            image.save(temp.name)
            image_docs = SimpleDirectoryReader(input_files=[temp.name]).load_data()
            response = extract_data(
                image_docs,
                query,
                model_name,
                temperature,
                api_key,
            )
        return response