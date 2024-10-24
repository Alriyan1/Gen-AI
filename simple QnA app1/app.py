import streamlit as st

# from langchain_openai import OpenAI
from langchain_huggingface import HuggingFaceEndpoint

def load_answer(question):
    llm = HuggingFaceEndpoint(repo_id = "mistralai/Mistral-7B-Instruct-v0.3")

    answer = llm.invoke(question)
    return answer


st.set_page_config(page_title='Langchain Demo', page_icon=':robot:')
st.header("Langchain Demo")

def get_text():
    input_text=st.text_input('You: ',key="input")
    return input_text
user_input=get_text()

submit = st.button("Generate")

if submit and user_input:
    response = load_answer(user_input)
    st.subheader("Answer:")
    st.write(response)
