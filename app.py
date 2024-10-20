import os
import streamlit as st
from spellchecker import SpellChecker
from groq import Groq
import re

# Initialize the Groq client
client = Groq(api_key="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")
class GrammarCorrector:
    def __init__(self):
        self.spell = SpellChecker()

    def identify_mistakes(self, text):
        words = re.findall(r'\b\w+\b', text.lower())
        misspelled = self.spell.unknown(words)
        mistakes = []

        for word in misspelled:
            for match in re.finditer(r'\b' + re.escape(word) + r'\b', text.lower()):
                start = match.start()
                end = match.end()
                original_word = text[start:end]
                mistakes.append((original_word, start, end))

        return mistakes

    def report_mistakes(self, text):
        mistakes = self.identify_mistakes(text)
        st.write("\n--- Spelling Mistakes Found ---")
        for i, (mistake, start, end) in enumerate(mistakes, start=1):
            correction = self.spell.correction(mistake.lower())
            st.write(f"{i}. Misspelled: '{mistake}' at position {start}-{end}.")

        return mistakes
# App Configuration
st.set_page_config(page_title="EnglishCoach", layout="wide")
st.title("EnglishCoach: Improve Your Communication Skills")
st.write("Unlock Your English Potential with Personalized Feedback!")

# Sidebar for Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choose a module", ["Home", "Writing Module", "Speaking Module"])

# Function to display writing plan
def display_writing_plan(plan_days, topics):
    # Allow the user to select their current day
    day = st.number_input(f"Select your current day (1-{plan_days})", 1, plan_days)
    
    # Display today's topic
    topic = topics[day - 1]  # Get the topic for the selected day
    st.write(f"### Today's Topic (Day {day}): {topic}")
    
    # Show upcoming topics in a dropdown (next 5 days)
    upcoming_days = list(range(day + 1, min(day + 6, plan_days + 1)))  # Next 5 days
    upcoming_topics = [f"Day {d}: {topics[d - 1]}" for d in upcoming_days]
    
    if upcoming_topics:
        st.selectbox("Upcoming Topics", upcoming_topics)
    else:
        st.write("No upcoming topics available.")

    # Write area for user to submit their essay
    st.write("#### Write your essay below:")
    user_input = st.text_area(f"Write your essay on: {topic}", height=200)

    # Submit button for essay
    if st.button("Submit for Feedback"):
        if len(user_input.strip()) == 0:
            st.warning("Please enter some text before submitting.")
        else:
            input_text = user_input

            corrector = GrammarCorrector()
            corrector.report_mistakes(input_text)

            # Initialize the client with your API key
            client = Groq(api_key="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")
            retrieved_content = "I am A1 user"

            # Use the retrieved content as context for the chat completion
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You have the change the sentence according to the english standards if needed but add any sentence by yourself just change the input provided to you.If user is of A1 level then retur the output for the begineers A2 for average and A3 for advance"},
                    {"role": "user", "content": retrieved_content},
                    {"role": "user", "content": input_text},
                ],
                model="llama3-70b-8192",
                temperature=0.5,
                max_tokens=1024,
                top_p=1,
                stop=None,
                stream=False,
            )

            model_output = chat_completion.choices[0].message.content
            feedback=model_output

            if feedback:
                st.success("Your writing has been submitted! Here’s the feedback:")
                st.write(f"**Feedback**: {feedback}")





# Home Navigation
if page == "Home":
    st.header("Welcome to EnglishCoach")
    st.write("This platform is designed to assist you in improving your English communication skills through personalized feedback and structured writing plans.")

# Writing Module
elif page == "Writing Module":
    st.header("Writing Module")
    st.write(""" 
    **EnglishCoach** is designed to assist you in improving your English communication skills.
    Choose a **Writing Plan** (30, 45, or 60 days) and practice writing on various topics. You’ll get real-time feedback.
    The key to mastering writing is consistency. Select a plan that fits your goals and start practicing today!
    """)
    
    # Key Feature Rectangles
    st.subheader("Key Features of Writing Plans")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("### 30-Day Plan")
        st.write("Focused on basics: introduction, conclusion, argumentative, descriptive writing.")
        if st.button("Explore 30-Day Plan"):
            st.session_state.page = "30-Day Plan"
            
    with col2:
        st.write("### 45-Day Plan")
        st.write("Expanded topics: deep-dive into opinion-based and analytical essays.")
        if st.button("Explore 45-Day Plan"):
            st.session_state.page = "45-Day Plan"
            
    with col3:
        st.write("### 60-Day Plan")
        st.write("Comprehensive plan covering reports, summaries, and essay writing.")
        if st.button("Explore 60-Day Plan"):
            st.session_state.page = "60-Day Plan"

    # Sub-navigation for Writing Plans
    writing_page = st.radio("Select Writing Plan", ["Home", "30-Day Plan", "45-Day Plan", "60-Day Plan"])

    if writing_page == "Home":
        st.write("""Writing is an essential skill. Choose a plan to begin practicing.""")

    elif writing_page == "30-Day Plan":
        st.write("### 30-Day Writing Plan")
        topics_30_day = [
            "Technology and Social Media", "Environmental Issues", "Education Systems",
            "Globalization and Culture", "Health and Wellness", "Economic Development",
            "Science and Innovation", "Travel and Tourism", "Food and Nutrition", 
            "Urbanization and Infrastructure", "Family Values and Relationships",
            "Cultural Diversity and Exchange", "Social Media Ethics", "Human Rights and Equality",
            "Traditional vs. Modern Practices", "Community Service and Volunteerism",
            "Language and Identity", "Immigration and Integration", "Social Justice and Activism",
            "Generational Differences", "The Impact of Artificial Intelligence",
            "Benefits and Drawbacks of Social Media", "Should University Education be Free?",
            "The Role of Government in Public Health", "Pros and Cons of Standardized Testing",
            "The Influence of Celebrity Culture", "Is Climate Change a Global Emergency?",
            "The Ethics of Animal Testing", "Should Schools Prioritize STEM Education?"
        ]
        display_writing_plan(30, topics_30_day)

    elif writing_page == "45-Day Plan":
        st.write("### 45-Day Writing Plan")
        topics_45_day = [
            "The Role of Media in Society", "Environmental Conservation", "The Future of Education",
            "Cultural Impacts of Technology", "Healthcare Accessibility", "Social Justice Movements",
            "The Impact of Globalization", "Youth Activism", "The Importance of Mental Health",
            "Climate Change and Policy", "Artificial Intelligence and Ethics", "The Future of Work",
            "Civic Responsibility and Engagement", "Digital Privacy and Security",
            "Sustainable Development Goals", "Gender Equality", "Food Security",
            "Technology in Education", "Community Building", "Art and Social Change",
            "Crisis Management", "Data Privacy", "Social Media Influence", "Renewable Energy",
            "Public Health Policies", "Consumerism", "Urban Development", "Sports and Society",
            "Diversity and Inclusion", "Future of Transportation"
        ]
        display_writing_plan(45, topics_45_day)

    elif writing_page == "60-Day Plan":
        st.write("### 60-Day Writing Plan")
        topics_60_day = [
            "Impact of Technology on Society", "Environmental Sustainability", "Ethics of Genetic Engineering",
            "Artificial Intelligence in Daily Life", "Media Influence on Public Opinion", "Political Polarization",
            "Crisis and Recovery", "Future of Renewable Energy", "Intergenerational Dialogue",
            "Consumer Rights", "Racial Equality", "Global Health Issues", "The Role of Art in Society",
            "History of Social Movements", "International Relations and Peace", "Digital Transformation",
            "Public vs. Private Education", "Corporate Responsibility", "Urban vs. Rural Living",
            "Future of Work in a Digital Age", "Mental Health in the Workplace", "Transnationalism",
            "Cultural Heritage and Identity", "The Ethics of Surveillance", "Challenges of Globalization",
            "Crisis in Democracy", "Digital Economy", "Sustainable Agriculture", "Human Rights in the Digital Age",
            "Technology and the Future of Education", "Civic Engagement in the 21st Century"
        ]
        display_writing_plan(60, topics_60_day)

# Speaking Module
elif page == "Speaking Module":
    st.header("Speaking Module")

    # Speaking options
    speaking_option = st.radio("Choose Speaking Mode", ["Speak in Real-Time", "Submit Audio for Feedback"])

    if speaking_option == "Speak in Real-Time":
        st.write("Speak on a topic and get real-time feedback.")
        st.warning("This feature is under development.")
    elif speaking_option == "Submit Audio for Feedback":
        st.write("Submit your speech recording for feedback.")
        uploaded_file = st.file_uploader("Choose an audio file...", type=["wav", "mp3"])
        if uploaded_file is not None:        
            # Read the content of the uploaded file
            file_content = uploaded_file.read()

            # Create a transcription of the audio file
            transcription = client.audio.transcriptions.create(
                file=(uploaded_file.name, file_content),  # Pass file name and content
                model="whisper-large-v3-turbo",  # Required model to use for transcription
                prompt="Specify context or spelling",  # Optional
                response_format="json",  # Optional
                language="en",  # Optional
                temperature=0.0  # Optional
            )

            # Print the transcription text
            st.write("Original Text:")
            st.write(transcription.text)
            input_text = transcription.text

            # Initialize the Grammar Corrector
            corrector = GrammarCorrector()
            corrector.report_mistakes(input_text)

            # Initialize the client with your API key
            client = Groq(api_key="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")
            retrieved_content = "I am A1 user"

            # Use the retrieved content as context for the chat completion
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You have to change the sentence according to English standards, but do not add any new sentence. Only change the input provided. If the user is A1 level, return output for beginners. A2 for average, and A3 for advanced."},
                    {"role": "user", "content": retrieved_content},
                    {"role": "user", "content": input_text},
                ],
                model="llama3-70b-8192",
                temperature=0.5,
                max_tokens=1024,
                top_p=1,
                stop=None,
                stream=False,
            )

            # Get the output from the model
            model_output = chat_completion.choices[0].message.content
            feedback = model_output

            if feedback:
                st.success("Your writing has been submitted! Here’s the feedback:")
                st.write(f"**Feedback**: {feedback}")

# Footer
st.sidebar.markdown("---")
st.sidebar.write("Developed by Visionary Squad.")
