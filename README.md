# 🚀 IntelliDocs: LangChain + FastAPI Project

## 📌 Project Overview

This project is a **FastAPI-based** microservice that integrates **LangChain** with a **Streamlit UI** to provide AI-powered document chat functionalities. It is designed to be a complete, containerized solution for chatting with your PDF documents.

## 📂 Project Structure

```bash
.
│── 📄 .dockerignore
│── 📄 .gitignore
│── 📄 Dockerfile
│── 📄 Dockerfile.frontend
│── 📄 README.md
│── 📄 app.py
│── 📄 docker-compose.yml
│── 📄 main.py
│── 📄 requirements.txt
│── 📁 data/
│── 📁 prompt/
│── 📁 tools/
└── 📁 vectorstores/
```

## ⚡ Features

- **FastAPI Backend**: Exposes API endpoints for PDF ingestion and querying.
- **Streamlit Frontend**: A modern, intuitive UI for uploading documents and chatting.
- **LangChain Integration**: Uses Google Gemini via LangChain for processing queries.
- **RAG Pipeline**: Implements Retrieval-Augmented Generation with a FAISS vector store.
- **Fully Containerized**: The entire application is managed via Docker and Docker Compose for easy deployment.

## 📦 Installation

### 🔑 Environment Variables

Create a `.env` file in the project root and add your Google API key:

```ini
GOOGLE_API_KEY=your-google-api-key
```

### 🚀 Deploying with Docker (Recommended)

This is the simplest way to run the entire application.

1.  **Ensure Docker is installed** on your system.
2.  **Clone the repository**:
    ```sh
    git clone https://github.com/your-repo/your-project.git
    cd your-project
    ```
3.  **Build and run the Docker containers**:
    ```sh
    docker-compose up --build
    ```
4.  The application will be accessible at **`http://localhost:8501`**.

### 💻 Running Locally

If you prefer to run the services manually:

1.  **Create a Virtual Environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # For macOS/Linux
    # venv\Scripts\activate    # For Windows
    ```
2.  **Install Dependencies**:
    ```sh
    pip install -r requirements.txt
    ```
3.  **Run the Backend**:
    Open a terminal and run the FastAPI app:
    ```sh
    uvicorn main:app --reload
    ```
4.  **Run the Frontend**:
    Open a second terminal and run the Streamlit app:
    ```sh
    streamlit run app.py
    ```
5. The application will be accessible at **`http://localhost:8501`**.


## 🛠 API Endpoints

The API provides the following endpoints, which are used by the Streamlit frontend:

-   **`POST /upload`**: Uploads a PDF file for ingestion.
    -   **Body**: `multipart/form-data` with a `file` field.
-   **`POST /query`**: Asks a question based on the ingested documents.
    -   **Body**: `application/json` with a `user_query` field.
    -   **Example**: `{"user_query": "What is the main topic of the document?"}`

## 🤝 Contributing

1.  Create a new branch (`git checkout -b feature-branch`).
2.  Commit changes (`git commit -m "Added a new feature"`).
3.  Push to your branch (`git push origin feature-branch`).
4.  Create a pull request.
