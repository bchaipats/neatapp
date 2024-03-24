from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.core.program import MultiModalLLMCompletionProgram

from neatapp.models import Restaurant
from neatapp.utils import get_multi_modal_llm


def extract_data(image_documents, data_extract_str, llm_name, model_temperature, api_key):
    llm = get_multi_modal_llm(llm_name, model_temperature, api_key, max_new_tokens=1000)
    openai_program = MultiModalLLMCompletionProgram.from_defaults(
        output_parser=PydanticOutputParser(Restaurant),
        image_documents=image_documents,
        prompt_template_str=data_extract_str,
        multi_modal_llm=llm,
        verbose=True,
    )
    json_response = openai_program()
    return json_response
