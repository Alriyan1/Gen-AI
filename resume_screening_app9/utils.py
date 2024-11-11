from langchain_google_genai import GoogleGenerativeAI
from langchain.vectorstores import Pinecone
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.schema import Document
from pinecone import Pinecone as PineconeClient
from pypdf import PdfReader
from langchain.chains.summarize import load_summarize_chain
from langchain.llms import HuggingFaceHub
import time


def get_pdf_text(pdf_doc):
    text=""
    pdf_reader=PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text+=page.extract_text()
    return text

def create_docs(user_pdf_list, unique_id):
    docs=[]
    for filenames in user_pdf_list:
        chunks=get_pdf_text(filenames)

        docs.append(Document(
            page_content=chunks,
            metadata={"name":filenames.name,"id":filenames.file_id,"type=":filenames.type,"size":filenames.size,"unique_id":unique_id},
        ))

    return docs

def create_embeddings_load_data():
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    return embeddings

def push_to_pinecone(pinecone_apikey,pinecone_environment,pinecone_index_name,embeddings,docs):
    PineconeClient(
        api_key=pinecone_apikey,
        environment=pinecone_environment
    )
    print('done......2')
    Pinecone.from_documents(docs,embeddings,index_name=pinecone_index_name)

def pull_from_pinecone(pinecone_apikey,pinecone_environment,pinecone_index_name,embeddings):
    PineconeClient(
        api_key=pinecone_apikey,
        environment=pinecone_environment
    )
    index_name=pinecone_index_name
    index=Pinecone.from_existing_index(index_name,embeddings)
    return index

def similar_docs(query,k,pinecone_apikey,pinecone_environment,pinecone_index_name,embeddings,unique_id):
    PineconeClient(
        api_key=pinecone_apikey,
        environment=pinecone_environment
    )
    index_name=pinecone_index_name
    index=pull_from_pinecone(pinecone_apikey,pinecone_environment,index_name,embeddings)
    similar_docs=index.similarity_search_with_score(query,int(k),{"unique_id":unique_id})
    return similar_docs

def get_summary(current_doc):
    llm=GoogleGenerativeAI(temperature=0,model='gemini-pro')
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summary = chain.run([current_doc])

    return summary