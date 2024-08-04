import streamlit as st 
from gemini import get_conversation_chain
from langchain.memory import StreamlitChatMessageHistory
from langchain.callbacks import get_openai_callback
from prompt import chat_prompt
from dataloader import page_content 
from embeddings import text_split , vector_store
from retriever import retriever

st.set_page_config(
    page_title="북마크 Chat",
    page_icon=":books:")

st.title("_BookMark :red[QA Chat]_ 🤔")

if "conversation" not in st.session_state:
        st.session_state.conversation = None

if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

if "processComplete" not in st.session_state:
        st.session_state.processComplete = None


if 'messages' not in st.session_state:
    st.session_state['messages'] = [{"role": "assistant", "content": "안녕하세요! 궁금한 것이 있으면 언제든지 물어봐주세요!"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

history = StreamlitChatMessageHistory(key="chat_messages")

# Chat logic
if user_input := st.chat_input("질문을 입력해주세요."):
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)
    
    #user url이 들어가는 곳 
    urls = ["https://www.youtube.com/watch?v=ulMzXgPmPhY&list=RD_Ra1M4uYdTI&index=23", "https://www.youtube.com/watch?v=cuHInDaF8WA"]
    
    splits = page_content(urls)
    chunks =  text_split(splits)
    vetorestore = vector_store(chunks)
    st.session_state.conversation = get_conversation_chain(vetorestore) 
    st.session_state.processComplete = True

    with st.chat_message("assistant"):
        chain = st.session_state.conversation

        with st.spinner("Thinking..."):
            result = chain({"question": user_input})
            with get_openai_callback() as cb:
                st.session_state.chat_history = result['chat_history']
            response = result['answer']
            source_documents = result['source_documents']
            
            st.session_state.messages.append({"role": "assistant", "co  ntent": response})

            st.markdown(response)
            with st.expander("참고 문서 확인"):
                st.markdown(source_documents[0].metadata['source'], help = source_documents[0].page_content)
                st.markdown(source_documents[1].metadata['source'], help = source_documents[1].page_content)
                st.markdown(source_documents[2].metadata['source'], help = source_documents[2].page_content)