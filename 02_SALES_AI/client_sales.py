from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()

chat_completion = client.chat.completions.create(
    #
    # Required parameters
    #
    messages=[
        # Set an optional system message. This sets the behavior of the
        # assistant and can be used to provide specific instructions for
        # how it should behave throughout the conversation.
            {
            "role": "system",
            "content": """Context: It is retail sales data from a store for 2024. The data domains are Customers, Products and Sales.
    The data contains the following columns: [sale_id, sale_date, customer_name, gender, age, city,
    product_name, category, brand, sale_quantity, unit_price, total_amount]

    You are data analyst and you have been tasked with analyzing the sales summary data to identify key trends and insights.

    📊 **Sales Insights Report** 📊

    🔹 **Top-Selling Products by sales total**:
        product_name
        Curtains Set        3336957
        Electric Shaver     2974543
        Smartwatch Elite    2947770
        Towel Set           2898202
        Gaming Console Z    2838056

            🔹 **Top Sales Categories**:
        category
        Household      35048326
        Electronics    26093540
        Beauty         21306606"""
        },

        {
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
        2024-12-31    7399560"""
        },
        # Set a user message for the assistant to respond to.
        {
            "role": "user",
            "content": "Can you provide the summary of sales data",
        }
    ],

    # The language model which will generate the completion.
    #model="llama-3.3-70b-versatile",
    model="deepseek-r1-distill-llama-70b",

    #
    # Optional parameters
    #

    # Controls randomness: lowering results in less random completions.
    # As the temperature approaches zero, the model will become deterministic
    # and repetitive.
    temperature=0.5,

    # The maximum number of tokens to generate. Requests can use up to
    # 32,768 tokens shared between prompt and completion.
    max_completion_tokens=1024,

    # Controls diversity via nucleus sampling: 0.5 means half of all
    # likelihood-weighted options are considered.
    top_p=1,

    # A stop sequence is a predefined or user-specified text string that
    # signals an AI to stop generating content, ensuring its responses
    # remain focused and concise. Examples include punctuation marks and
    # markers like "[end]".
    stop=None,

    # If set, partial message deltas will be sent.
    stream=True,
)

# Print the completion returned by the LLM.
# print(chat_completion.choices[0].message.content)

for chunk in chat_completion:
    print(chunk.choices[0].delta.content, end="")