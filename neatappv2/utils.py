import uuid
from pathlib import Path
from typing import Optional
from llama_index.multi_modal_llms.openai import OpenAIMultiModal

from neatappv2.constants import STORAGE_DIR


def generate_unique_image_path(original_filename: Optional[str] = None) -> Path:
    """Generate a unique file path in the storage directory with the same extension as the original file"""
    ext = ".png"
    if original_filename and "." in original_filename:
        ext = Path(original_filename).suffix
    unique_name = f"{uuid.uuid4()}{ext}"
    return STORAGE_DIR / unique_name


def get_multimodal_llm(llm_name: str, temperature: float, api_key: str) -> OpenAIMultiModal:
    """Instantiate an OpenAI multimodal LLM"""
    return OpenAIMultiModal(
        model_name=llm_name,
        temperature=temperature,
        openai_api_key=api_key,
        max_new_tokens=1000,
    )