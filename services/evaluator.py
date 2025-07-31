import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
from prompts.evaluation_prompt import EVALUATION_PROMPT
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def evaluate_response(question, answer):
    prompt = EVALUATION_PROMPT.format(question=question, answer=answer)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    result = json.loads(response.choices[0].message.content)
    return result['score'], result['feedback']
