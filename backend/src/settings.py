import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / '.env')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PERPLEXITY_KEY = os.getenv('PERPLEXITY_KEY')
WEB_URL = os.getenv('WEB_URL')

print(OPENAI_API_KEY)
print(PERPLEXITY_KEY)
