import os
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

class RAGPipeline:
    def __init__(self, llm, embeddings, pdf_path, vectorstore_path="./vectorstore"):
        """
        Initializes the RAGPipeline class with the necessary components
        for processing PDFs and generating answers.

        Args:
            llm: The language model to be used for answering questions.
            embeddings: The embedding model to create vector representations of documents.
            pdf_path: Path to the PDF file to process.
            vectorstore_path: Directory to store the vectorized document representations.
        """
        self.llm = llm
        self.ollama_embeddings = embeddings
        self.pdf_path = pdf_path
        self.vectorstore_path = vectorstore_path

        # Predefined prompt from the hub
        self.prompt = hub.pull("rlm/rag-prompt")

        # Load (or create) vectorstore
        self.vectorstore = self._load_or_create_vectorstore()

        # Define how to format retrieved documents before feeding them into LLM
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        # Define the QA chain
        self.qa_chain = (
            {
                "context": self.vectorstore.as_retriever() | format_docs,
                "question": RunnablePassthrough(),
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def _load_or_create_vectorstore(self):
        """
        If the vectorstore directory exists and is non-empty,
        load the existing store. Otherwise, read PDF, chunk it,
        and create a new one.
        """
        if (
            os.path.exists(self.vectorstore_path)
            and os.path.isdir(self.vectorstore_path)
            and os.listdir(self.vectorstore_path)
        ):
            print(f"[RAGPipeline] Loading existing index from: {self.vectorstore_path}")
            return Chroma(
                persist_directory=self.vectorstore_path,
                embedding_function=self.ollama_embeddings
            )

        print("[RAGPipeline] No existing index found; creating a new one...")

        # If no existing index, read and chunk the PDF, then create/persist the new index.
        loader = PDFPlumberLoader(self.pdf_path)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=0
        )
        all_splits = splitter.split_documents(docs)

        return Chroma.from_documents(
            documents=all_splits,
            embedding=self.ollama_embeddings,
            persist_directory=self.vectorstore_path
        )

    async def generate_stream(self, question: str):
        """
        Generates a streaming response for the given question.
        """
        stream = self.qa_chain.astream_events(question, version="v2")
        async for event in stream:
            if event["event"] == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    yield content
