# Import libraries
import whisper
import os
from gtts import gTTS
import streamlit as st
from groq import Groq

# Load Whisper model for transcription with error handling
try:
    model = whisper.load_model("base")
except AttributeError as e:
    st.error(f"Error loading Whisper model: {e}")
    model = None  # Handle the case when model loading fails

# Set up Groq API client (ensure GROQ_API_KEY is set in your environment)
GROQ_API_KEY = "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"

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

# Main chatbot function to handle audio input and output
def chatbot(audio):
    if model is None:
        return "Model not available", None

    # Step 1: Transcribe the audio using Whisper
    result = model.transcribe(audio)
    user_text = result["text"]

    # Step 2: Get LLM response from Groq
    response_text = get_llm_response(user_text)

    # Step 3: Convert the response text to speech
    output_audio = text_to_speech(response_text)

    return response_text, output_audio

# Streamlit UI setup
st.title("Audio Chatbot")

# Upload audio file
audio_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])

if audio_file is not None:
    # Process the uploaded audio file
    response_text, output_audio = chatbot(audio_file)

    # Display the response text
    st.subheader("Response:")
    st.write(response_text)

    # Provide the audio output
    st.audio(output_audio)


