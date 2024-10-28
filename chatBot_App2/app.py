import streamlit as st

from langchain.schema import AIMessage,HumanMessage,SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI 


st.set_page_config(page_title="LangChain Demo", page_icon=":robot:")
st.header("Hey, I am your Chat GPT")

if 'sessionMessages' not in st.session_state:
    st.session_state.sessionMessages=[
        SystemMessage(content="You are a helpful assistent")
    ]

def load_answer(question):
    st.session_state.sessionMessages.append(HumanMessage(content=question))
    assistant_answer = chat(st.session_state.sessionMessages)
    st.session_state.sessionMessages.append(AIMessage(content=assistant_answer.content))
    return assistant_answer.content

def get_text():
    input_text = st.text_input("You: ",key="input")
    return input_text


chat = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-002",
    temperature=0.7,
)

user_input=get_text()
submit= st.button('Generate')

if submit:
    response = load_answer(user_input)
    st.subheader("Answer:")

    st.write(response,key = 1)
    