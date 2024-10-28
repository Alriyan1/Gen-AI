import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import pandas as pd
from tensorflow.keras.losses import cosine_similarity

st.set_page_config(page_title="Educate Kids", page_icon=":robot:")
st.header("Hey, Ask me anything & I will give out similar things")

embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")

df=pd.read_csv('mydata.csv')

df["embeddings"]=df['words'].apply(lambda x: embeddings.embed_query(x))

def get_text():
    input_text=st.text_input("You: ", key=input)
    return input_text

user_input=get_text()

submit=st.button("Find similar Things")

if submit:
    text_embedding = embeddings.embed_query(user_input)
    df["similarity_score"]=df['embeddings'].apply(lambda x:cosine_similarity(x,text_embedding).numpy())
    df=df.sort_values('similarity_score',ascending=True).head(2)['words'].tolist()
    st.subheader("Top Matches:")
    st.text(df[0])
    st.text(df[1])