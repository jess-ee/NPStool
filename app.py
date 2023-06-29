#import dependencies
import os 
import langchain
import streamlit as st 
import time

from langchain.llms import OpenAI

from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from langchain.chains import LLMChain
apikey = os.getenv('OPENAI_API_KEY')

#App framework

st.title ('The NPS label tool 😄🥲😊')
st.markdown("""
Introducing our AI-powered feedback analysis tool, designed to unlock customer insights at scale. Utilizing the power of OpenAI's GPT-3, our tool automates the process of deciphering customer sentiment and identifying key themes from your feedback data. It's built to save time, enhance understanding, and empower businesses to act on customer insights faster than ever before. With our tool, make every piece of feedback count!
""")
NPSanswer = st.text_input(' **Enter your NPS open answer** ')

#Chatmodel

chat_model= ChatOpenAI(temperature=0.9, model="gpt-3.5-turbo")

#Prompt template

system_message_prompt = SystemMessagePromptTemplate.from_template("Pretend you're a customer journey specialist who is an expert in labeling customer feedback.")
human_message_prompt = HumanMessagePromptTemplate.from_template("**Context**For the consumer electronics store of Coolblue, we receive feedback on how an appointment in one of our stores has gone. **Assignment** In the following assignment, you need to derive from the given text the reasons why they are not satisfied and process this into labels. Use a maximum of 3 labels per answer. If fewer labels are needed, use fewer. Focus the labeling on the cause of the dissatisfaction. **Format**Make sure the labels are as short and concrete as possible. Separate the labels with commas. Use only English language to create labels. **Example** Label, Label, Label' **Input** Label the following NPS input {NPSanswer} ")
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

 #LLM CHain

nps_chain = LLMChain(llm=chat_model, prompt=chat_prompt, verbose = True)

# Show stuff on the screen when there is a prompt 
if st.button('Generate'):
    try:
        if NPSanswer:
            response = nps_chain.run({"NPSanswer": NPSanswer})
            st.write(response)
    except Exception as e:
        st.error(f"an error occurred:{e}")








#uploaded_file = st.file_uploader("Choose a file")

#if uploaded_file is not None:
    # To read file as bytes:
    #bytes_data = uploaded_file.getvalue()
    # To convert to a string based on the file type, here assuming it's a text file:
    #string_data = uploaded_file.getvalue().decode()
    #st.write(string_data)
