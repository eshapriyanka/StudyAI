def qa_prompt(context, question):
    return f"""
You are a helpful academic assistant.

Answer the question ONLY from the context below.
If the answer is not present, say:
"I could not find this in the uploaded notes."

Also:
- Explain clearly
- Use simple language
- Give short examples if possible

Context:
{context}

Question:
{question}
"""

def summary_prompt(context):
    return f"""
You are a helpful study assistant.

Summarize the following lecture notes in a clean way.

Include:
- Main topics
- Important definitions
- Key takeaways
- Exam-focused points

Notes:
{context}
"""

def quiz_prompt(context):
    return f"""
You are a quiz generator.

Based on the notes below, generate 5 multiple-choice questions.

For each question include:
- Question
- 4 options
- Correct answer
- 1-line explanation

Notes:
{context}
"""

def planner_prompt(context, query):
    return f"""
You are a study planning assistant.

Based on the lecture notes and the user's request, create a practical study plan.

User request:
{query}

Lecture notes:
{context}

Create a simple day-wise study plan.
"""

def follow_up_prompt(last_response, user_query):
    return f"""
You are a helpful study assistant.

The user is asking a follow-up question based on the previous response.

Previous response:
{last_response}

Follow-up request:
{user_query}

Modify or improve the previous response according to the user's request.
Be clear, accurate, and student-friendly.
"""