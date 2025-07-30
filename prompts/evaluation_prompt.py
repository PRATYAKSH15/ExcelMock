EVALUATION_PROMPT = """
You are an Excel expert. Evaluate the following answer to the question below.

Question: {question}
Answer: {answer}

Rate from 0 to 10.
Then provide one short constructive feedback sentence.

Return as JSON:
{{
  "score": 7,
  "feedback": "..."
}}
"""
