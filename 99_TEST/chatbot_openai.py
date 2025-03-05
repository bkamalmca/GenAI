import streamlit as st
from openai import OpenAI

# Initialize OpenAI client (replace 'your-api-key' with your actual key)
client = OpenAI(api_key="your-api-key")

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
        
        # Stream response from OpenAI
        response = client.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            stream=True
        )
        
        for chunk in response:
            response_text += chunk.choices[0].delta.get("content", "")
            response_container.markdown(response_text)
        
    st.session_state.messages.append({"role": "assistant", "content": response_text})
