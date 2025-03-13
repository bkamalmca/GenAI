# pip install langchain langchain-community faiss-cpu sentence-transformers ollama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.document_loaders import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.schema import Document
from langchain_core.runnables import RunnablePassthrough
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import PromptTemplate


text_entries = [
    ("Total sales revenue for Q1 was $1.5M.", "sales_summary", "Q1"),
    ("Top-selling product: iPhone 15 (10,000 units)", "top_products", "2024"),
    ("Highest spending customer: John Doe ($20,000)", "top_customers", "2024"),
]

# Load and preprocess sales data
def text_preprocess_data(textdata):
    docs = [
        Document(
            page_content=text, 
            metadata={"source": source, "period": period}
        )
        for text, source, period in textdata
    ]
    return docs

# Generate embeddings and store in FAISS
def create_faiss_vectorstore(docs):
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embedding_model)
    vectorstore.save_local("faiss_sales_data")
    return vectorstore

# Load FAISS vectorstore from file
def load_faiss_vectorstore_from_file():
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local(
        "faiss_sales_data", 
        embeddings=embedding_model, 
        allow_dangerous_deserialization=True
    )
    return vectorstore

# Load the Ollama model
def load_ollama_model():
    llm = Ollama(model="llama3.2")  # Ensure Ollama is running and has Llama 3
    return llm

# Create the RAG-based retrieval chain
def create_rag_chain(llm, vectorstore):
    retriever = vectorstore.as_retriever()

    '''
    # Define prompt template
    prompt = PromptTemplate.from_template(
        "You are an AI assistant. Use the following retrieved context to answer the question.\n\n"
        "Context:\n{context}\n\n"
        "Question:\n{question}\n\n"
        "Answer:"
    )
    '''

    # Create retrieval chain
    rag_chain = create_retrieval_chain(retriever, llm)

    return rag_chain

# Example Query Execution
def query_rag(chain, query):
    # response = chain.invoke(query)
    
    response = chain.invoke({"input": query})
    return response  # Adjust key if necessary

# Main Execution
if __name__ == "__main__":
    # docs = text_preprocess_data(text_entries)
    # vectorstore = create_faiss_vectorstore(docs)

    vectorstore = load_faiss_vectorstore_from_file()

    llm = load_ollama_model()
    print(llm)
    response = llm.invoke("What is 2 + 2?")
    print("Ollama Response:", response)    

    
    rag_chain = create_rag_chain(llm, vectorstore)
    print("Expected Input Schema:", rag_chain.input_schema.schema()) 

'''
    query = "What is the total sales? Can you provide insights?"
    answer = query_rag(rag_chain, query)
    print("AI Response:", answer)
'''

# not worked due to Schema mismatch ERROR - ollama vs huggingface embeddings
# tried several attempts but still failed