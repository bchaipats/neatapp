from pathlib import Path

# Directory for storing uploaded images
ROOT_DIR = Path(__file__).parent.parent.absolute()
STORAGE_DIR = Path(ROOT_DIR, "storage")
STORAGE_DIR.mkdir(exist_ok=True)

# Prompt for data extraction
DATA_EXTRACT_PROMPT = """
Please analyze the content of the image and provide a summary in JSON format.
"""

# Example response for testing
EXAMPLE_RESPONSE = {
    "restaurant": "Not Specified",
    "food": "Not Specified",
    "discount": "N/A",
    "price": "N/A",
    "rating": "N/A",
    "review": "N/A"
}