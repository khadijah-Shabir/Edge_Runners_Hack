# Import libraries
import os
from gtts import gTTS
import streamlit as st
from groq import Groq

# Set up Groq API client (ensure GROQ_API_KEY is set in your environment)
GROQ_API_KEY = "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"
Client=Groq(api_key=GROQ_API_KEY)

# Function to get the LLM response from Groq
def get_llm_response(user_input):
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": user_input}],
        model="llama3-8b-8192",  # Replace with your desired model
    )
    return chat_completion.choices[0].message.content

# Function to convert text to speech using gTTS
def text_to_speech(text, output_audio="output_audio.mp3"):
    tts = gTTS(text)
    tts.save(output_audio)
    return output_audio

# Main chatbot function to handle user input and output
def chatbot(user_input):
    # Step 1: Get LLM response from Groq
    response_text = get_llm_response(user_input)

    # Step 2: Convert the response text to speech
    output_audio = text_to_speech(response_text)

    return response_text, output_audio

# Streamlit UI setup
st.title("Text Chatbot")

# Text input for user
user_input = st.text_area("Enter your message:", height=150)

if st.button("Send"):
    if user_input:
        # Process the user input
        response_text, output_audio = chatbot(user_input)

        # Display the response text
        st.subheader("Response:")
        st.write(response_text)

        # Provide the audio output
        if output_audio:
            st.audio(output_audio)
    else:
        st.warning("Please enter a message.")
