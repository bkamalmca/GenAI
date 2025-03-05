import streamlit as st
from phi.model.groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client
client = Groq()

st.set_page_config(page_title="Chatbot App", layout="wide")

# Sidebar menu
st.sidebar.title("Menus")
st.sidebar.markdown("### Chatbot")

# Main chat interface
st.title("Chatbot Interface")

# Initialize chat history if not already in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Type your message here...")
if user_input:
    # Display user input
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Get chatbot response
    with st.chat_message("assistant"):
        response_container = st.empty()
        response_text = ""
        
        # Generate response using Groq client
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                #*st.session_state.messages,
                # Set a user message for the assistant to respond to.
                {
                    "role": "user",
                    "content": user_input,
                },
            ],
            model="deepseek-r1-distill-llama-70b",
            temperature=0.5,
            max_completion_tokens=1024,
            top_p=1,
            stop=None,
            stream=False,
        )
        
        response_text = chat_completion.choices[0].message.content
        response_container.markdown(response_text)
        
    st.session_state.messages.append({"role": "assistant", "content": response_text})
