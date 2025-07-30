from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

from prompts.question_prompt import QUESTION_GEN_PROMPT
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_questions():
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": QUESTION_GEN_PROMPT}
        ]
    )
    return json.loads(response.choices[0].message.content)
