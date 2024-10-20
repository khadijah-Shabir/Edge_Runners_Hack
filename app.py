# Import libraries
import whisper
import os
from gtts import gTTS
import streamlit as st
from groq import Groq

# Load Whisper model for transcription
model = whisper.load_model("base")

# Set up Groq API client (ensure GROQ_API_KEY is set in your environment)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

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
        result = model.transcribe(audio_file)
        user_text = result["text"]
        st.text_area("Transcribed Text", user_text, height=200)

    # Step 3: Get LLM response from Groq
    with st.spinner("Getting response from LLM..."):
        response_text = get_llm_response(user_text)
        st.text_area("LLM Response", response_text, height=200)

    # Step 4: Convert the response text to speech
    with st.spinner("Generating audio response..."):
        output_audio = text_to_speech(response_text)
        st.audio(output_audio, format="audio/mp3")

# Optional: Add a footer or other content
st.write("Upload an audio file to chat with the AI!")
