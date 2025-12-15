# Default Configuration

# Memory Settings
use_sqlite_memory = True
sqlite_memory_path = "data/botsmith.db"

local_model = "qwen2.5-coder:7b"
code_model = "qwen2.5-coder:7b"

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
