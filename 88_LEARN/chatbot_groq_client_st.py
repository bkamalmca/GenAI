import streamlit as st
#from phi.model.groq import Groq
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

salemsg1={
            "role": "system",
            "content": """Context: It is retail sales data from a store for 2024. The data domains are Customers, Products and Sales.
    The data contains the following columns: [sale_id, sale_date, customer_name, gender, age, city,
    product_name, category, brand, sale_quantity, unit_price, total_amount]

    You are data analyst and you have been tasked with analyzing the sales summary data to identify key trends and insights.

    📊 **Sales Insights Report** 📊

    🔹 **Top-Selling Products by sales total**:
        product_name
        Curtains Set                3336957
        Electric Shaver             2974543
        Smartwatch Elite            2947770
        Towel Set                   2898202
        Gaming Console Z            2838056
        Shoe Rack                   2786146
        Electric Pressure Cooker    2625886
        Wireless Gaming Mouse       2546440
        Wall Clock                  2518685
        Shampoo Herbal              2504838

            🔹 **Top Sales Categories**:
        category
        Household      35048326
        Electronics    26093540
        Beauty         21306606"""
        }

salemsg2={
            "role": "system",
            "content": """Context: It is retail sales data from a store for 2024. The data domains are Customers, Products and Sales.
    The data contains the following columns: [sale_id, sale_date, customer_name, gender, age, city,
    product_name, category, brand, sale_quantity, unit_price, total_amount]

    Additional monthly sales data.

            🔹 **Monthly Sales Trends**:
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
        2024-12-31    7399560
        
            🔹 **Top customers by Sales Total**
        customer_name
        Rohit Choudhary    2605304
        Swati Das          2496217
        Sneha Rao          2481199
        Meena Gopal        2457278
        Shruti Prasad      2442006
        Neha Kapoor        2344035
        Asha Pillai        2156002
        Arjun Kumar        2133273
        Rajiv Joshi        2022708
        Rahul Sen          2002140

            🔹 **Sales by Gender**
       gender  total_amount
    0  Female      41792097
    1    Male      40656375

    🔹 **Sales by Age group**
      age_group  total_amount
    0       <18             0
    1     18-25       9211050
    2     26-35      27622159
    3     36-45      21712172
    4     46-55      18065186
    5     56-65       5837905
    6       65+             0

    🔹 **Sales by City**
        city  total_amount
    0     Chennai      17644819
    1  Coimbatore      15144837
    2     Madurai      16637754
    3       Salem      16786763
    4      Trichy      16234299
        """
        }

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
                salemsg1,
                #*st.session_state.messages,
                # Set a user message for the assistant to respond to.
                {
                    "role": "user",
                    "content": user_input,
                },
            ],
            model="deepseek-r1-distill-llama-70b",
            temperature=0.5,
            max_completion_tokens=2048,
            top_p=1,
            stop=None,
            stream=False,
        )
        
        response_text = chat_completion.choices[0].message.content
        response_container.markdown(response_text)
        
    st.session_state.messages.append({"role": "assistant", "content": response_text})

# streamlit run .\chatbot_groq_client_st.py