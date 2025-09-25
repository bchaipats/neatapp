class Config:
    def __init__(self):
        self.api_key = ""
        self.llm_models = ["gpt-4-vision-preview"]
        self.default_llm_index = 0
        self.llm_model = self.llm_models[self.default_llm_index]
        self.model_temperature = 0.5
        self.prompt = (
            "can you summarize what is in the image and return the answer with json format"
        )