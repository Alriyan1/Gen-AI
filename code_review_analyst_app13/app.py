from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
from io import StringIO
from langchain.schema import HumanMessage,SystemMessage
import time
import base64

st.title("Let's do code review for your python code")
st.header('Please upload your .py file here:')

def text_downloader(raw_text):
    # Generate a timestamp for the filename to ensure uniqueness
    timestr = time.strftime("%Y%m%d-%H%M%S")
    
    # Encode the raw text in base64 format for file download
    b64 = base64.b64encode(raw_text.encode()).decode()
    
    # Create a new filename with a timestamp
    new_filename = "code_review_analysis_file_{}_.txt".format(timestr)
    
    st.markdown("#### Download File ✅###")
    
    # Create an HTML link with the encoded content and filename for download
    href = f'<a href="data:file/txt;base64,{b64}" download="{new_filename}">Click Here!!</a>'
    
    # Display the HTML link using Streamlit markdown
    st.markdown(href, unsafe_allow_html=True)

data=st.file_uploader('Upload python file',type = ".py")

if data:
    stringio = StringIO(data.getvalue().decode('utf-8'))

    fetched_data=stringio.read()

    st.write(fetched_data)


    chat = ChatGoogleGenerativeAI(model='gemini-1.5-pro',temperature=0.9)

    systemMessage = SystemMessage(content="You are a code review assistant. Provide detailed suggestions to improve the given python code along by mentioning the existing code line by line with proper indent")

    humanMessage = HumanMessage(content=fetched_data)

    finalResponse = chat([systemMessage, humanMessage])

    st.markdown(finalResponse.content)

    text_downloader(finalResponse.content)