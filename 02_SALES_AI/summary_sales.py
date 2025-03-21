import pandas as pd

# Load sales data
df = pd.read_csv("C:/LearnData/retail_sales_details.csv")  # Ensure this file contains relevant sales data

# Sample structure: [Date, Product, Category, Sales, Quantity, Customer Type]
# print(df.head())  # Check data structure

def generate_sales_summary(df):
    """Summarize key sales trends in text format."""
    
    # Top-selling products
    top_products = df.groupby("product_name")["total_amount"].sum().nlargest(10).to_string()
    
    # Sales trends by category
    category_trends = df.groupby("category")["total_amount"].sum().nlargest(10).to_string()

    # Monthly sales trends
    df["sale_date"] = pd.to_datetime(df["sale_date"])
    monthly_sales = df.resample('ME', on="sale_date")["total_amount"].sum().to_string()

     # Top customers 
    top_customers = df.groupby("customer_name")["total_amount"].sum().nlargest(10).to_string()

    # Define age groups
    bins = [0, 18, 25, 35, 45, 55, 65, 100]
    labels = ["<18", "18-25", "26-35", "36-45", "46-55", "56-65", "65+"]

    # Add age group column
    df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels)

    # summary by Gender, Age group, City
    # Summarize by Gender
    sales_by_gender = df.groupby("gender")["total_amount"].sum().reset_index()

    # Summarize by Age Group
    sales_by_age = df.groupby("age_group")["total_amount"].sum().reset_index()

    # Summarize by City
    sales_by_city = df.groupby("city")["total_amount"].sum().reset_index()

    # Create a sales report summary
    summary = f"""
    Context: It is retail sales data from a store for 2024. The data domains are Customers, Products and Sales. 
    The data contains the following columns: [sale_id, sale_date, customer_name, gender, age, city,
    product_name, category, brand, sale_quantity, unit_price, total_amount]

    You are data analyst and you have been tasked with analyzing the sales summary data to identify key trends and insights.
     
    📊 **Sales Insights Report** 📊
    
    🔹 **Top-Selling Products by Sales Total**
    {top_products}

    🔹 **Top Sales Categories by Sales Total**
    {category_trends}

    🔹 **Monthly Sales Trends**
    {monthly_sales}

    🔹 **Top customers by Sales Total**
    {top_customers}

    🔹 **Sales by Gender**
    {sales_by_gender}

    🔹 **Sales by Age group**
    {sales_by_age}

    🔹 **Sales by City**
    {sales_by_city}

    """

    return summary

# Generate summary
sales_summary = generate_sales_summary(df)
print(sales_summary)
