from llama_index.multi_modal_llms.openai import OpenAIMultiModal


def get_multi_modal_llm(llm_name, model_temperature, openai_api_key, max_new_tokens=1000):
    llm = OpenAIMultiModal(
        model=llm_name,
        temperature=model_temperature,
        api_key=openai_api_key,
        max_new_tokens=max_new_tokens,
    )
    return llm
