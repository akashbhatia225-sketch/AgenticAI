import streamlit as st
import requests
import nest_asyncio

# Apply nest_asyncio to handle nested event loops
nest_asyncio.apply()

# Streamlit frontend
st.title("Provide Research Topic")
topic = st.text_input("Enter a research topic:")

if st.button("Do research"):
    if not topic.strip():
        st.error("Please enter a valid research topic")
    else:
        with st.spinner("Processing..."):
            try:
                response = requests.post("http://localhost:8008/get_prints", json={"text": topic})
                if response.status_code == 200:
                    prints = response.json()["prints"]
                    st.subheader("Captured Print Statements:")
                    for line in prints:
                        if line.strip():
                            st.write(line)
                else:
                    st.error(f"Failed to fetch print statements: {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the backend server: {str(e)}")