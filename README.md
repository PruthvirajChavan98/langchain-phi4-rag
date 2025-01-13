# langchain-phi4-rag


# Document Chatbot Using RAGPipeline and Phi-4

This project is a PDF-based document chatbot that allows users to interact with their uploaded PDF documents using natural language queries. It leverages Retrieval-Augmented Generation (RAG) methodology to retrieve relevant information from documents and generate answers using a state-of-the-art language model.

---

## Features

1. **PDF Upload and Processing**:
   - Users can upload PDF files via a Streamlit frontend.
   - The backend processes the document, splits it into smaller chunks, and stores embeddings for efficient retrieval.

2. **Chat Interface**:
   - Users can ask questions about the uploaded PDF through a chat interface.
   - Responses are streamed in real-time from the backend.

3. **Retrieval-Augmented Generation (RAG)**:
   - The RAGPipeline combines document retrieval and a language model to provide accurate, contextually relevant answers.

4. **Storage and Metadata**:
   - Pipeline metadata (e.g., PDF name, vector store path) is stored in an SQLite database for future reference.

---

## Key Components

### **Language Model**
- **LLM**: The application uses **Phi-4**, a large language model from Ollama. Phi-4 is known for its advanced conversational and reasoning capabilities, which make it suitable for complex question-answering tasks.

### **Embeddings**
- **Embedding Model**: The `nomic-embed-text` model from Ollama is used to generate dense vector representations of document chunks. These embeddings enable efficient similarity-based retrieval.

### **RAGPipeline**
The RAGPipeline class is the core of this application. It integrates the following components:
- **PDF Parsing**: Extracts text from PDF files using `PDFPlumberLoader`.
- **Text Splitting**: Splits the document into smaller, manageable chunks using `RecursiveCharacterTextSplitter`.
- **Vector Store**: Creates a Chroma vector store for storing and retrieving document embeddings.
- **QA Chain**: 
  - Uses a predefined RAG prompt template.
  - Retrieves relevant document chunks and combines them with the user’s question.
  - Generates a response using the Phi-4 model.
  - Provides real-time streaming responses.

---

## Tech Stack

### Backend
- **FastAPI**: Serves as the backend for handling file uploads, document processing, and question-answering requests.
- **SQLite**: Used to store metadata about uploaded PDFs and vector stores.
- **LangChain**: Manages the RAG pipeline and facilitates integration with LLMs.

### Frontend
- **Streamlit**: Provides an intuitive chat interface for interacting with the backend.
- **Bootstrap Sidebar**: Enables easy PDF uploading and management.

### Vector Store
- **Chroma**: A high-performance vector database for efficient document retrieval.

---

## How It Works

1. **Upload a PDF**:
   - The user uploads a PDF file through the Streamlit sidebar.
   - The PDF is processed, split into chunks, and stored as embeddings in a Chroma vector store.

2. **Ask Questions**:
   - Users type questions in the chat interface.
   - The RAGPipeline retrieves relevant document chunks based on the embeddings and combines them with the user query.
   - Phi-4 generates a response, which is streamed back to the user in real time.

3. **Pipeline Metadata**:
   - Metadata for each uploaded PDF is stored in SQLite, allowing the backend to reuse previously created pipelines.

---

## Usage

### Running the PHI-4 LLM on Ollama

1. **Install Ollama**:
   Follow the installation instructions from [Ollama's official website](https://ollama.com).

2. **Download the PHI-4 Model**:
   ```bash
   ollama pull phi4
   ```

3. **Run the Model**:
   ```bash
   ollama run phi4
   ```

### Running the Application

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/PruthvirajChavan98/langchain-phi4-rag.git
   cd langchain-phi4-rag
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Backend**:
   ```bash
   uvicorn main:app --reload
   ```

4. **Run the Frontend**:
   ```bash
   streamlit run app.py
   ```

5. **Access the Application**:
   Open your browser and go to [http://127.0.0.1:8501](http://127.0.0.1:8501).


Future Improvements
	•	Multi-Document Support: Extend the application to allow querying across multiple PDFs.
	•	Advanced Analytics: Add features to visualize insights and trends from documents.
	•	Authentication: Implement user authentication to restrict access to uploaded documents.

License

This project is licensed under the MIT License. See the LICENSE file for details.

