from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.tools import DuckDuckGoSearchRun
from langchain_google_genai import GoogleGenerativeAI

def generate_script(prompt,video_length,creativity,api_key):

    title_template = PromptTemplate(
        input_variable = ['subject'],
        template = 'Please come up with a title for a youtube video on the {subject}.'
    )

    script_template = PromptTemplate(
        input_variable = ['title','DuckDuckGo_Search','duration'],
        template = "Create a script for a youtube video based on this title for me. TITLE: {title} of duration: {duration} minutes using this search data {DuckDuckGo_Search}"
    )

    llm = GoogleGenerativeAI(temperature=creativity,google_api_key=api_key,model = "gemini-pro")

    title_chain = LLMChain(llm=llm, prompt=title_template,verbose = True)
    script_chain = LLMChain(llm=llm, prompt=script_template,verbose = True)

    search = DuckDuckGoSearchRun()

    title = title_chain.run(prompt)
    search_result = search.run(prompt)
    script = script_chain.run(title=title,DuckDuckGo_Search=search_result,duration = video_length)

    return search_result,title,script