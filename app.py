#import dependencies
import os 
from apikey import apikey
import langchain
import streamlit as st 
import time
import pandas as pd

from langchain.llms import OpenAI

from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from langchain.chains import LLMChain
os.environ['OPENAI_API_KEY'] = apikey

#App framework

st.title ('The NPS label tool 😄🥲😊')
st.markdown("""
Introducing our AI-powered feedback analysis tool, designed to unlock customer insights at scale. Utilizing the power of OpenAI's GPT-3, our tool automates the process of deciphering customer sentiment and identifying key themes from your feedback data. It's built to save time, enhance understanding, and empower businesses to act on customer insights faster than ever before. With our tool, make every piece of feedback count!
""")
#NPSanswer = st.text_input(' **Enter your NPS open answer** ')

#Chatmodel

chat_model= ChatOpenAI(temperature=0.9, model="gpt-3.5-turbo")

#Prompt template

system_message_prompt = SystemMessagePromptTemplate.from_template("Pretend you're a customer journey specialist who is an expert in labeling customer feedback.")
human_message_prompt = HumanMessagePromptTemplate.from_template(" ##Context For the consumer electronics store of Coolblue, we receive feedback on how an appointment in one of our stores has gone. ##Assignment In the following assignment, you need to derive from the given text the reasons why they are not satisfied and process this into labels. Use a maximum of 5 labels for all combined answers. Focus the labeling on the cause of the dissatisfaction. Also provide an explanation of the label, keep general and do not use specific examples. Also provide a weight to each label according to how much it is mentioned in the answers. Use 100 points to divide over the 5 labels.   ##FormatMake sure the labels are as short and concrete as possible.  Use only English language to create labels. ##Input Label the following NPS input {NPSanswer}")
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

 #LLM CHain

nps_chain = LLMChain(llm=chat_model, prompt=chat_prompt, verbose = True)

# This line will allow the user to upload an Excel file
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

# This line will convert the uploaded file into a pandas DataFrame
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.write(df)  # Optional: This will display the DataFrame in the app

# Combine all feedback stories into a single string
    feedback_text = '\n'.join(df['Feedback'].astype(str))
    NPSanswer = feedback_text
    #NPSanswer = st.text_input(' **Enter your NPS open answer** ', value=feedback_text)
    
# Show stuff on the screen when there is a prompt 
if st.button('Generate'):
    try:
        if NPSanswer:
            response = nps_chain.run({"NPSanswer": NPSanswer})
            st.write(response)
    except Exception as e:
        st.error(f"An error occurred: {e}")

    # This line will create a new column 'insights' in the DataFrame
    # It will apply the OpenAI model to the combined feedback text
    #if NPSanswer:
        #df['insights'] = nps_chain.run({"NPSanswer": NPSanswer})
        #top_insights = df.sort_values('insights').head(8)
        #st.write(top_insights)











# This line will create a new column 'insights' in the DataFrame
# It will apply the OpenAI model to each row of the 'feedback' column
# Replace 'feedback' with the name of the column that contains the feedback
##if uploaded_file is not None:
##    df['insights'] = df['feedback'].apply(lambda x: nps_chain.run({"NPSanswer": x}))

# This line will sort the DataFrame by the 'insights' column and return the top 8 rows
# You may need to modify this line to fit your use case
# For example, if 'insights' contains numeric values, you might want to sort in descending order
# If 'insights' contains text, you might need a different method to determine the "top" insights
##if uploaded_file is not None:
##    top_insights = df.sort_values('insights').head(8)
##    st.write(top_insights)


#uploaded_file = st.file_uploader("Choose a file")

#if uploaded_file is not None:
    # To read file as bytes:
    #bytes_data = uploaded_file.getvalue()
    # To convert to a string based on the file type, here assuming it's a text file:
    #string_data = uploaded_file.getvalue().decode()
    #st.write(string_data)
