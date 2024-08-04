# import streamlit as st 
# from utils import print_messages 
# from langchain_core.messages import ChatMessage
# from langchain.chains import ConversationalRetrievalChain
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.chat_history import BaseChatMessageHistory 
# from langchain_core.runnables.history import RunnableWithMessageHistory
# from langchain_community.chat_message_histories import ChatMessageHistory
# from langchain_core.runnables import RunnablePassthrough
# import os 
# from gemini import llm_model
# from prompt import chat_prompt
# from dataloader import page_content 
# from embeddings import text_split , vector_store
# from retriever import retriever


# st.set_page_config(page_title = "ChatBot" , page_icon = "🗨️")
# st.title("🗨️ BookMark Chatbot") 

# os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

# #session state를 사용해서 data를 계속 기록하는 코드 (캐싱)
# if "messages" not in st.session_state : #session state에 messages 라는 key 값이 없으면,
#     st.session_state['messages'] = [] #리스트 형식으로 새로 생성 

# if "store" not in st.session_state :
#     st.session_state["store"] = dict()
    
# with st.sidebar : 
#     session_id = st.text_input("Session ID" , value = "abc123") #카톡방 ID와 같은 개념
#     #anthropic_api_key = st.text_input("Gemini API Key", key="file_qa_api_key", type="password")
#     clear_btn = st.button("대화기록 초기화") 
    
#     if clear_btn : 
#         st.session_state["message"]  = [] 
#         #st.seesion_state['store'] = dict() -> 이전 대화 기록들도 모두 초기화 하고 싶을 경우 
#         st.experimental_rerun() #새로고침
           
# #이전 대화기록 출력 코드 
# print_messages() 


# #세션ID를 기반으로 세션 기록을 가져오는 함수 
# def get_session_history(session_ids : str) -> BaseChatMessageHistory :
#     if session_ids not in st.session_state["store"] : #세션 ID가 store에 없는 경우 
#         #새로운 ChatMessageHistory 객체를 생성하여 store에 저장 
#         st.session_state["store"][session_ids] = ChatMessageHistory() 
#     return st.session_state["store"][session_ids] #해당 세션ID에 대한 세션 기록 반환


# if user_input := st.chat_input("메세지를 입력해 주세요.") :
#     #사용자가 입력한 내용 
#     st.chat_message('user').write(f'{user_input}') #user message 입력 -> 입력을 하게 되면 새로고침 된다. (수동으로 구현하기) 
#     #st.session_state['messages'].append(("user" , user_input))
#     st.session_state['messages'].append(ChatMessage(role = "user" , content=user_input)) #코드가 조금 더 명확함.
    
#     #AI의 답변 
#     with st.chat_message("assistant") :
        
#         api_key = 'AIzaSyCtUU0L03NUTda15zkyYbPTakuXt6k1Xjs'

#         if "GOOGLE_API_KEY" not in os.environ:
#             os.environ["GOOGLE_API_KEY"] = api_key
        
#         #1. 사용자 url 넣기 
#         urls = ["https://www.youtube.com/watch?v=ulMzXgPmPhY&list=RD_Ra1M4uYdTI&index=23",
#         "https://www.youtube.com/watch?v=cuHInDaF8WA"]
        
#         #2. content loader
#         docs = page_content(urls)
        
#         #3. split 및 embedding 
#         splits = text_split(docs)
        
#         #4.vector store
#         vectorstore = vector_store(splits)
        
#         #5.retreiver 설정 
#         chat_rt = retriever( vectorstore = vectorstore)
        
#         #6.모델생성 
#         llm = llm_model()
#         #llm = ChatOpenAI(streaming = True , callbacks = [stream_handler]) 
        
#         #7.프롬프트 생성 
#         prompt = chat_prompt()
        
#         def format_docs(docs):
#         # 검색한 문서 결과를 하나의 문단으로 합쳐줍니다.
#             return "\n\n".join(doc.page_content for doc in docs)
        
#         #8. 체인생성 
#         rag_chain = (
#             {"context": chat_rt | format_docs , "question": RunnablePassthrough() }
#             | prompt
#             | llm
#             | StrOutputParser()
#         )   
    
#         # 9. 대화기록 저장 
#         chain_with_memory = (
#             RunnableWithMessageHistory(         #RunnableWithMessageHistory 객체 생성 
#                 rag_chain , #실행할 Runnable 객체 
#                 get_session_history, #세션 기록을 가져오는 함수
#                 input_messages_key="question", # 사용자 질문의 키 
#                 history_messages_key="history" # 기록 메시지의 키 
#             )
#         )

#         response_stream = chain_with_memory.stream(
#                 #사용자의 질문을 입력
#                 {"question" : user_input} , 
#                 #세션 ID 설정 
#                 config = {"configurable" : {"session_id" : session_id}})

#         # msg ="" 
#         # response_placeholder = st.empty()
        
#         # for chunk in response_stream :
#         #     msg += chunk.content
#         #     response_placeholder.markdown(msg)
        
#         #response = rag_chain.stream(user_input)
#         st.write(response_stream) #-> 실시간으로 찍히므로 필요 X 
#         st.session_state['messages'].append(ChatMessage(role = "assistant" , content=response_stream))
