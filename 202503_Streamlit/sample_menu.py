import streamlit as st

st.title("📊 Sales Order Dashboard")

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
    "🏠 Home         ": "home",
    "📦 View Orders  ": "view_orders",
    "✏️ Modify Orders": "modify_orders",
    "📊 Analytics    ": "analytics"
}

# Initialize session state for page selection
if "selected_page" not in st.session_state:
    st.session_state.selected_page = "home"  # Default page

# Sidebar button-based navigation with active highlight
for label, key in menu_options.items():
    if st.sidebar.button(label, key=key):
        st.session_state.selected_page = key  # Store selected option

# Display active section
st.subheader(f"📌 {list(menu_options.keys())[list(menu_options.values()).index(st.session_state.selected_page)]}")

if st.session_state.selected_page == "home":
    st.write("Welcome to the Sales Order System!")
elif st.session_state.selected_page == "view_orders":
    st.write("List of all orders will be displayed here.")
elif st.session_state.selected_page == "modify_orders":
    st.write("Modify existing orders here.")
elif st.session_state.selected_page == "analytics":
    st.write("View sales trends and reports.")
