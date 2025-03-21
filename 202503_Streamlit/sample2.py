import streamlit as st
import pandas as pd
import datetime

st.title("Sales Order Management")
# st.header("This is a Header")
# st.subheader("This is a Subheader")
# st.text("This is normal text")

# Sidebar Menu
menu = st.sidebar.selectbox("Select an Option", ["Home", "View Orders", "Modify Orders", "Analytics"])

if menu == "Home":
    st.write("Welcome to the Sales Order Management System!")
    name = st.text_input("Enter your name")
    st.write(f"Hello, {name}!")

    #col1, col2 = st.columns(2)
    col1, col2 = st.columns([2, 1])  # First column is twice the width of the second

    # Place the inputs inside the columns
    with col1:
        product = st.selectbox("Select Product", ["Laptop", "Phone", "Tablet"])

    with col2:
        quantity = st.number_input("Enter Quantity", min_value=1, max_value=100, step=1)

    st.write(f"You selected {quantity} unit(s) of {product}.")


    agree = st.checkbox("I agree to the terms")
    if agree:
        st.write("Thank you for agreeing!")

    status = st.radio("Order Status", ["Pending", "Shipped", "Delivered"])
    st.write(f"Status selected: {status}")

    discount = st.slider("Select Discount", 0, 50, 5)
    st.write(f"Applied Discount: {discount}%")

    if st.button("Submit"):
        st.write("Form submitted!")

elif menu == "View Orders":
    st.write("Here you can view all sales orders.")

    tab1, tab2 = st.tabs(["Product", "Json"])
    with tab1:
        # Sample DataFrame
        data = pd.DataFrame({
            "Order ID": [101, 102, 103],
            "Product": ["Laptop", "Phone", "Tablet"],
            "Quantity": [2, 5, 3],
            "Price": [1000, 500, 300]
        })

        # Interactive Table
        edited_data = st.data_editor(data, num_rows="dynamic")  

        # Display selected row
        st.write("Updated Data:", edited_data)

    with tab2:
        jdata = {"Product": "Laptop", "Price": 1000}
        st.json(jdata)

        data = pd.DataFrame({"Product": ["Laptop", "Phone", "Tablet"], "Price": [1000, 500, 300]})
        #st.dataframe(data)

        # Add a selection column
        data["Select"] = False  

        # Editable Table
        edited_data = st.data_editor(data, column_config={"Select": st.column_config.CheckboxColumn("Select Row")})

        # Find selected row
        selected_rows = edited_data[edited_data["Select"]]
        st.write("You selected:", selected_rows)


elif menu == "Modify Orders":
    st.write("Modify existing sales orders.")
elif menu == "Analytics":
    st.write("View sales analytics and reports.")

# Date filter
start_date = st.sidebar.date_input("Start Date", datetime.date(2024, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime.date(2024, 12, 31))

# Category filter
category = st.sidebar.radio("Product Category", ["All", "Electronics", "Furniture", "Clothing"])

# Apply filter button
if st.sidebar.button("Apply Filters"):
    st.write(f"Filtering orders from {start_date} to {end_date} for category {category}")



