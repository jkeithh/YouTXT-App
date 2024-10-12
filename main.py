import streamlit as st
import yt_dlp as youtube_dl
from deepgram import Deepgram
from streamlit_quill import st_quill

# API Key for Deepgram
DEEPGRAM_API_KEY = 'a0b3e0caed8808979462331899c72fe79eda5ba8'

# Initialize Deepgram Client
dg_client = Deepgram(DEEPGRAM_API_KEY)

def extract_audio(url):
    """Extract audio from the given YouTube URL using yt-dlp."""
    ydl_opts = {'format': 'bestaudio', 'outtmpl': 'audio.mp3'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return 'audio.mp3'

def transcribe_audio(file_path):
    """Transcribe audio using Deepgram."""
    with open(file_path, 'rb') as audio:
        response = dg_client.transcription.prerecorded(audio, {'punctuate': True})
    return response['results']['channels'][0]['alternatives'][0]['transcript']

# Streamlit App Interface
st.title("YouTXT: Convert YouTube Videos to Text")
video_url = st.text_input("Enter YouTube URL:")

if st.button("Transcribe"):
    if video_url:
        st.info("Extracting audio...")
        audio_file = extract_audio(video_url)

        st.info("Transcribing audio...")
        transcript = transcribe_audio(audio_file)

        # Display transcript and allow editing
        st.text_area("Transcript:", transcript)
        edited_text = st_quill(value=transcript, placeholder="Edit the transcript here...")
        
        if st.button("Save Edited Transcript"):
            with open("edited_transcript.md", "w") as f:
                f.write(edited_text)
            st.success("Transcript saved!")
    else:
        st.error("Please enter a valid YouTube URL.")
