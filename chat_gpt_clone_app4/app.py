import streamlit as st
from streamlit_chat import message
from langchain.chains import LLMChain,ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory,ConversationBufferWindowMemory,ConversationSummaryMemory
import tiktoken
from langchain.memory import ConversationTokenBufferMemory

from langchain_google_genai import GoogleGenerativeAI

if "conversation" not in st.session_state:
    st.session_state['conversation']=None
if "messages" not in st.session_state:
    st.session_state['messages']=[]
if "API_Key" not in st.session_state:
    st.session_state['API_Key']=''

# setting page title and header
st.set_page_config(page_title="Chat GPT Clone", page_icon=":robot:")
st.markdown("<h1 style='text-align: center;'>How can I assist you? </h1>", unsafe_allow_html=True)


st.sidebar.title("😎")
st.session_state['API_Key']=st.sidebar.text_input('What is your API key?',type='password')
summarise_button = st.sidebar.button("Summarise the conversatsion",key='summarise')
if summarise_button:
    summarise_placeholder=st.sidebar.write('Nice chatting with you my friend ❤️:\n\n'+st.session_state['conversation'].memory.buffer)



def getresponse(userInput,api_key):
    if st.session_state['conversation'] is None:
        
        llm = GoogleGenerativeAI(temperature=0,
                                 google_api_key=api_key,
                                 model='gemini-pro')
        
        st.session_state['conversation'] = ConversationChain(
            llm=llm,
            verbose=True,
            memory=ConversationSummaryMemory(llm=llm)
        )
    
    
    response=st.session_state['conversation'].predict(input=userInput)
    print(st.session_state['conversation'].memory.buffer)
    return response

response_container = st.container()

container = st.container()

with container:
    with st.form(key='my_form',clear_on_submit=True):
        user_input=st.text_area('Your question goes here:', key='input',height=100)
        submit_button=st.form_submit_button(label='Send')
        if submit_button:
            st.session_state['messages'].append(user_input)
            answer=getresponse(user_input,st.session_state['API_Key'])
            st.session_state['messages'].append(answer)

            with response_container:
                for i in range(len(st.session_state['messages'])):
                    if i%2 == 0:
                        message(st.session_state['messages'][i] ,is_user=True, key=str(i)+"_user")
                    else:
                        message(st.session_state['messages'][i] , key=str(i)+"_AI")

