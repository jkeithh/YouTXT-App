import streamlit as st
import yt_dlp as youtube_dl
from deepgram import Deepgram
from streamlit_quill import st_quill

# API Key (Replace with your own)
DEEPGRAM_API_KEY = 'a0b3e0caed8808979462331899c72fe79eda5ba8'

# Initialize Deepgram client
dg_client = Deepgram(DEEPGRAM_API_KEY)

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

        # Display the transcript
        st.text_area("Transcript:", transcript)

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
