# Neatapp Codebase Overview

## Introduction
Neatapp is an application that allows users to upload images or PDF files, extract structured data from them using multimodal large language models (LLMs), and store the results into a PostgreSQL database. The app is designed for extracting data from advertising media (e.g., restaurant promos) and is powered by OpenAI's GPT-4 Vision and LlamaIndex for intelligent extraction.

---

## Project Structure

```
neatapp/
├── data/                # Example data (images and PDFs)
├── migrations/          # Database setup scripts
├── neatapp/             # Main application package
│   ├── app.py           # Streamlit app – main user interface
│   ├── constants.py     # Query and app-wide config constants
│   ├── data.py          # Data extraction logic
│   ├── db.py            # Database logic for storing/loading data
│   ├── main.py          # CLI entry point (optional)
│   ├── models.py        # (Placeholder) for data models
│   ├── utils.py         # Helper functions
├── notebooks/           # Experiments and utility scripts
├── Makefile             # Build automation (if needed)
├── README.md            # User and setup instructions
├── OVERVIEW.md          # (You are here) Architectural overview
├── poetry.lock, pyproject.toml # Dependency management
├── setup-db.sh          # DB initialization script
```

---

## Key Components

### Streamlit App (`app.py`)
- The main user interface for interacting with the app.
- Lets users upload images or PDFs.
- Shows extracted data, enables confirmation and insertion to DB.
- Tabs for model setup, upload/extract, and viewing saved records.

### Data Extraction (`data.py`)
- Handles AI backend for extracting data from uploaded files.
- Uses OpenAI's `gpt-4-vision-preview` for powerful vision-language understanding.
- Integrates LlamaIndex and `pdf2image` (for converting PDF pages to images).

### Database Handling (`db.py`)
- Functions for connecting to and interacting with the PostgreSQL DB.
- Inserts extracted payloads and maintains a record of file paths and data.
- Provides retrieval as DataFrames for display in Streamlit.

### Utility and Support
- `constants.py`: Shared constants and default extraction queries.
- `utils.py`: Miscellaneous helpers (e.g., for file naming/handling).
- `models.py`: (Placeholder) For defining types or ORM models if extended.

### Data & Notebooks
- `data/`: Contains sample restaurant advertising images and PDFs for demo/testing.
- `notebooks/`: Jupyter notebooks for experimentation, pre/post-processing.

---

## Workflow
1. **User loads Streamlit app** (`app.py`), sets up LLM credentials.
2. **Uploads** an image or PDF file.
3. File is processed:
   - PDF: First page is converted to image with `pdf2image`.
   - Image sent to LLM for extraction using predefined (or user-edited) query.
4. Result is displayed. User can confirm insertion into the database.
5. Saved extractions can be viewed in-app (retrieved as DataFrames).

---

## Extending the App
- Add new extraction queries in `constants.py`.
- Integrate additional models or extraction logic in `data.py`.
- Enhance data schema via `models.py` and migration scripts.
- Customize UX by editing `app.py` (Streamlit interface).

---

## Requirements & Setup
- Python 3.9+, Streamlit, Poetry, PostgreSQL, OpenAI API key.
- See `README.md` for installation and environment setup instructions.

---

## Limitations
- Only processes one file at a time.
- PDFs: Only the first page is considered.

---

For more details, see `README.md` or each individual module's docstrings and inline comments.