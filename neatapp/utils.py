import uuid
from pathlib import Path

from llama_index.multi_modal_llms.openai import OpenAIMultiModal

from neatapp.constants import STORAGE_DIR


def get_multi_modal_llm(llm_name, model_temperature, openai_api_key, max_new_tokens=1000):
    llm = OpenAIMultiModal(
        model=llm_name,
        temperature=model_temperature,
        api_key=openai_api_key,
        max_new_tokens=max_new_tokens,
    )
    return llm


def generate_unique_path(file_name: str) -> Path:
    """Given the file name, generate a unique file path.

    Args:
        file_name (str): name of the file.

    Returns:
        Path: a unique PosixPath object.
    """
    file_path = Path(STORAGE_DIR, str(uuid.uuid4()), file_name)
    return file_path
