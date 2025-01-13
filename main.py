from fastapi import FastAPI, UploadFile, File
from starlette.responses import StreamingResponse
from langchain_ollama import ChatOllama, OllamaEmbeddings
from pydantic import BaseModel, Field
from RAGPipeline import RAGPipeline
from utility import get_pipeline_metadata, store_pipeline_metadata, save_pdf, init_db

# Initialize FastAPI application
app = FastAPI()

# Initialize embeddings and LLM
ollama_embeddings = OllamaEmbeddings(model="nomic-embed-text")

llm = ChatOllama(
    model="phi4",
    temperature=0,
    verbose=True
)

# Pydantic models
class AskQuestionRequest(BaseModel):
    """Query parameters for asking a question about an uploaded PDF."""
    question: str = Field(..., description="The question to ask about the PDF.")
    pdf_name: str = Field(..., description="The name of the previously uploaded PDF.")

# Database initialization
init_db()

# API endpoints
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    pdf_name = file.filename
    print(f"Uploaded PDF name: {pdf_name}")

    # Save PDF and initialize RAGPipeline
    pdf_path = save_pdf(file)
    vectorstore_path = f"./vectorstore_{pdf_name}"
    pipeline = RAGPipeline(
        llm=llm,
        embeddings=ollama_embeddings,
        pdf_path=pdf_path,
        vectorstore_path=vectorstore_path
    )

    # Store metadata in SQLite
    store_pipeline_metadata(pdf_name, pdf_path, vectorstore_path)

    return {"message": f"Uploaded and processed {pdf_name} successfully."}

@app.post("/ask")
async def ask_question(params: AskQuestionRequest):
    pdf_name = params.pdf_name
    print(f"Requested PDF name: {pdf_name}")

    # Retrieve metadata
    metadata = get_pipeline_metadata(pdf_name)
    if not metadata:
        return {"error": "No pipeline found for the provided PDF name."}

    pdf_path, vectorstore_path = metadata

    # Recreate RAGPipeline
    pipeline = RAGPipeline(
        llm=llm,
        embeddings=ollama_embeddings,
        pdf_path=pdf_path,
        vectorstore_path=vectorstore_path
    )

    return StreamingResponse(pipeline.generate_stream(params.question), media_type="text/event-stream")
