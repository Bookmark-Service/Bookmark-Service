import os 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from prompt import chat_prompt 

def llm_model() : 
    llm=ChatGoogleGenerativeAI(model ='gemini-1.5-flash')
    return llm 


def get_conversation_chain(vetorestore):
    llm = ChatGoogleGenerativeAI(model ='gemini-1.5-flash')
    conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm, 
            chain_type="stuff", 
            retriever=vetorestore.as_retriever(search_type = 'mmr', vervose = True), 
            memory=ConversationBufferMemory(memory_key='chat_history', return_messages=True, output_key='answer'),
            get_chat_history=lambda h: h,
            return_source_documents=True,
            verbose = True
        )

    return conversation_chain