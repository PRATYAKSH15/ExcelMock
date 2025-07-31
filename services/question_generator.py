from openai import OpenAI
import os
import json
from dotenv import load_dotenv
load_dotenv()

from prompts.question_prompt import QUESTION_GEN_PROMPT

# Load your OpenAI API key from the environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_questions():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an Excel interview question generator."},
            {"role": "user", "content": QUESTION_GEN_PROMPT}
        ]
    )
    return json.loads(response.choices[0].message.content)

def generate_mcq_questions():
    mcq_prompt = """
    You are an Excel test maker. Generate 30 random Excel MCQs. Each question must be labeled with difficulty ("Medium" or "Advanced"), have 4 options, and specify the correct answer.
    Return as a JSON list like:
    [
      {
        "question": "What does the VLOOKUP function do?",
        "options": ["Finds a value in a column", "Finds a value in a row", "Adds values", "None"],
        "answer": "Finds a value in a column",
        "difficulty": "Medium"
      },
      ...
    ]
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an Excel MCQ generator."},
            {"role": "user", "content": mcq_prompt}
        ]
    )
    return json.loads(response.choices[0].message.content)
