from functions.llm import call_groq
from functions.prompts import qa_prompt, summary_prompt, quiz_prompt, planner_prompt, follow_up_prompt

def answer_question(vector_store, query):
    docs = vector_store.similarity_search(query, k=6)
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = qa_prompt(context, query)
    answer = call_groq(prompt)
    return answer, docs

def summarize_notes(vector_store):
    docs = vector_store.similarity_search("Give an overall summary of the document", k=6)
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = summary_prompt(context)
    answer = call_groq(prompt)
    return answer, docs

def generate_quiz(vector_store):
    docs = vector_store.similarity_search("important concepts and definitions", k=6)
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = quiz_prompt(context)
    answer = call_groq(prompt)
    return answer, docs

def create_study_plan(vector_store, query):
    docs = vector_store.similarity_search("topics covered in the lecture", k=6)
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = planner_prompt(context, query)
    answer = call_groq(prompt)
    return answer, docs

def handle_follow_up(last_response, query):
    prompt = follow_up_prompt(last_response, query)
    answer = call_groq(prompt)
    return answer