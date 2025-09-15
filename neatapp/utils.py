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
        openai_api_key (str): an OPENAI API key
        max_new_tokens (int, optional): maximum new tokens to generate. Defaults to 1000.

    Returns:
        OpenAIMultiModal: OpenAIMultiModal instance
    """
    return OpenAIMultiModal(
        llm_name=llm_name,
        model_temperature=model_temperature,
        openai_api_key=openai_api_key,
        max_new_tokens=max_new_tokens,
    )


def hello_world():
    """Prints hello world"""
    print("hello_world")