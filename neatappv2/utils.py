import uuid
from pathlib import Path
from llama_index.multi_modal_llms.openai import OpenAIMultiModal
from neatappv2.constants import STORAGE_DIR


def get_multi_modal_llm(llm_name: str, temperature: float, api_key: str, max_new_tokens=1000):
    return OpenAIMultiModal(
        model=llm_name,
        temperature=temperature,
        api_key=api_key,
        max_new_tokens=max_new_tokens,
    )


def generate_unique_path(file_name: str) -> Path:
    return Path(STORAGE_DIR, str(uuid.uuid4()), file_name)