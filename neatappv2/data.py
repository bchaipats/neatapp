from typing import Sequence, Dict
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.core.program import MultiModalLLMCompletionProgram
from llama_index.core.schema import ImageDocument

from neatappv2.models import Restaurant
from neatappv2.utils import get_multi_modal_llm


class LLMClient:
    def __init__(self, llm_name: str, temperature: float, api_key: str):
        self.llm_name = llm_name
        self.temperature = temperature
        self.api_key = api_key
        self.llm = self._init_llm()

    def _init_llm(self):
        return get_multi_modal_llm(self.llm_name, self.temperature, self.api_key)

    def query(self, image_documents: Sequence[ImageDocument], prompt: str) -> Dict:
        program = MultiModalLLMCompletionProgram.from_defaults(
            output_parser=PydanticOutputParser(Restaurant),
            image_documents=image_documents,
            prompt_template_str=prompt,
            multi_modal_llm=self.llm,
            verbose=True,
        )
        return program()


class DataExtractor:
    def __init__(self, llm_client: LLMClient, prompt: str):
        self.llm_client = llm_client
        self.prompt = prompt

    def extract(self, image_documents: Sequence[ImageDocument]) -> Dict:
        return self.llm_client.query(image_documents, self.prompt)