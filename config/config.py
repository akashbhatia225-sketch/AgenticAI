from dotenv import load_dotenv

import os


load_dotenv()


GROQ_API_KEY = os.getenv('Groq_API_KEY')
EXA_API_KEY = os.getenv('EXA_API_KEY')
MODEL = "llama-3.1-8b-instant"