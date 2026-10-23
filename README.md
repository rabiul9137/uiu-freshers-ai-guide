# UIU Freshers AI Guide

An AI-powered information assistant designed to help new students at United International University (UIU), Bangladesh, find university-related information through natural-language questions.

## Live Demo

- **Frontend:** https://uiu-freshers-ai-guide-tc35eyuzemiskadpkfcrpi.streamlit.app/
- **Backend API:** https://uiu-freshers-ai-guide.onrender.com
- **API Documentation:** https://uiu-freshers-ai-guide.onrender.com/docs
- **Health Check:** https://uiu-freshers-ai-guide.onrender.com/health

> This is an independent student project, not an official UIU service.

## Project Overview

Starting university can be challenging for freshers. Students often need information about academic resources, student clubs, counselling services, and university support facilities.

The UIU Freshers AI Guide aims to make this information easier to discover through an AI-powered question-answering application that retrieves information from a curated collection of university-related documents and uses a language model to generate responses.

## Key Features

- Ask questions about UIU in natural language.
- Retrieve relevant information from a curated JSON knowledge base.
- Use lightweight keyword-based document retrieval.
- Generate AI-assisted answers through the Groq API.
- Return source information alongside answers when available.
- Provide fallback responses when the application cannot answer a question reliably.
- Expose backend functionality through a FastAPI REST API.
- Provide a Streamlit-based user interface.
- Run the deployed backend without requiring a GPU.

**Language support:** The project is intended to support English and Bengali queries. Retrieval quality and response accuracy should be tested separately for both languages before claiming full multilingual support.

## Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| Backend API | FastAPI |
| Frontend | Streamlit |
| AI inference | Groq API |
| Language model | Configurable; development configuration uses `openai/gpt-oss-20b` |
| Retrieval | Lightweight keyword-based search |
| Knowledge storage | JSON documents |
| Data collection | Requests and BeautifulSoup |
| Validation | Pydantic |
| Version control | Git and GitHub |
| Backend deployment | Render |
| Frontend deployment | Streamlit Community Cloud |

The deployed lightweight retrieval implementation avoids loading large embedding models and FAISS indexes, helping reduce backend memory requirements.

## Project Structure

```text
uiu-freshers-ai-guide/
├── app/
│   ├── main.py
│   ├── vector_search.py
│   ├── knowledge_base.py
│   ├── scraper.py
│   └── ...
├── data/
│   ├── seed_documents.json
│   └── ...
├── frontend.py
├── add_verified_documents.py
├── test_scraper.py
├── requirements.txt
├── requirements-render.txt
├── .gitignore
└── README.md
```

The exact files may vary as development continues.

## Getting Started

### Prerequisites

- Python 3.11 or a compatible version supported by the project
- Git
- A Groq API key for AI-generated responses

### 1. Clone the repository

```bash
git clone https://github.com/rabiul9137/uiu-freshers-ai-guide.git
cd uiu-freshers-ai-guide
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

On Windows CMD:

```cmd
.venv\Scripts\activate
```

A virtual environment keeps project dependencies separate from other Python projects.

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Use `requirements-render.txt` for the lightweight Render deployment configuration when following the project's deployment setup.

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Replace the placeholder with your own Groq API key.

**Security:**
- Never commit `.env` to GitHub.
- Keep API keys private.
- Configure `GROQ_API_KEY` separately in the environment settings of your deployment service.

### 5. Start the backend

From the project root, run:

```bash
python -m uvicorn app.main:app --reload
```

The backend should be available at:

- API root: http://127.0.0.1:8000/
- Health check: http://127.0.0.1:8000/health
- Interactive API documentation: http://127.0.0.1:8000/docs

### 6. Start the frontend

Open a second terminal in the project directory and activate the virtual environment.

Run:

```bash
python -m streamlit run frontend.py
```

Streamlit normally opens at:

http://localhost:8501

Ensure the frontend is configured to use the correct backend API base URL.

## How It Works

The application follows a retrieval-augmented question-answering workflow.

1. **Question input:** A student submits a question through the Streamlit interface.
2. **Document retrieval:** The backend searches the available university documents using lightweight keyword matching.
3. **Context preparation:** Relevant retrieved documents are selected and prepared as context.
4. **Answer generation:** The configured language model receives the question and available context through the Groq API.
5. **Source reporting:** The API returns an answer and source metadata when available.
6. **Fallback handling:** If the application cannot provide an answer, it may return a fallback response rather than inventing missing university information.

### Retrieval limitations

The current lightweight retrieval implementation is not equivalent to embedding-based semantic search. Questions phrased with different words from the stored documents may fail to retrieve relevant information.

Retrieval quality depends on the content, language, wording, and coverage of the knowledge base.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Basic API information |
| GET | `/health` | Health and configuration status |
| POST | `/ask` | Submit a question to the assistant |

Use the interactive API documentation at `/docs` to inspect the current request schema, submit questions, and examine responses.

Example request body for `/ask`:

```json
{
  "question": "What student clubs are available at UIU?"
}
```

The exact response fields and validation requirements are defined by the deployed API.

## Testing

Test the scraper using:

```bash
python -m pytest test_scraper.py -v
```

If pytest is not installed:

```bash
python -m pip install pytest
```

Recommended manual tests:

- Ask a question covered by the knowledge base.
- Ask a question using different wording from the stored document.
- Test English and Bengali queries separately.
- Ask a question unrelated to UIU and inspect the fallback behavior.
- Check whether returned sources actually support the generated answer.
- Verify that the application behaves appropriately when the Groq API key is missing or the API is unavailable.

## Deployment

The application uses separate frontend and backend deployments.

- **Frontend:** Streamlit Community Cloud
- **Backend:** Render
- **AI inference:** Groq API
- **Secrets:** Environment variables configured in the relevant deployment service

The backend has been deployed on Render using a lightweight dependency configuration to reduce memory consumption.

Render's free instance may spin down after inactivity, so the first request after an idle period may take longer.

Deployment status does not guarantee that every feature is functioning. Health checks, API requests, source relevance, and frontend integration should be tested independently.

## Limitations

- The assistant can only provide reliable information covered by the available knowledge base.
- Keyword-based retrieval may miss semantically related questions with different wording.
- Bengali and English retrieval quality requires separate evaluation.
- University websites may block automated scraping or change their page structure.
- Admission requirements, room numbers, schedules, and other time-sensitive details must be verified against official UIU sources.
- AI-generated answers may contain errors.
- Groq API availability, configuration, and usage limits may affect answer generation.
- The application is not an official UIU service unless formally authorized by the university.

## Future Improvements

- Expand the knowledge base with verified UIU documents.
- Improve retrieval relevance and Bengali-language query handling.
- Evaluate retrieval with a test set of representative questions.
- Improve source ranking and remove irrelevant citations.
- Add document verification dates and update timestamps.
- Add automated tests for retrieval, API behavior, and fallback responses.
- Improve logging, error handling, and monitoring.
- Explore embedding-based semantic retrieval if deployment resources permit.

## Author

**Rabiul Islam**

GitHub: https://github.com/rabiul9137

## License

No license has been specified yet. Until a license is added, reuse and redistribution are subject to applicable copyright law and the repository owner's rights.
