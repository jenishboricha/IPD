import streamlit as st
import pandas as pd
import google.generativeai as genai

def get_gemini_response(question):
    try:
        # Configure the API key securely
        genai.configure(api_key="AIzaSyBzB-FbuQimtmUEoaXUwYdGoxUwTXvMO3I")

        # Initialize the generative model
        model = genai.GenerativeModel("gemini-pro")

        # Start a chat session
        chat = model.start_chat()

        # Send a message to the chat model
        response = chat.send_message(question, stream=True)

        # Collect and return the response text
        response_text = ""
        for message in response:
            # Print out the message to understand its structure
            st.write(message.text)
            # Extract the actual content of the message


        return response_text

    except Exception as e:
        print(f"Error occurred: {e}")
        return None

# Streamlit app UI
st.title("Educational Script Generator")
st.write("Welcome")
st.write("Learn any topic easily")

# Input for the topic
topic = st.text_input("Enter the topic to learn")

# Slider for difficulty
difficulty = st.slider("Select 0 for easy and 1 for Hard", 0.0, 1.0, 0.0)

# Button to submit
submit = st.button("Submit")

if submit:
    if topic:
        st.write("Generating script, please wait...")

        difficulty_text = "easy" if difficulty < 0.5 else "hard"

        # Prompt construction
        prompt = f"Write a 300-word educational script for a video that explains the topic of '{topic}' at a {difficulty_text} difficulty level. Use clear and engaging language suitable for teenagers. Include at least two real-life examples to illustrate key concepts. Ensure the explanation is concise and maintains the audience's interest throughout the script."

        # Get the response from the Gemini model
        st.write(get_gemini_response(prompt))

        # Convert the response to a DataFrame
    else:
        st.write("Please enter a valid topic.")
