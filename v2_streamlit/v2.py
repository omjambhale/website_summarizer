#!/usr/bin/env python
# coding: utf-8

# In[11]:


import streamlit as st
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from openai import OpenAI


# In[12]:


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


# In[13]:


def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text()
    except Exception as e:
        return f"Failed to extract text: {e}"


# In[14]:


def summarize_text(text):
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": f"Summarize this:\n{text}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Failed to summarize: {e}"


# In[15]:


st.set_page_config(page_title="Website Summarizer", page_icon="🧠")
st.title("🧠 Website Summarizer")

url = st.text_input("Enter website URL")

if url:
    with st.spinner("⏳ Fetching and summarizing..."):
        text = extract_text_from_url(url)
        summary = summarize_text(text)
        st.subheader("Summary:")
        st.write(summary)

