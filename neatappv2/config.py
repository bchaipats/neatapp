from pathlib import Path

class AppConfig:
    # Directories
    ROOT_DIR = Path(__file__).parent.parent.absolute()
    STORAGE_DIR = ROOT_DIR / 'data' / 'storage'
    
    # Model defaults
    DEFAULT_LLM = 'gpt-4-vision-preview'
    DEFAULT_TEMPERATURE = 0.0
    DATA_EXTRACT_PROMPT = (
        "can you summarize what is in the image "
        "and return the answer in json format"
    )