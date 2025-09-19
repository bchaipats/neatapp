from typing import Sequence
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.core.program import MultiModalLLMCompletionProgram
from llama_index.core.schema import ImageDocument
from neatapp.neatappv2.models import Restaurant

def extract_data_with_llm(
    image_documents: Sequence[ImageDocument],
    prompt: str,
    llm,
) -> Restaurant:
    """Invoke multimodal LLM for data extraction. Returns parsed Restaurant object."""
    program = MultiModalLLMCompletionProgram.from_defaults(
        output_parser=PydanticOutputParser(Restaurant),
        image_documents=image_documents,
        prompt_template_str=prompt,
        multi_modal_llm=llm,
        verbose=True,
    )
    response = program()
    return response