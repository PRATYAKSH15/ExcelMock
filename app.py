import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from services.question_generator import generate_questions
from services.evaluator import evaluate_response
from services.feedback_generator import generate_feedback
from db.database import save_response, init_db
from session import initialize_session_state
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Excel Mock Interviewer", layout="wide")
st.sidebar.title("🧪 Interview Modes")
mode = st.sidebar.radio("Choose a mode:", ["Text Interview", "MCQ Test (30 mins)"])

st.title("🎤 AI-Powered Excel Mock Interviewer")

# Initialize DB and session state
init_db()
initialize_session_state()

# --- TEXT INTERVIEW MODE ---
if mode == "Text Interview":
    if st.button("🧠 Start Interview"):
        st.session_state.questions = generate_questions()
        st.session_state.current_q = 0
        st.session_state.responses = []
        st.session_state.scores = []
        st.session_state.start_time = time.time()
        st.rerun()

    if "questions" in st.session_state and st.session_state.current_q < 10:
        q = st.session_state.questions[st.session_state.current_q]
        st.subheader(f"Question {st.session_state.current_q + 1} ({q['difficulty']})")
        st.markdown(q["question"])

        if "start_time" not in st.session_state:
            st.session_state.start_time = time.time()

        elapsed = int(time.time() - st.session_state.start_time)
        remaining = max(0, 60 - elapsed)
        st.warning(f"⏳ Time remaining: {remaining} seconds")

        st.markdown("---")
        answer = st.text_area("✍️ Type your answer here (formula, explanation, or notes):")

        if st.button("Submit Answer") and answer.strip():
            score, feedback = evaluate_response(q["question"], answer)
            save_response(q, answer, score, feedback)
            st.session_state.responses.append(answer)
            st.session_state.scores.append(score)
            st.session_state.current_q += 1
            st.session_state.start_time = time.time()
            st.rerun()

    elif "questions" in st.session_state and st.session_state.current_q == 10:
        st.success("✅ Interview Completed!")
        report = generate_feedback(st.session_state.questions, st.session_state.responses, st.session_state.scores)
        st.download_button("📅 Download Feedback Report", report, file_name="Excel_Interview_Feedback.txt")

# --- MCQ TEST MODE ---
elif mode == "MCQ Test (30 mins)":
    st.header("📝 Multiple Choice Excel Test")
    st.info("30 questions · 30 minutes")
    st.warning("⚠️ MCQ functionality not yet implemented. GPT-generated MCQs and scoring logic coming soon!")
    st.write("\nIf you'd like, I can now add the full logic to generate MCQs via OpenAI, store them, track time, and score the test.")
