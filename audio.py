from audio_recorder_streamlit import audio_recorder
import streamlit as st
import tempfile
from openai import OpenAI

client = OpenAI()

def record_and_transcribe():
    st.info("🎙️ Click to record your answer")
    audio_bytes = audio_recorder(text="Start Recording", pause_threshold=1.5)

    if audio_bytes:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
            tmpfile.write(audio_bytes)
            tmpfile_path = tmpfile.name

        with open(tmpfile_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return {"transcript": transcript.text}

    return {"transcript": ""}
