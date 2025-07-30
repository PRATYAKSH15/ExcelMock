import streamlit as st

def initialize_session_state():
    if "current_q" not in st.session_state:
        st.session_state.current_q = 0
    if "responses" not in st.session_state:
        st.session_state.responses = []
    if "scores" not in st.session_state:
        st.session_state.scores = []
