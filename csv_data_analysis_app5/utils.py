from langchain_experimental.agents import create_pandas_dataframe_agent
import pandas as pd
from langchain_google_genai import GoogleGenerativeAI

def query_agent(data,query):

    df = pd.read_csv(data)

    llm = GoogleGenerativeAI(model='gemini-pro')

    agent = create_pandas_dataframe_agent(llm, df, verbose=True,allow_dangerous_code=True)


    return agent.run(query)