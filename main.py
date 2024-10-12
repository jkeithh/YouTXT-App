import streamlit as st
import openai
import yt_dlp as youtube_dl
from deepgram import Deepgram
from streamlit_quill import st_quill

# API Keys (Replace these with your own)
DEEPGRAM_API_KEY = 'a0b3e0caed8808979462331899c72fe79eda5ba8'
OPENAI_API_KEY = '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'

# Initialize APIs
dg_client = Deepgram(DEEPGRAM_API_KEY)
openai.api_key = OPENAI_API_KEY

# Streamlit App Interface
st.title("YouTXT: Convert YouTube Videos to Text")
video_url = st.text_input("Enter YouTube URL:")

def extract_audio(url):
    """Extract audio from the given YouTube URL using yt-dlp."""
    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': 'audio.mp3'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return 'audio.mp3'


if st.button("Transcribe"):
    if video_url:
        st.info("Extracting audio...")
        audio_file = extract_audio(video_url)

        # Send audio to Deepgram for transcription
        with open(audio_file, 'rb') as f:
            response = dg_client.transcription.prerecorded(f, {'punctuate': True})
            transcript = response['results']['channels'][0]['alternatives'][0]['transcript']

        st.text_area("Transcript:", transcript)

        # Generate summary using OpenAI
        summary = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Summarize the following: {transcript}",
            max_tokens=100
        ).choices[0].text.strip()

        st.text_area("Summary:", summary)

        # Allow editing in Quill editor
        edited_text = st_quill(value=transcript, placeholder="Edit the transcript here...")
        st.text_area("Edited Transcript:", edited_text)

        # Save edited transcript
        if st.button("Save"):
            with open("edited_transcript.md", "w") as f:
                f.write(edited_text)
            st.success("Transcript saved!")
    else:
        st.error("Please enter a valid YouTube URL.")
