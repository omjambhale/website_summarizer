#!/usr/bin/env python
# coding: utf-8

# In[41]:


import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
from openai import OpenAI

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


# In[42]:


load_dotenv(override = True)
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("No API key was found!")
elif not api_key.startswith("sk-proj-"):
    print("An API key was found, but it doesn't start with sk-proj-; please check the key!")
elif api_key.strip() != api_key:
    print("An API key was found, but it looks like it might have space and tab characters ate the start or end!")
else:
    print("API key found, looks good so far!")


# In[43]:


# lets make a quick call to a frontier model to get started, as a preview!
openai = OpenAI()
message = "Hello, GPT! This is my first ever message to you! Hi!"
response = openai.chat.completions.create(
    model= "gpt-4o-mini", 
    messages=[
        {
            "role":"user", 
         "content":message
        }
    ]
)
print(response.choices[0].message.content)


# In[44]:


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class Website:
    def __init__(self, url):
        self.url = url

        options = Options()
        options.add_argument("--headless")  # run browser in background
        driver = webdriver.Chrome(options=options)

        driver.get(url)
        time.sleep(3)  # wait for JavaScript to finish loading

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        self.title = soup.title.string if soup.title else "No title found"

        for tag in soup(["script", "style", "img", "input"]):
            tag.decompose()

        self.text = soup.body.get_text(separator="\n", strip=True)


# In[45]:


ed = Website("https://en.wikipedia.org/wiki/Perplexity_AI")
print(ed.title)


# In[46]:


system_prompt = "You are an assistant that analyzes the contents of a website \
and provides a short summary, ignoring text that might be navigation related. \
Respond in markdown."


# In[47]:


def user_prompt_for(website):
    user_prompt = f"You are looking at a website titled {website.title}"
    user_prompt += "\nThe contents of this website is as follows; \
please provide a short summary of this website in markdown. \
If it includes news or announcements, then summarize these too.\n\n"

    user_prompt += website.text
    return user_prompt


# In[48]:


# print(user_prompt_for(ed))


# In[49]:


messages = [
    {"role": "system", "content" : "You are a snarky assistent"},
    {"role" : "user", "content" : "What is 2 + 2 ?"}
]


# In[50]:


response = openai.chat.completions.create(model = "gpt-4o-mini", messages = messages)
print(response.choices[0].message.content)


# In[51]:


def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content" : user_prompt_for(website)}
    ]


# In[52]:


# messages_for(ed)


# In[53]:


def summarize(url):
    website = Website(url)
    response = openai.chat.completions.create(
        model = "gpt-4o-mini",
        messages = messages_for(website)
    )
    return response.choices[0].message.content


# In[54]:


summarize("https://en.wikipedia.org/wiki/Perplexity_AI")


# In[ ]:





# In[ ]:





# In[ ]:




