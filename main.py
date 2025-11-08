from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from fastapi.responses import JSONResponse
from loguru import logger

from tools.processing_doc import PDFIngestionPipelineFAISS
from tools.generating_response import response_generate

app = FastAPI(title="PDF -> FAISS Upload and Query")

pipeline = PDFIngestionPipelineFAISS()  # uses local HuggingFace embeddings and FAISS-CPU
response_generator = response_generate()

@app.post("/upload")
async def upload(
    file: UploadFile = File(..., description="PDF to ingest"),
):
    logger.info(f"Uploading file: {file.filename}")
    if file.content_type not in ("application/pdf",):
        logger.error(f"Unsupported file type: {file.content_type}")
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    try:
        file_bytes = await file.read()
        # Use filename as namespace; or a default, since the pipeline expects a namespace
        namespace = "default"
        result = pipeline.ingest(
            file_bytes=file_bytes,
            filename=file.filename,
            namespace=namespace,
        )
        response_generator.reload_retriever_db()  # Reload the vector store
        logger.info(f"File uploaded and ingested successfully: {file.filename}")
        return JSONResponse(result)
    except Exception as e:
        logger.error(f"Error during file upload: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/query")
async def query(user_query: str = Body(..., embed=True)):
    logger.info(f"Received query: {user_query}")
    try:
        response = response_generator.query_response(user_query)
        logger.info(f"Generated response for query: {user_query}")
        return JSONResponse({"response": response})
    except Exception as e:
        logger.error(f"Error during query processing: {e}")
        raise HTTPException(status_code=500, detail=str(e))

