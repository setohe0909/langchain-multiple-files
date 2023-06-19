import streamlit as st

from dotenv import load_dotenv

from utils.methods import  get_pdf_text, get_text_chunks, get_vectorstore, get_conversation_chain, handle_userinput
from utils.htmlTemplates import  css

def main():
  load_dotenv()
  st.set_page_config(page_title='Chat with multiples PDFs', page_icon=":books:")
  st.write(css, unsafe_allow_html=True)

  if "conversation" not in st.session_state:
    st.session_state.conversation = None
  if "chat_history" not in st.session_state:
    st.session_state.chat_history = None

  st.header('Chat with multpiples PDFs :books:')
  user_question = st.text_input("Ask a question about your documents:")

  if user_question:
    handle_userinput(user_question)

  with st.sidebar:
    st.subheader("Your Documents")
    pdf_docs = st.file_uploader(
      "Upload your PDFs Here and click on Process", accept_multiple_files=True)

    if st.button("Proccess"):
       with  st.spinner("Processing"):
        # Get pdf text
        raw_text = get_pdf_text(pdf_docs)
        # st.write(raw_text) # --> Show the output for each PDF
        # ---------------------------

        # Get the text chunks
        text_chunks = get_text_chunks(raw_text)
        # st.write(text_chunks) # --> Show the output for each chunk
        # ---------------------------

        # Create vector store  
        # Embeding models with open-ai  - it has a cost
        vectorstore = get_vectorstore(text_chunks)

        # create conversation chain
        st.session_state.conversation = get_conversation_chain(vectorstore)


if __name__ == '__main__':
    main()
