import streamlit as st

# Custom CSS for styling the sidebar buttons
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #f8f9fa;  /* Light background */
    }
    .sidebar-button {
        display: block;
        width: 100%;
        padding: 10px 15px;
        text-align: left;
        border: none;
        background-color: transparent;
        color: black;
        font-size: 16px;
        cursor: pointer;
        border-radius: 5px;
        margin: 5px 0;
    }
    .sidebar-button:hover {
        background-color: #e1e1e1;  /* Hover effect */
    }
    .sidebar-button.active {
        background-color: #007bff !important; /* Active button color */
        color: white !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("📂 Navigation")

# Define menu options
menu_options = {
    "🏠 Home": "home",
    "📦 View Orders": "view_orders",
    "✏️ Modify Orders": "modify_orders",
    "📊 Analytics": "analytics"
}

# Initialize session state for active button
if "selected_page" not in st.session_state:
    st.session_state.selected_page = "home"  # Default page

# Create buttons with active highlight
for label, key in menu_options.items():
    btn_class = "sidebar-button active" if st.session_state.selected_page == key else "sidebar-button"
    
    # Button as a clickable Markdown (CSS styled)
    if st.sidebar.markdown(f'<button class="{btn_class}" onclick="window.location.href=\'?page={key}\'">{label}</button>', unsafe_allow_html=True):
        st.session_state.selected_page = key  # Store active state

# Display the selected section
st.subheader(f"📌 {list(menu_options.keys())[list(menu_options.values()).index(st.session_state.selected_page)]}")

if st.session_state.selected_page == "home":
    st.write("Welcome to the Sales Order System!")
elif st.session_state.selected_page == "view_orders":
    st.write("List of all orders will be displayed here.")
elif st.session_state.selected_page == "modify_orders":
    st.write("Modify existing orders here.")
elif st.session_state.selected_page == "analytics":
    st.write("View sales trends and reports.")
