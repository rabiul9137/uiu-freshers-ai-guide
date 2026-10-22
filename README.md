\# UIU Freshers AI Guide



An AI-powered information assistant designed to help new students at United International University (UIU), Bangladesh, find useful university-related information through natural-language questions.



\## Project Overview



Starting university can be challenging for freshers. They may need information about academic programs, student clubs, counselling services, and student support resources.



The UIU Freshers AI Guide aims to make this information easier to discover using an AI-powered question-answering system grounded in a curated knowledge base.



\## Key Features



\- Ask questions about UIU in natural language.

\- Retrieve relevant information from a curated collection of documents.

\- Support English and Bengali queries through multilingual semantic retrieval.

\- Generate AI-assisted answers using the Groq API.

\- Use retrieved information to help ground answers in available sources.

\- Provide a safe fallback when relevant information is unavailable.

\- Expose backend endpoints through FastAPI.



\*Features and language support should be validated against the current implementation before the final capstone submission.\*



\## Technology Stack



\- \*\*Language:\*\* Python

\- \*\*Backend API:\*\* FastAPI

\- \*\*Frontend:\*\* Streamlit

\- \*\*AI inference:\*\* Groq API

\- \*\*Language model:\*\* Configurable model; the current development configuration uses `openai/gpt-oss-20b`

\- \*\*Semantic retrieval:\*\* Sentence Transformers

\- \*\*Vector search:\*\* FAISS

\- \*\*Data processing:\*\* JSON, Requests, BeautifulSoup

\- \*\*Version control:\*\* Git and GitHub



\## Project Structure



```text

uiu-freshers-ai-guide/

├── app/

│   ├── main.py

│   ├── vector\_search.py

│   ├── knowledge\_base.py

│   ├── scraper.py

│   └── ...

├── data/

│   ├── seed\_documents.json

│   └── ...

├── frontend.py

├── add\_verified\_documents.py

├── test\_scraper.py

├── requirements.txt

├── .gitignore

└── README.md

```



\## Getting Started



\### Prerequisites



\- Python 3.11 or a compatible Python version

\- Git

\- A Groq API key for AI-generated responses



\### 1. Clone the repository



```bash

git clone https://github.com/rabiul9137/uiu-freshers-ai-guide.git

cd uiu-freshers-ai-guide

```



\### 2. Create a virtual environment



```bash

python -m venv .venv

```



Activate it on Windows CMD:



```cmd

.venv\\Scripts\\activate

```



\### 3. Install dependencies



```bash

python -m pip install --upgrade pip

pip install -r requirements.txt

```



\### 4. Configure environment variables



Create a `.env` file in the project root and configure the API key using the environment variable name expected by the application.



For example, if the application reads `GROQ\_API\_KEY`:



```env

GROQ\_API\_KEY=your\_groq\_api\_key\_here

```



\*\*Security:\*\* Never commit `.env` or publish your API key. Keep `.env` excluded through `.gitignore`.



\### 5. Start the backend



```bash

python -m uvicorn app.main:app --reload

```



Open the interactive API documentation at:



http://127.0.0.1:8000/docs



The backend health endpoint is available at:



http://127.0.0.1:8000/health



\### 6. Start the frontend



Open a second terminal in the project directory, activate the virtual environment, and run:



```bash

python -m streamlit run frontend.py

```



Streamlit normally opens at:



http://localhost:8501



Ensure the frontend's configured API base URL points to the running backend.



\## AI and Retrieval Methodology



The application uses a retrieval-based approach to find relevant information from the local document collection.



1\. \*\*Knowledge base:\*\* University-related information is stored in JSON documents.

2\. \*\*Embedding generation:\*\* Sentence Transformers converts text into vector representations.

3\. \*\*Semantic retrieval:\*\* FAISS searches for relevant document vectors.

4\. \*\*Answer generation:\*\* Retrieved context is used with the configured language model through Groq.

5\. \*\*Fallback behavior:\*\* When relevant information cannot be found, the application can respond that it does not have enough information rather than inventing an answer.



The quality of responses depends on the accuracy, coverage, and freshness of the source documents.



\## API



The backend currently includes these endpoints:



| Endpoint | Purpose |

|---|---|

| `GET /` | Basic API information |

| `GET /health` | Health and configuration status |

| `POST /ask` | Submit a question to the AI assistant |



See `/docs` while the backend is running for the actual request and response schemas.



\## Testing



Run the scraper test with:



```bash

python -m pytest test\_scraper.py -v

```



If `pytest` is not installed, install it in the virtual environment before running the test.



Also manually test questions with known answers and questions for which the knowledge base has no relevant information.



\## Limitations



\- The assistant can only provide reliable information covered by its available sources.

\- University websites may block automated scraping or change their page structure.

\- Room numbers, schedules, admission requirements, and other time-sensitive information must be verified against official university sources.

\- AI-generated answers may still contain errors and should be checked for important decisions.

\- A configured API key and reachable backend are required for the corresponding online AI features.



\## Responsible Use



This project is an informational assistant and is not an official UIU service unless formally authorized by the university. Users should verify important academic and administrative information with official UIU sources.



\## Future Improvements



\- Expand the verified university knowledge base.

\- Improve retrieval quality and Bengali-language query handling.

\- Add source citations and document update timestamps to answers.

\- Deploy the frontend and backend with secure environment-variable configuration.

\- Add automated tests for retrieval, API behavior, and fallback responses.

\- Improve monitoring and error handling.



\## Author



\*\*Rabiul Islam\*\*



GitHub: https://github.com/rabiul9137



\## License



A license has not yet been specified. All rights and permissions remain subject to the repository owner's terms until a license is added.



