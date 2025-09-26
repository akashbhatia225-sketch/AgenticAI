import io
import sys
from fastapi import FastAPI
from contextlib import redirect_stdout
import logging
from groq import Groq
from exa_py import Exa
from config.config import GROQ_API_KEY, EXA_API_KEY, MODEL
from agent.agents import react_agent

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize clients
client = Groq(api_key=GROQ_API_KEY)
exa = Exa(api_key=EXA_API_KEY)
MODEL = MODEL

# FastAPI app
app = FastAPI()

# Function to capture print statements
def capture_prints(topic):
    if not topic.strip():
        return "Error: Topic cannot be empty"
    if not GROQ_API_KEY or not EXA_API_KEY:
        return "Error: API keys are not configured"
    output = io.StringIO()
    with redirect_stdout(output):
        try:
            report = react_agent(client, MODEL, exa, topic, max_steps=4, pause=1.0)
            print("Final Report")
            print(report)
        except Exception as e:
            print(f"Error processing topic: {str(e)}")
    return output.getvalue()

# FastAPI endpoint
@app.post("/get_prints")
async def get_prints(data: dict):
    topic = data.get("text", "")
    logger.info(f"Received topic: {topic}")
    return {"prints": capture_prints(topic).split('\n')}