import os
import warnings
from dotenv import load_dotenv
import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.document_loaders import CSVLoader
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Load environment variables
load_dotenv()
warnings.filterwarnings("ignore")

# Load and preprocess sales data
def load_and_preprocess_data(file_path):
    loader = CSVLoader(file_path=file_path)
    documents = loader.load()

    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)
    
    return docs

# Create FAISS vector store with Ollama embeddings
def setup_vector_store(docs):
    embeddings = OllamaEmbeddings(model='nomic-embed-text', base_url="http://localhost:11434")
    
    # Initialize FAISS index
    sample_vector = embeddings.embed_query("sample text")  # Get vector dimension
    index = faiss.IndexFlatL2(len(sample_vector))
    
    vector_store = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={}
    )
    
    vector_store.add_documents(docs)
    return vector_store

# Create RAG Chain
def create_rag_chain(retriever):
    prompt = """
        You are a sales data analyst. Use the retrieved context to answer the query.
        If you don't know the answer, say you don't know.
        Question: {question} 
        Context: {context} 
        Answer:
    """
    # model = ChatOllama(model="deepseek-r1:1.5b", base_url="http://localhost:11434")
    model = ChatOllama(model="llama3.2", base_url="http://localhost:11434")
    prompt_template = ChatPromptTemplate.from_template(prompt)

    return (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt_template
        | model
        | StrOutputParser()
    )

# Helper function to format documents for RAG retrieval
def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])

# Main execution
if __name__ == "__main__":
    file_path = "202503_RAG_sales/sales_summary.csv"  # Update with your actual file
    docs = load_and_preprocess_data(file_path)
    
    # Setup vector store and retriever
    vector_store = setup_vector_store(docs)
    retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={'k': 1000})
    

    # Create RAG chain
    rag_chain = create_rag_chain(retriever)

    # Example query
    query = "What was the total revenue? Can you provide any insights?"
    print("Question:", query)
    for chunk in rag_chain.stream(query):
        print(chunk, end="", flush=True)
    print("\n" + "-" * 50 + "\n")
