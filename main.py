import streamlit as st
import yt_dlp as youtube_dl
from deepgram import Deepgram
import asyncio
import os

# API Key for Deepgram
DEEPGRAM_API_KEY = 'a0b3e0caed8808979462331899c72fe79eda5ba8'

# Initialize Deepgram Client
dg_client = Deepgram(DEEPGRAM_API_KEY)

def extract_audio(url):
    """Extract audio from the given YouTube URL using yt-dlp."""
    if os.path.exists("audio.mp3"):
        os.remove("audio.mp3")  # Clear previous downloads
    ydl_opts = {'format': 'bestaudio', 'outtmpl': 'audio.mp3'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return 'audio.mp3'

async def transcribe_audio(file_path):
    """Transcribe audio using Deepgram asynchronously."""
    with open(file_path, 'rb') as audio:
        source = {'buffer': audio, 'mimetype': 'audio/mpeg'}
        response = await dg_client.transcription.prerecorded(source, {'punctuate': True})
    return response['results']['channels'][0]['alternatives'][0]['transcript']

def run_async_function(func, *args):
    """Helper function to run async code inside a synchronous context."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(func(*args))

# Streamlit App Interface
st.title("YouTXT: Convert YouTube Videos to Text")

# Input for YouTube URL
video_url = st.text_input("Enter YouTube URL:", key="youtube_url")

if st.button("Transcribe", key="transcribe_button"):
    if video_url:
        st.info("Extracting audio...")
        audio_file = extract_audio(video_url)

        st.info("Transcribing audio...")
        transcript = run_async_function(transcribe_audio, audio_file)

        # Save transcript to session state
        st.session_state["transcript"] = transcript

# Display the transcript if available
if "transcript" in st.session_state:
    transcript = st.session_state["transcript"]
    st.text_area("Transcript:", transcript, height=300, key="transcript_area")

    # JavaScript to copy text to clipboard
    copy_script = f"""
        <script>
        function copyToClipboard() {{
            const text = `{transcript}`;  // Use backticks for multiline handling
            navigator.clipboard.writeText(text).then(() => {{
                alert('Transcript copied to clipboard!');
            }}).catch(err => {{
                console.error('Failed to copy: ', err);
            }});
        }}
        </script>
        <button onclick="copyToClipboard()">Copy Transcript</button>
    """

    # Render the JavaScript-based button
    st.markdown(copy_script, unsafe_allow_html=True)
