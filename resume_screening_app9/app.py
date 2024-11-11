import streamlit as st
import uuid
from utils import *

if 'unique_id' not in st.session_state:
    st.session_state['unique_id']=""

def main():

    st.set_page_config(page_title="Resume Screening Assistance")
    st.title("HR - Resume Screening Assistance...🧞")
    st.subheader("I can help you in resume screening process")

    job_description = st.text_area("Please paste the 'JOB DESCRIPTION' here...",key='1')
    document_count=st.text_input("No.of 'RESUME' to return",key='2')

    pdf=st.file_uploader('Upload resumes here, only PDF files allowed',type=['pdf'],accept_multiple_files=True)

    submit=st.button('Help me with the analysis')

    if submit:
        with st.spinner("Wait for it..."):

            st.session_state['unique_id']=uuid.uuid4().hex

            docs = create_docs(pdf,st.session_state['unique_id'])
            #st.write(docs)

            st.write(len(docs))

            embeddings=create_embeddings_load_data()

            push_to_pinecone("***********************","gcp-starter","test",embeddings,docs)

            relavant_docs=similar_docs(job_description,document_count,"*******************",'gcp-starter','test',embeddings,st.session_state['unique_id'])

            #st.write(relavant_docs)
            st.write(":heavy_minus_sign:" * 30)

            for item in range(len(relavant_docs)):
                
                st.subheader("👉 "+str(item+1))

                #Displaying Filepath
                st.write("**File** : "+relavant_docs[item][0].metadata['name'])

                #Introducing Expander feature
                with st.expander('Show me 👀'): 
                    st.info("**Match Score** : "+str(relavant_docs[item][1]))
                    #st.write("***"+relavant_docs[item][0].page_content)
                    
                    #Gets the summary of the current item using 'get_summary' function that we have created which uses LLM & Langchain chain
                    summary = get_summary(relavant_docs[item][0])
                    st.write("**Summary** : "+summary)
            #st.write("Our process")

        st.success('Hope I was able to save your time❤️')

if __name__=="__main__":
    main()
    