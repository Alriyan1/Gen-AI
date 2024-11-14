import streamlit as st
from utils import *

def main():
    st.title('Call Summarization')

    upload_files = st.file_uploader('Upload recorded .mp3 files',type = ['mp3'],accept_multiple_files=True)

    if upload_files:
        st.write('Uploaded Files:')

        for file in upload_files:
            filename = file.name

            col1,col2,col3 = st.columns([0.1,1,2])
            with col1:
                st.write("-")
            with col2:
                st.write(filename)
            with col3:
                send_button = st.button(f"Send Email for {filename}")

                if send_button:
                    email_summary(filename)
                    st.success(f"Send email for {filename}")


if __name__=="__main__":
    main()