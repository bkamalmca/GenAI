import streamlit as st

# Title
st.title("My Streamlit App")

# Interactive widget
user_input = st.slider("Select a number", 0, 100)

# Display dynamic outputs
st.write(f"You selected: {user_input}")

# Plot with Matplotlib
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [user_input, 2, 3])
st.pyplot(fig)

# Run app
##PS C:\SourceCode\Kamal\Test> streamlit run .\streamlit_test.py   