# Research Paper Q&A System

This repository provides a system for extracting information from research papers and answering questions based on their content. It leverages vector embeddings and a Qdrant vector database for efficient information retrieval, combined with a summarization agent to generate concise answers. This system was developed to assist in the process of writing a systematic literature review thesis.

---

## Features

* **PDF Processing**: Automatically ingests PDF documents from a specified directory.
* **Text Embedding**: Converts document chunks into numerical vector representations using `sentence-transformers/all-MiniLM-L6-v2`.
* **Vector Database (Qdrant)**: Stores and retrieves document embeddings for fast similarity searches.
* **Question Answering**: Takes a list of predefined questions and retrieves relevant document snippets.
* **Summary Generation**: Utilizes a `SummaryAgent` to synthesize retrieved information into coherent answers.
* **Output**: Appends generated answers and original questions to an `output.txt` file.
* **Database Management**: Clears the Qdrant database upon completion.

---

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* Python 3.12+
* `pip` (Python package installer)
* Qdrant (follow this [guide](https://qdrant.tech/documentation/quickstart/))
* Google Gemini [API key](https://aistudio.google.com/app/apikey)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Peppe-elefante/AI-SLR.git
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *The requirements.txt file includes:*
    ```
    qdrant_client
    fastembed
    google-generativeai
    docling
    dotenv
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the root directory of your project.
    ```
    GOOGLE_API_KEY = Your google api_key
    QDRANT_URL = your Qdrant URL
    ```

### Usage

1.  **Place your PDF studies:**
    Inside the folder named `Studi` place all the studies needed for your SLR

2.  **Define your questions:**
    Ensure your `utils/questions.py` file contains a list of strings, where each string is a question you want the system to answer. For example:
    ```python
    # utils/questions.py
    questions = [
        "What is the main finding of the first study?",
        "How does the second study approach data analysis?",
        "What are the limitations mentioned in the third paper?"
    ]
    ```

3.  **Run the main script:**
    ```bash
    python main.py
    ```

After execution, the `output.txt` file in the root directory will contain the generated answers for each question.

