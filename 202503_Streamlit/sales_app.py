import streamlit as st
import pymysql
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os
import plotly.express as px

load_dotenv()  # Load .env file

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

# Function to connect to MySQL
def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

# Function to fetch sales transaction data
def fetch_db_data(query):

    conn = get_db_connection()
    
    # df = pd.read_sql(query, conn)
    with conn.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()  # Fetch as a list of dictionaries
    
    conn.close()
    
    # Convert to DataFrame
    df = pd.DataFrame(result)

    return df

def fetch_sales_data(query, start_date, end_date):

    conn = get_db_connection()
    
    params = [start_date, end_date]

    # df = pd.read_sql(query, conn)
    with conn.cursor() as cursor:
        cursor.execute(query, params)
        result = cursor.fetchall()  # Fetch as a list of dictionaries
    
    conn.close()
    
    # Convert to DataFrame
    df = pd.DataFrame(result)

    return df

product_query = """SELECT product_id, product_name, category, brand, price, stock_quantity FROM product"""
customer_query = """SELECT customer_id, customer_name, gender, age, city, state, convert(phone, char) phone FROM customer"""
sale_query = """select sale_id,
                sale_date,
                customer_name,
                gender,
                age,
                city,
                -- state,
                product_name,
                category,
                brand,
                sale_quantity,
                unit_price,
                total_amount
            from sample.retail_sales s,
                sample.customer c,
                sample.product p
            where s.customer_id = c.customer_id
            and s.product_id = p.product_id
            and s.sale_date between %s and %s"""
    
st.title("📈 Sales App - Analytics & AI")

# Sidebar Title
# st.sidebar.header("PulseAI")
# st.sidebar.text("- Smarter Decisions, Faster Growth...")

# Custom CSS for styling
st.sidebar.markdown("""
    <style>
    .sidebar-header {
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 0px;  /* Reduce space below header */
    }
    .sidebar-subtext {
        font-size: 14px;
        font-style: italic;
        margin-top: 0px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar content
st.sidebar.markdown('<p class="sidebar-header">PulseAI</p>', unsafe_allow_html=True)
st.sidebar.markdown('<p class="sidebar-subtext">- Smarter Decisions, Faster Growth...</p>', unsafe_allow_html=True)

# Define menu options
menu_options = {
    "🏠 Home": "home",
    "🤖 Chatbot AI": "chatbot",
    "📊 Analytics": "analytics"
}

# Initialize session state for page selection
if "selected_page" not in st.session_state:
    st.session_state.selected_page = "home"  # Default page

# Sidebar button-based navigation with active highlight
for label, key in menu_options.items():
    if st.sidebar.button(label, key=key):
        st.session_state.selected_page = key  # Store selected option

# Display active section
st.subheader(f"{list(menu_options.keys())[list(menu_options.values()).index(st.session_state.selected_page)]}")

if st.session_state.selected_page == "home":
    st.write("Welcome to the Sales Data View!")

    sale_tab1, prod_tab2, cust_tab3 = st.tabs(["Sales Transaction", "Product Details", "Customer Details"])

    with sale_tab1:
        # Fetch and filter data
        sdf = fetch_sales_data(sale_query, pd.to_datetime("2024-01-01"), pd.to_datetime("today"))

        # Dynamic Filters
        col1, col2 = st.columns(2)
        start_date = col1.date_input("Start Date", pd.to_datetime("2024-01-01"))
        end_date = col2.date_input("End Date", pd.to_datetime("today"))
        col3, col4 = st.columns(2)
        customer_name = col3.text_input("👤 Customer Name")
        product_name = col4.text_input("🔍 Product Name")

        # Apply filters in Pandas
        # sdf = sdf[(sdf["sale_date"] >= pd.to_datetime(start_date)) & 
        #        (sdf["sale_date"] <= pd.to_datetime(end_date))]

        if product_name:
            sdf = sdf[sdf["product_name"].str.contains(product_name, case=False, na=False)]

        if customer_name:
            sdf = sdf[sdf["customer_name"].str.contains(customer_name, case=False, na=False)]

        # Display the table with sorting and filtering enabled
        st.data_editor(sdf, hide_index=True, use_container_width=True)

    with prod_tab2:
        # Fetch and filter data
        pdf = fetch_db_data(product_query)
        # Display the table with sorting and filtering enabled
        st.data_editor(pdf, hide_index=True, use_container_width=True, num_rows="dynamic")

    with cust_tab3:
        # Fetch and filter data
        cdf = fetch_db_data(customer_query)
        # Display the table with sorting and filtering enabled
        st.data_editor(cdf, hide_index=True, use_container_width=True, num_rows="dynamic")

elif st.session_state.selected_page == "chatbot":
    st.write("Chatbot AI is ready to assist you!")

elif st.session_state.selected_page == "analytics":
    st.write("View sales trends and reports.")

    # Fetch and filter data
    df = fetch_sales_data(sale_query, pd.to_datetime("2024-01-01"), pd.to_datetime("today"))

    df["sale_date"] = pd.to_datetime(df["sale_date"])  # Convert to datetime
    df["sale_month"] = df["sale_date"].dt.strftime("%Y-%m")  # Converts to 'YYYY-MM' string

    # Define age groups
    bins = [0, 18, 25, 35, 45, 55, 65, 100]
    labels = ["<18", "18-25", "26-35", "36-45", "46-55", "56-65", "65+"]

    # Add age group column
    df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels)

    # Monthly Sales Trend
    sales_over_month = df.groupby("sale_month")["total_amount"].sum().reset_index()

    # Top 5 Products by Sales
    top_products = df.groupby("product_name")["total_amount"].sum().nlargest(5).reset_index()

    # Top Categories by Sales
    # Group sales by category and get the top 5
    top_categories = df.groupby("category")["total_amount"].sum().nlargest(5).reset_index()

    # Add percentage column
    top_categories["percentage"] = (top_categories["total_amount"] / top_categories["total_amount"].sum()) * 100

    # Summarize by Gender
    sales_by_gender = df.groupby("gender")["total_amount"].sum().reset_index()

    # Summarize by Age Group
    sales_by_age = df.groupby("age_group")["total_amount"].sum().reset_index()

    # Summarize by City
    sales_by_city = df.groupby("city")["total_amount"].sum().reset_index()


    # 📈 Monthly Sales Trend
    fig_monthly = px.line(sales_over_month, x="sale_month", y="total_amount", 
                        title="📈 Monthly Sales Trend", markers=True)
    st.plotly_chart(fig_monthly)

    # 🏆 Top 5 Products by Sales
    fig_top_products = px.bar(top_products, x="product_name", y="total_amount", 
                            title="🏆 Top 5 Products by Sales", color="total_amount")
    st.plotly_chart(fig_top_products)

    # Create Pie Chart
    fig_pie = px.pie(top_categories, 
                    names="category", 
                    values="total_amount", 
                    title="📊 Sales Distribution by Category",
                    hover_data=["total_amount", "percentage"],  
                    labels={"total_amount": "Sales Amount", "percentage": "Percentage"},
                    hole=0.4)  # Makes it a donut chart

    # Format hover text to show values and percentage
    fig_pie.update_traces(textinfo="label+percent+value")
    st.plotly_chart(fig_pie)

    # Gender Sales Chart
    fig_gender = px.bar(sales_by_gender, x="gender", y="total_amount", title="Total Sales by Gender", color="gender")
    st.plotly_chart(fig_gender)

    # Age Group Sales Chart
    fig_age = px.bar(sales_by_age, x="age_group", y="total_amount", title="Total Sales by Age Group", color="age_group")
    st.plotly_chart(fig_age)

    # City Sales Chart
    fig_city = px.bar(sales_by_city, x="city", y="total_amount", title="Total Sales by City", color="city")
    st.plotly_chart(fig_city)


