from pathlib import Path
import uuid
from pdf2image import convert_from_bytes
from PIL import Image
from neatapp.constants import STORAGE_DIR

class DocumentHandler:
    def get_image(self, uploaded_file):
        if uploaded_file.type == "application/pdf":
            # Take first page only
            image = convert_from_bytes(uploaded_file.read())[0]
        else:
            image = Image.open(uploaded_file).convert("RGB")
        return image

    @staticmethod
    def generate_save_path(file_name):
        file_path = Path(STORAGE_DIR, str(uuid.uuid4()), file_name)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        return file_path