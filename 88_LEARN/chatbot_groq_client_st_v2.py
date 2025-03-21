import streamlit as st
from groq import Groq
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=API_KEY)

# Function to read system messages from JSON file
def load_sales_context(file_path="C:\SourceCode\Kamal\GenAI\88_LEARN\sales_context.json"):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Error loading context file: {e}")
        return []

# Load system messages
system_context = load_sales_context()

# Set Streamlit Page Config
st.set_page_config(page_title="Chatbot App", layout="wide")

# Sidebar
st.sidebar.title("Menus")
st.sidebar.markdown("### Chatbot")

# Title
st.title("Chatbot Interface")

# Initialize session state for chat history (Excludes system messages)
if "messages" not in st.session_state:
    st.session_state.messages = []  # Only stores user & assistant messages

# Display previous chat messages (Excluding system messages)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Type your message here...")
if user_input:
    # Display user input immediately
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Assistant response container
    with st.chat_message("assistant"):
        response_container = st.empty()
        response_text = ""

        # Generate streaming response using Groq API
        response_stream = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=system_context + st.session_state.messages + [{"role": "user", "content": user_input}],
            temperature=0.5,
            max_tokens=2048,
            top_p=1,
            stream=True,  # Enable streaming
        )

      # Process streamed response safely
        for chunk in response_stream:
            if chunk.choices and hasattr(chunk.choices[0], "delta"):
                delta = chunk.choices[0].delta
                if hasattr(delta, "content") and delta.content:
                    response_text += delta.content
                    response_container.markdown(response_text)

    # Save assistant response to session history
    st.session_state.messages.append({"role": "assistant", "content": response_text})



# streamlit run .\chatbot_groq_client_st_v2.py