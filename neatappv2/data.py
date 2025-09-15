from typing import List, Dict
from PIL import Image
from llama_index.core.schema import ImageDocument
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.core.program import MultiModalLLMCompletionProgram

from neatappv2.models import Restaurant


def extract_data(images: List[Image.Image], prompt: str, llm) -> Dict:
    """Extract data from images using multimodal LLM

    Args:
        images (List[Image.Image]): List of images to analyze
        prompt (str): Prompt to guide data extraction
        llm: a multimodal LLM instance

    Returns:
        Dict: extracted data parsed to dictionary
    """

    image_docs = [ImageDocument.from_pil_image(img) for img in images]

    output_parser = PydanticOutputParser(pydantic_object=Restaurant)

    program = MultiModalLLMCompletionProgram(llm=llm, output_parser=output_parser, prompt=prompt)

    response = program.invoke(image_docs)

    return response