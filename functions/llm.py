import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

def call_groq(prompt, model="llama-3.1-8b-instant"):    
    """
    Send prompt to Groq and return model response.
    """
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content