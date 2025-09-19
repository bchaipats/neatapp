import uuid
from pathlib import Path
from llama_index.multi_modal_llms.openai import OpenAIMultiModal
from neatapp.neatappv2.config import AppConfig

def generate_unique_path(file_name: str) -> Path:
    """Generate unique path for an upload."""
    return AppConfig.STORAGE_DIR / str(uuid.uuid4()) / file_name

def build_openai_multimodal(
    llm_name: str,
    temperature: float,
    api_key: str,
    max_new_tokens: int = 1000
):
    return OpenAIMultiModal(
        model=llm_name,
        temperature=temperature,
        api_key=api_key,
        max_new_tokens=max_new_tokens,
    )