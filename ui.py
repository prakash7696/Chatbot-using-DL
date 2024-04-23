import streamlit as st
import requests

# Define Streamlit UI components
st.title("Chatbot with Streamlit")

# User input for query
user_query = st.text_input("Enter your question:")

# Button to trigger chatbot response
if st.button("Get Response"):
    # Make POST request to Flask API
    api_url = 'http://127.0.0.1:5000/api/chatbot'  # Update with your Flask API URL
    data = {'query': user_query}
    response = requests.post(api_url, json=data)

    # Display chatbot response
    if response.status_code == 200:
        chatbot_response = response.json()['response']
        st.success(f"Chatbot: {chatbot_response}")
    else:
        st.error("Error fetching response from chatbot")

