# Research Topic Processor

This application allows users to input a research topic via a Streamlit frontend, which sends the topic to a FastAPI backend for processing. The backend uses the `react_agent` function (powered by Groq and Exa APIs) to generate a report, captures the output, and returns it to the frontend for display.

## Features
- **Streamlit Frontend**: A simple web interface for entering a research topic and viewing the generated report.
- **FastAPI Backend**: Handles topic processing and report generation, capturing print statements for display.
- **API Integration**: Uses Groq and Exa APIs to process research topics (assumes `react_agent` implementation).
- **Error Handling**: Validates input and handles server connection issues.

## Project Structure
```
research-topic-processor/
├── app.py              # FastAPI backend
├── streamlit_app.py    # Streamlit frontend
├── .env                # Environment variables (API keys)
├── config/             # Configuration module (assumed)
│   └── config.py
├── agent/              # Agent module (assumed)
│   └── agents.py
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Prerequisites
- Python 3.8+
- A Groq API key (sign up at [x.ai](https://x.ai/api))
- An Exa API key (sign up at [exa.ai](https://exa.ai))
- Git (optional, for cloning)

## Setup
1. **Clone the Repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd research-topic-processor
   ```

2. **Install Dependencies**:
   Create a virtual environment and install required packages:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install fastapi uvicorn streamlit requests groq exa_py python-dotenv nest_asyncio
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the project root with your API keys and model:
   ```plaintext
   GROQ_API_KEY=your_groq_api_key
   EXA_API_KEY=your_exa_api_key
   MODEL=your_model_name
   ```
   Replace `your_groq_api_key`, `your_exa_api_key`, and `your_model_name` with actual values.

4. **Verify Modules**:
   Ensure the `config.config` and `agent.agents` modules (containing `react_agent`) are available in the `config/` and `agent/` directories, respectively. Update `app.py` if these are located elsewhere.

## Running the Application
1. **Start the FastAPI Backend**:
   In a terminal, navigate to the project directory and run:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8008 --reload
   ```
   - The server will be available at `http://localhost:8008`.
   - The `--reload` flag enables auto-restart during development.

2. **Start the Streamlit Frontend**:
   In a separate terminal, run:
   ```bash
   streamlit run streamlit_app.py
   ```
   - The app will open in your browser at `http://localhost:8501`.

3. **Use the Application**:
   - Enter a research topic (e.g., "AI ethics") in the Streamlit interface.
   - Click "Get Print Statements" to send the topic to the backend.
   - View the generated report in the browser.

## Troubleshooting
- **"Error connecting to the backend server"**:
  - Ensure the FastAPI server is running (`http://localhost:8008`).
  - Test the endpoint: `curl -X POST http://localhost:8008/get_prints -H "Content-Type: application/json" -d '{"text":"test"}'`.
  - Check for port conflicts: `lsof -i :8008` (macOS/Linux) or `netstat -ano | findstr :8008` (Windows). Use a different port (e.g., 8009) if needed.
- **"Attribute 'app' not found in module"**:
  - Ensure the FastAPI file is named `app.py` and run `uvicorn app:app`.
  - If using `main.py`, run `uvicorn main:app`.
- **API Key Errors**:
  - Verify `.env` file exists and is loaded (check `app.py` for `python-dotenv` usage).
- **Dependency Issues**:
  - Reinstall dependencies: `pip install -r requirements.txt`.
  - Ensure `config.config` and `agent.agents` are correctly implemented.

## Notes
- **Security**: Keep API keys in `.env` and avoid committing it to version control (add `.env` to `.gitignore`).
- **Development**: Use `--reload` with Uvicorn for auto-restart during development.
- **Production**: Run FastAPI with a production server (e.g., `gunicorn`) and consider Docker for deployment.
- **Custom Modules**: The `react_agent` function and `config.config` are assumed to be provided. Update paths or imports if they differ.

## License
This project is unlicensed. Use and modify as needed for personal or educational purposes.

## Contact
For issues or questions, open an issue on the repository or contact the project maintainer.