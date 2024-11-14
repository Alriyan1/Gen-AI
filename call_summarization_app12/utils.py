import whisper
from langchain.llms import OpenAI
from langchain.agents import initialize_agent
from langchain.agents.agent_toolkits import ZapierToolkit
from langchain.utilities.zapier import ZapierNLAWrapper
from langchain_google_genai import GoogleGenerativeAI


def email_summary(file):


    llm = GoogleGenerativeAI(temperature=0,model='gemini-pro')

    zapier = ZapierNLAWrapper()
    toolkit = ZapierToolkit.from_zapier_nla_wrapper(zapier)

    agent = initialize_agent(toolkit.get_tools(), llm, agent="zero-shot-react-description", verbose=True)


    model = whisper.load_model("base")

   

    result = model.transcribe(file)
    print(result["text"])

    agent.run("Send an Email to krippto7678@gmail.com via gmail summarizing the following text provided below : "+result["text"])


