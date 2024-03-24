import uuid
from pathlib import Path

from llama_index.multi_modal_llms.openai import OpenAIMultiModal

from neatapp.constants import STORAGE_DIR


def get_multi_modal_llm(
    llm_name: str, model_temperature: int, openai_api_key: str, max_new_tokens: int = 1000
) -> OpenAIMultiModal:
    """Create a multimodal LLM from OpenAI

    Args:
        llm_name (str): name of the OpenAI GPT model
        model_temperature (int): model temperature ranging from 0-1
        openai_api_key (str): an OPENAI_API_KEY used to authenticate with the OpenAI platform
        max_new_tokens (int, optional): number of maximum tokens generated. Defaults to 1000.

    Returns:
        OpenAIMultiModal: _description_
    """
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
