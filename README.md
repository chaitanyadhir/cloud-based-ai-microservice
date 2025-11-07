# 🚀 LangChain + FastAPI Project

## 📌 Project Overview

This project is a **FastAPI-based** microservice that integrates **LangChain** with various modules to provide AI-powered functionalities. It is designed to be modular, supporting different use cases such as document processing and question answering.

## 📂 Project Structure

```bash
langchain-project/
│── data/                     # Data storage for vectorstores
│── prompt/                   # Prompt templates for LLMs
│   └── main_prompt.txt
│── tools/                    # Custom tools for handling various functionalities
│   ├── generating_response.py
│   ├── llm_call.py
│   ├── processing_doc.py
│   └── retrieval.py
│── vectorstores/             # FAISS vectorstores
│── .gitignore                # Git ignore file
│── main.py                   # FastAPI main entry point
│── README.md                 # Project documentation
│── requirements.txt          # Python dependencies
```

## ⚡ Features

- **FastAPI Backend**: Exposes API endpoints for PDF ingestion and querying.
- **LangChain Integration**: Uses Google Gemini for processing queries.
- **PDF Processing**: Ingests PDF files, splits them into chunks, and stores them in a FAISS vectorstore.
- **Question Answering**: Answers questions based on the ingested PDF documents.

## 📦 Installation (Running Locally)

### 1️⃣ Clone the Repository

```sh
git clone -b intial-project https://github.com/chaitanyadhir/cloud-based-ai-microservice.git
cd cloud-based-ai-microservice
```

### 2️⃣ Create a Virtual Environment

```sh
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate    # For Windows
```

### 3️⃣ Install Dependencies

```sh
pip install -r requirements.txt
```

## 🔑 Environment Variables

Create a `.env` file in the project root and add:

```ini
GOOGLE_API_KEY=your-google-api-key
```

## 4️⃣ Running the Application Locally

Using `uvicorn`:

```sh
uvicorn main:app --reload
```

## 🚀 Deploying on a Server Using Docker

To deploy the application on a server, follow these steps:

1. **Ensure Docker is installed** on the server:
   ```sh
   sudo apt update && sudo apt install docker.io -y
   ```
2. **Clone the repository**:
   ```sh
   git clone -b intial-project https://github.com/chaitanyadhir/cloud-based-ai-microservice.git
   cd cloud-based-ai-microservice
   ```
3. **Build and run the Docker container**:
   ```sh
   docker build -t langchain-app .
   docker run -d --name langchain-module -p 8000:8000 langchain-app
   ```
4. The application will be accessible at `http://your-server-ip:8000`.

### Redeployment (After Code Updates)
1. **Pull the latest code**:
   ```sh
   git pull origin intial-project
   ```
2. **Stop and remove the existing container**:
   ```sh
   docker stop langchain-module
   docker rm langchain-module
   ```
3. **Rebuild the Docker image**:
   ```sh
   docker build --no-cache -t langchain-app .
   ```

4. **Run the updated container**:
   ```sh
   docker run -d --name langchain-module -p 8000:8000 langchain-app
   ```

## 🛠 API Endpoints

The API provides the following endpoints:

- **`POST /upload`**: Uploads a PDF file for ingestion.
  - **Body**: `multipart/form-data` with a `file` field containing the PDF file.
- **`POST /query`**: Asks a question based on the ingested documents.
  - **Body**: `application/json` with a `user_query` field.
  - **Example**: `{"user_query": "What is the main topic of the document?"}`

## 🤝 Contributing

1. Create a new branch (`git checkout -b feature-branch`).
2. Commit changes (`git commit -m "Added a new feature"`).
3. Push to your branch (`git push origin feature-branch`).
4. Create a pull request.
