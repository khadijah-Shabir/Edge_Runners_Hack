# Import libraries
import whisper
import os
from gtts import gTTS
import streamlit as st
from groq import Groq

# Load Whisper model for transcription
try:
    model = whisper.load_model("base")  # Ensure "base" is a valid model name
except Exception as e:
    st.error(f"Error loading Whisper model: {str(e)}")
    st.stop()

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
def text_to_speech(text):
    tts = gTTS(text)
    output_audio = "output_audio.mp3"
    tts.save(output_audio)
    return output_audio

# Streamlit app layout
st.title("Audio Chatbot")

# Step 1: Upload audio file
audio_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])

if audio_file is not None:
    # Step 2: Transcribe the audio using Whisper
    with st.spinner("Transcribing audio..."):
        try:
            result = model.transcribe(audio_file)
            user_text = result["text"]
            st.text_area("Transcribed Text", user_text, height=200)
        except Exception as e:
            st.error(f"Error transcribing audio: {str(e)}")

    # Step 3: Get LLM response from Groq
    if user_text:
        with st.spinner("Getting response from LLM..."):
            try:
                response_text = get_llm_response(user_text)
                st.text_area("LLM Response", response_text, height=200)
            except Exception as e:
                st.error(f"Error getting response from LLM: {str(e)}")

        # Step 4: Convert the response text to speech
        with st.spinner("Generating audio response..."):
            try:
                output_audio = text_to_speech(response_text)
                st.audio(output_audio, format="audio/mp3")
            except Exception as e:
                st.error(f"Error generating audio response: {str(e)}")

# Optional: Add a footer or other content
st.write("Upload an audio file to chat with the AI!")
