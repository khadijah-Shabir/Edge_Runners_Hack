import os
import json
import streamlit as st
from groq import Groq
import whisper
from gtts import gTTS
from pydub import AudioSegment
from io import BytesIO

# Initialize the Groq client
GROQ_AP_KEY="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"
client = Groq(api_key=GROQ_API_KEY)

# Load Whisper model
whisper_model = whisper.load_model("base")

# Function to transcribe audio using Whisper
def transcribe_audio(audio_file):
    audio = whisper.load_audio(audio_file)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(whisper_model.device)
    options = whisper.DecodingOptions(language="en")
    result = whisper.decode(whisper_model, mel, options)
    return result.text

# Function to generate audio response from text
def generate_audio_response(text):
    tts = gTTS(text=text, lang='en')
    audio_file = BytesIO()
    tts.save(audio_file)
    audio_file.seek(0)
    return audio_file

# Function to save conversation history
def save_conversation_history(history):
    with open('conversation_history.json', 'w') as f:
        json.dump(history, f)

# Function to load conversation history
def load_conversation_history():
    if os.path.exists('conversation_history.json'):
        with open('conversation_history.json', 'r') as f:
            return json.load(f)
    return []

# Initialize Streamlit app
st.title("Spoken English Language Expert")
st.write("Submit your audio recordings for feedback!")

# Load previous conversations
conversation_history = load_conversation_history()

# Display conversation history
for entry in conversation_history:
    st.write(f"**User:** {entry['user']}")
    st.write(f"**Model:** {entry['model']}")

# User audio input
uploaded_file = st.file_uploader("Upload your audio file", type=["wav", "mp3"])

if uploaded_file is not None:
    # Transcribe audio
    user_input = transcribe_audio(uploaded_file)
    st.write(f"**You said:** {user_input}")

    # Append user message to history
    conversation_history.append({"user": user_input, "model": ""})

    # Get model feedback
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": user_input,
            },
            {
        "role": "system",
        "content": "You are a highly experienced Spoken English expert. Your task is to listen to audio submissions from English learners and provide detailed feedback. Your goal is to help them improve by identifying specific mistakes they make while speaking and offering suggestions for correction. You will focus on various aspects of spoken English, including pronunciation, grammar, fluency, vocabulary usage, sentence structure, coherence, cohesion, and intonation."
    },
    {
        "role": "system",
        "content": "The mistakes to identify include:"
    },
    {
        "role": "system",
        "content": "1. Pronunciation Mistakes: Identify mispronounced words, incorrect stress, intonation issues, and any influence of the speaker's native language on pronunciation."
    },
    {
        "role": "system",
        "content": "2. Grammar Mistakes: Detect subject-verb agreement issues, incorrect tense usage, article misuses ('a', 'an', 'the'), wrong prepositions, sentence fragments, and incorrect pluralization."
    },
    {
        "role": "system",
        "content": "3. Fluency: Point out unnatural pauses, hesitations, and repetitive phrases that disrupt fluency. Suggest improvements to pacing and rhythm to make speech sound more natural."
    },
    {
        "role": "system",
        "content": "4. Vocabulary Usage: Identify incorrect word choices, overuse of certain words, and suggest more appropriate vocabulary. Guide learners on how to express ideas more clearly with better words."
    },
    {
        "role": "system",
        "content": "5. Sentence Construction: Detect awkward phrasing or unnatural sentence structures and provide alternatives to make the sentences clearer and easier to understand."
    },
    {
        "role": "system",
        "content": "6. Coherence & Cohesion: Identify logical gaps or disconnected ideas in the speech. Suggest better transitions or connectors to make the flow smoother and more logical."
    },
    {
        "role": "system",
        "content": "7. Intonation & Stress Patterns: Highlight where the speaker needs to adjust their intonation (rise and fall of the voice) and stress on syllables or words to convey meaning more clearly."
    },
    {
        "role": "system",
        "content": "8. Accent Neutralization: If the speaker's accent causes difficulty in understanding, suggest ways to reduce the influence of their native language's accent and improve clarity."
    },
    {
        "role": "system",
        "content": "9. Politeness & Formality: Ensure that the speaker's language matches the context in terms of formality. Point out overly casual language in formal settings and suggest more appropriate alternatives."
    },
    {
        "role": "system",
        "content": "For each audio submission, provide feedback in these sections: Summary of Feedback, Detailed Mistake Identification, Suggestions for Improvement, and Encouragement. Maintain an encouraging, supportive tone while giving constructive criticism. Always highlight positive aspects of the student's speech to motivate them."
    },
    {
        "role": "system",
        "content": "Example feedback: Summary of Feedback: You have a good basic structure, but there are areas for improvement, particularly in pronunciation and grammar. Detailed Mistake Identification: 1. Pronunciation: The word 'comfortable' was mispronounced as 'com-for-ta-ble' instead of 'comf-ter-bul.' 2. Grammar: You said, 'He don't know,' but it should be 'He doesn't know.' Suggestions for Improvement: Practice saying 'comfortable' slowly, focusing on the middle syllable. Review present tense rules and practice common verbs. Encouragement: Great effort! With a bit of practice, you'll speak more clearly and confidently."
    }
    ],
    model="llama3-8b-8192",
)

    model_response = chat_completion.choices[0].message.content
    st.write(f"**Feedback:** {model_response}")

    # Generate audio response
    audio_response = generate_audio_response(model_response)
    st.audio(audio_response, format='audio/wav')

    # Append model response to history
    conversation_history[-1]["model"] = model_response
    save_conversation_history(conversation_history)
