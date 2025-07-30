QUESTION_GEN_PROMPT = """
You are an Excel interviewer. Generate 10 random Excel questions labeled with difficulty level (Medium or Advanced). Cover formulas, PivotTables, charts, Power Query, macros, etc. Output JSON list format:

[
  {"id": 1, "question": "...", "difficulty": "Medium"},
  ...
]
"""
