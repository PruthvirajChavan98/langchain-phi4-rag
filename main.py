from fastapi import FastAPI, UploadFile, File
from starlette.responses import StreamingResponse
from pydantic import BaseModel, Field

from langchain_ollama import ChatOllama, OllamaEmbeddings

from RAGPipeline import RAGPipeline
from utility import get_pipeline_metadata, store_pipeline_metadata, save_pdf, init_db

# Create FastAPI app
app = FastAPI()

# Initialize embeddings and LLM just once
ollama_embeddings = OllamaEmbeddings(model="nomic-embed-text")

llm = ChatOllama(model="phi4", temperature=0, streaming=True)


# Pydantic model
class AskQuestionRequest(BaseModel):
    question: str = Field(..., description="Question about the PDF.")
    pdf_name: str = Field(..., description="Name of the previously uploaded PDF.")

# Initialize database
init_db()

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # Save the incoming PDF locally
    pdf_name = file.filename
    pdf_path = save_pdf(file)

    # Unique directory for this PDF's vectorstore
    vectorstore_path = f"./vectorstore_{pdf_name}"

    # Instantiate RAGPipeline (creates or loads Chroma index)
    pipeline = RAGPipeline(
        llm=llm,
        embeddings=ollama_embeddings,
        pdf_path=pdf_path,
        vectorstore_path=vectorstore_path
    )

    # Store references in our DB
    store_pipeline_metadata(pdf_name, pdf_path, vectorstore_path)

    return {"message": f"Uploaded and processed {pdf_name} successfully."}

@app.post("/ask")
async def ask_question(params: AskQuestionRequest):
    # Look up the PDF's metadata from our DB
    metadata = get_pipeline_metadata(params.pdf_name)
    if not metadata:
        return {"error": "No pipeline found for the provided PDF name."}

    pdf_path, vectorstore_path = metadata

    # Re-initialize RAGPipeline (will load an existing index if found)
    pipeline = RAGPipeline(
        llm=llm,
        embeddings=ollama_embeddings,
        pdf_path=pdf_path,
        vectorstore_path=vectorstore_path
    )

    # Send back a streaming response
    return StreamingResponse(
        pipeline.generate_stream(params.question),
        media_type="text/event-stream"
    )
