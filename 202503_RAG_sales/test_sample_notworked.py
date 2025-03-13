# pip install langchain langchain-community faiss-cpu llama-cpp-python sentence-transformers
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.document_loaders import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import LlamaCpp
from langchain.chains import RetrievalQA
from langchain.schema import Document

text_entries = [
    ("Total sales revenue for Q1 was $1.5M.", "sales_summary", "Q1"),
    ("Top-selling product: iPhone 15 (10,000 units)", "top_products", "2024"),
    ("Highest spending customer: John Doe ($20,000)", "top_customers", "2024"),
]

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

    # Convert each tuple into a LangChain Document
    docs = [
        Document(
            page_content=text, 
            metadata={"source": source, "period": period}
        )
        for text, source, period in textdata
    ]
    # Split documents into chunks
    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    # docs = text_splitter.split_documents(doc)
    
    return docs

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

    docs = text_preprocess_data(text_entries)
    print(docs)

    # print(docs.page_content)  # Output: Total sales revenue for Q1 was $1.5 million.
    # print(docs.metadata)  # Output: {'source': 'sales_summary', 'quarter': 'Q1'}
 
    # print(type(docs))  # Should be <class 'list'>
    # print(type(docs[0]))  # Should be <class 'langchain.schema.Document'>
 

    vectorstore = create_faiss_vectorstore(docs)
    llm = load_llama_model()
    

    rag_chain = create_rag_chain(llm, vectorstore)

    # Example query
    query = "What was the total sales? Can you provide insights?"
    answer = query_rag(rag_chain, query)
    print("AI Response:", answer)

# not worked due to ERROR: Failed building wheel for llama-cpp-python
# tried several attempts installing C++, cmake, etc. but still failed