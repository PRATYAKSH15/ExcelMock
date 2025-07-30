def generate_feedback(questions, answers, scores):
    total = sum(scores)
    summary = f"Final Score: {total}/100\n\n"

    for i in range(10):
        summary += f"Q{i+1}: {questions[i]['question']}\n"
        summary += f"Answer: {answers[i]}\n"
        summary += f"Score: {scores[i]}/10\n\n"

    summary += "Thank you for participating!"
    return summary.encode("utf-8")
