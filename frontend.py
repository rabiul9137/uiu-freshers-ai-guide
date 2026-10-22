
import os

import requests
import streamlit as st


# FastAPI backend endpoint
# Local development uses localhost by default.
# Online deployment can provide API_URL through Streamlit secrets
# or an environment variable.
DEFAULT_API_BASE_URL = "http://127.0.0.1:8000"

try:
    API_BASE_URL = st.secrets.get(
        "API_URL",
        os.getenv("API_URL", DEFAULT_API_BASE_URL),
    )
except Exception:
    API_BASE_URL = os.getenv(
        "API_URL",
        DEFAULT_API_BASE_URL,
    )

API_URL = f"{API_BASE_URL.rstrip('/')}/ask"


# Page configuration
st.set_page_config(
    page_title="UIU Freshers AI Guide",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded",
)


# Custom CSS for a clean interface
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #777777;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Sidebar
with st.sidebar:
    st.title("🎓 UIU Guide")
    st.write("Your AI-powered university information assistant.")
    st.divider()

    st.subheader("Try asking")
    st.markdown(
        "- What undergraduate programs does UIU offer?\n"
        "- Where can I get mental health counselling?\n"
        "- UIU-তে কী কী স্টুডেন্ট ক্লাব আছে?\n"
        "- UIU-এর vision and mission কী?"
    )

    st.divider()

    if st.button("🗑️ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.caption("Prototype version 0.7.0")
    st.caption("Verify important information through official UIU sources.")


# Main heading
st.markdown(
    '<div class="main-title">🎓 UIU Freshers AI Guide</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Welcome to United International University! "
    "Ask questions in English or বাংলা."
    "</div>",
    unsafe_allow_html=True,
)

st.info(
    "This assistant retrieves information from its knowledge base "
    "and uses an AI model to generate answers."
)


# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Helper function to display sources
def display_sources(sources):
    if not sources:
        st.info(
            "No matching source was found in the current knowledge base."
        )
        return

    with st.expander("📚 Sources and relevance scores", expanded=True):
        for source in sources:
            title = source.get("title", "UIU source")
            url = source.get("url", "")
            score = source.get("relevance_score")

            if url.startswith(("https://", "http://")):
                st.markdown(f"- [{title}]({url})")
            else:
                st.markdown(f"- {title}")

            if isinstance(score, (int, float)):
                st.caption(
                    f"Retrieval similarity score: {score:.3f}"
                )


# Display previous conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant":
            if message.get("sources"):
                display_sources(message["sources"])

            if message.get("error"):
                st.warning(message["error"])


# Chat input
question = st.chat_input(
    "Ask about UIU... / UIU সম্পর্কে প্রশ্ন করুন..."
)


if question:
    # Display and store user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # Generate answer through the FastAPI RAG backend
    with st.chat_message("assistant"):
        with st.spinner(
            "Searching UIU documents and generating an answer..."
        ):
            try:
                response = requests.post(
                    API_URL,
                    json={"question": question},
                    timeout=90,
                )

                response.raise_for_status()
                data = response.json()

                answer = data.get(
                    "answer",
                    "Sorry, no answer was returned.",
                )
                sources = data.get("sources", [])
                model = data.get("model")

                st.markdown(answer)

                if sources:
                    display_sources(sources)
                else:
                    st.info(
                        "No matching source was found in the "
                        "current knowledge base."
                    )

                if model:
                    st.caption(f"AI model: {model}")

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sources": sources,
                    }
                )

            except requests.exceptions.Timeout:
                error_message = (
                    "The request took too long. Please try again."
                )

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                        "sources": [],
                        "error": error_message,
                    }
                )

            except requests.exceptions.ConnectionError:
                error_message = (
                    "Cannot connect to the backend. "
                    "Check the backend URL and confirm that "
                    "the FastAPI service is running."
                )

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                        "sources": [],
                        "error": error_message,
                    }
                )

            except requests.exceptions.HTTPError as error:
                error_message = (
                    f"The backend returned an HTTP error: "
                    f"{error.response.status_code}. "
                    "Check the backend service logs and configuration."
                )

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                        "sources": [],
                        "error": error_message,
                    }
                )

            except (ValueError, KeyError):
                error_message = (
                    "Could not process the backend response. "
                    "Please check the FastAPI server."
                )

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                        "sources": [],
                        "error": error_message,
                    }
                )
