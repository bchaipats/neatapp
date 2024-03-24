# neatapp

## Prerequisite

- Python 3.9.16

## Setup

### Mac
We'll be using [`pdf2image`](https://github.com/Belval/pdf2image) library to convert a PDF into image so that we can reuse the same data extraction process for both PDF and image.

To use `pdf2image`, Mac users will have to install poppler.

Installing using Brew:
```bash
brew install poppler
```

### Windows & Linux

For Windows & Linux users, please check out the installation instruction of poppler from the [pdf2image GitHub repository](https://github.com/Belval/pdf2image?tab=readme-ov-file#how-to-install)

### API keys

We'll need OpenAI to access GPT-4V multimodal LLM `(gpt-4-vision-preview)`. Make sure to create an OpenAI account and generate an API key.

### Repository
```bash
git clone https://github.com/bchaipats/neatapp.git .
git config --global user.name <GITHUB-USERNAME>
git config --global user.email <EMAIL-ADDRESS>
```

### Environment
Set up the environment by specifying `OPENAI_API_KEY` and `DB_CONNECTION_STRING` in your `.env` file, and installing the dependencies:
```bash
python -m venv .venv
source .venv/bin/activate
pip instal poetry
poetry install
export PYTHONPATH=$PYTHONPATH:$PWD
pre-commit install
pre-commit autoupdate
```

### Credentials
```bash
touch .env
# Add environment variables to .env
OPENAI_API_KEY=""  # https://platform.openai.com/account/api-keys
DB_CONNECTION_STRING="dbname=postgres user=postgres host=localhost password=postgres"
source .env
```

### Database
We'll be using PostgreSQL database to store extracted json payloads and image paths. After installing PostgreSQL and start the service, execute the `setup-db.sh` script to initialize a table before using the app:
```bash
./setup-db.sh
```

### Run Streamlit app
Now we're ready to test the app!
```bash
streamlit run neatapp/app.py
```
