from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.absolute()
STORAGE_DIR = Path(ROOT_DIR, "mocked_storage")

DATA_EXTRACT_STR = """\
can you summarize what is in the image
and return the answer with json format
"""

EXAMPLE_RESPONSE = {
    "restaurant": "Not Specified",
    "food": "8 Wings or Chicken Poppers",
    "discount": "Black Friday Offer",
    "price": "$8.73",
    "rating": "Not Available",
    "review": "Not Available",
}