import streamlit as st
from phi.agent import Agent, RunResponse
from phi.model.groq import Groq
from dotenv import load_dotenv
import re
from phi.utils.pprint import pprint_run_response

load_dotenv()

# Initialize Groq agent
agent = Agent(model=Groq(id="llama-3.3-70b-versatile"))

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
        
        # Get response from Groq agent
        #response_text = agent.get_response(user_input)
        response = agent.run(user_input, stream=False)
        #response_text: RunResponse = agent.run(user_input, stream=False)
        #response_text = response.message.content

        # print(response.content)
        response_container.markdown(response.content)
        
    st.session_state.messages.append({"role": "assistant", "content": response.content})

# streamlit run .\chatbot_groq_st.py