import sys
import os
import time
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from services.question_generator import generate_questions, generate_mcq_questions
from services.evaluator import evaluate_response
from services.feedback_generator import generate_feedback
from db.database import save_response, init_db
from session import initialize_session_state
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Excel Mock Interviewer", layout="wide")
st.sidebar.title("🧪 Interview Modes")
mode = st.sidebar.radio("Choose a mode:", ["Text Interview", "MCQ Test (30 mins)"])

st.title("AI-Powered Excel Mock Interviewer: Test Your Skills!")

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
    st.info("20 questions · 30 minutes")

    if st.button("🚀 Start MCQ Test"):
        max_retries = 3
        mcqs = []
        for attempt in range(max_retries):
            mcqs = generate_mcq_questions()
            if len(mcqs) >= 20:
                mcqs = mcqs[:20]
                break

        if len(mcqs) < 20:
            st.error(f"⚠️ Only {len(mcqs)} questions generated after {max_retries} attempts. Please try again.")
        else:
            st.session_state.mcq_questions = mcqs
            st.session_state.mcq_current_q = 0
            st.session_state.mcq_score = 0
            st.session_state.mcq_answers = []
            st.session_state.mcq_start_time = time.time()
            st.rerun()

    if "mcq_questions" in st.session_state and st.session_state.mcq_current_q < len(st.session_state.mcq_questions):
        q = st.session_state.mcq_questions[st.session_state.mcq_current_q]
        st.subheader(f"Question {st.session_state.mcq_current_q + 1} ({q['difficulty']})")
        st.markdown(q["question"])
        selected = st.radio("Select your answer:", q["options"], key=f"mcq_{st.session_state.mcq_current_q}")

        elapsed = int(time.time() - st.session_state.mcq_start_time)
        remaining = max(0, 1800 - elapsed)
        mins, secs = divmod(remaining, 60)
        st.warning(f"⏳ Time remaining: {mins:02}:{secs:02}")

        if st.button("Submit MCQ Answer"):
            is_correct = selected == q["answer"]
            st.session_state.mcq_score += int(is_correct)
            st.session_state.mcq_answers.append({
                "question": q["question"],
                "selected": selected,
                "correct": q["answer"]
            })
            st.session_state.mcq_current_q += 1
            st.rerun()

    elif "mcq_questions" in st.session_state and st.session_state.mcq_current_q == len(st.session_state.mcq_questions):
        st.success("🎉 MCQ Test Completed!")
        st.markdown(f"**Your Score: {st.session_state.mcq_score}/20**")
        with st.expander("🧾 Review Your Answers"):
            for idx, a in enumerate(st.session_state.mcq_answers):
                st.write(f"Q{idx+1}: {a['question']}")
                st.write(f"Your Answer: {a['selected']}")
                st.write(f"Correct Answer: {a['correct']}")
                st.markdown("---")
