# pip install langchain langchain-community faiss-cpu llama-cpp-python sentence-transformers
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.document_loaders import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import LlamaCpp
from langchain.chains import RetrievalQA
from langchain.schema import Document

text_data ="""
 **Monthly Sales Trends**:
        sale_date
        2024-01-31    7380897
        2024-02-29    4979950
        2024-03-31    7443369
        2024-04-30    8366908
        2024-05-31    8706027
        2024-06-30    6950311
        2024-07-31    6480954
        2024-08-31    6330975
        2024-09-30    5202278
        2024-10-31    6578314
        2024-11-30    6628929
        2024-12-31    7399560"""

# Load and preprocess sales data
def load_and_preprocess_data(file_path):
    loader = CSVLoader(file_path=file_path)
    documents = loader.load()

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)
    
    return docs

# Load and preprocess sales data
def text_preprocess_data(textdata):

    doc = Document(
    page_content=textdata,
    metadata={"source": "sales_summary", "year": "2024"}
    )

    # Split documents into chunks
    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    # docs = text_splitter.split_documents(doc)
    
    return doc

# Generate embeddings and store in FAISS
def create_faiss_vectorstore(docs):
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embedding_model)
    vectorstore.save_local("faiss_sales_data")
    return vectorstore

# Load the Llama model
def load_llama_model():
    llm = LlamaCpp(
        model_path="llama-3.2.gguf",  # Update with your Llama 3.2 model file
        temperature=0.7,
        max_tokens=1024
    )
    return llm

# Create the RAG-based QA chain
def create_rag_chain(llm, vectorstore):
    retriever = vectorstore.as_retriever()
    rag_chain = RetrievalQA(llm=llm, retriever=retriever, return_source_documents=True)
    return rag_chain

# Run a query
def query_rag(chain, query):
    response = chain.invoke(query)
    return response["result"]

# Main Execution
if __name__ == "__main__":
    # file_path = "sales_summary.csv"  # Update with your actual file
    # docs = load_and_preprocess_data(file_path)

    docs = text_preprocess_data(text_data)

    print(docs.page_content)  # Output: Total sales revenue for Q1 was $1.5 million.
    print(docs.metadata)  # Output: {'source': 'sales_summary', 'quarter': 'Q1'}
 
    vectorstore = create_faiss_vectorstore(docs)
    llm = load_llama_model()
    
    rag_chain = create_rag_chain(llm, vectorstore)

    # Example query
    query = "What was the total sales? Can you provide insights on the monthly sales trends?"
    answer = query_rag(rag_chain, query)
    print("AI Response:", answer)