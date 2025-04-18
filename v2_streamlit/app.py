import streamlit as st
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Function to extract text from a webpage
def extract_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text()

# Function to summarize text using OpenAI
def summarize_text(text):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            { "role": "system", "content": "You are a helpful assistant that summarizes text." },
            { "role": "user", "content": f"Summarize this:
{text}" }
        ]
    )
    return response.choices[0].message.content

# Streamlit interface
st.title("🧠 Website Summarizer")

url = st.text_input("Enter website URL")

if url:
    with st.spinner("Fetching and summarizing..."):
        text = extract_text_from_url(url)
        summary = summarize_text(text)
        st.subheader("Summary")
        st.write(summary)