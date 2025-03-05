import pandas as pd

# Load sales data
df = pd.read_csv("C:/LearnData/retail_sales_details.csv")  # Ensure this file contains relevant sales data

# Sample structure: [Date, Product, Category, Sales, Quantity, Customer Type]
# print(df.head())  # Check data structure

def generate_sales_summary(df):
    """Summarize key sales trends in text format."""
    
    # Top-selling products
    top_products = df.groupby("product_name")["total_amount"].sum().nlargest(5).to_string()
    
    # Sales trends by category
    category_trends = df.groupby("category")["total_amount"].sum().nlargest(5).to_string()

    # Monthly sales trends
    df["sale_date"] = pd.to_datetime(df["sale_date"])
    monthly_sales = df.resample('ME', on="sale_date")["total_amount"].sum().to_string()

    # Create a sales report summary
    summary = f"""
    Context: It is retail sales data from a store for 2024. The data domains are Customers, Products and Sales. 
    The data contains the following columns: [sale_id, sale_date, customer_name, gender, age, city,
    product_name, category, brand, sale_quantity, unit_price, total_amount]

    You are data analyst and you have been tasked with analyzing the sales summary data to identify key trends and insights.
     
    📊 **Sales Insights Report** 📊
    
    🔹 **Top-Selling Products**:  
    {top_products}

    🔹 **Top Sales Categories**:  
    {category_trends}

    🔹 **Monthly Sales Trends**:  
    {monthly_sales}
    """

    return summary

# Generate summary
sales_summary = generate_sales_summary(df)
print(sales_summary)
