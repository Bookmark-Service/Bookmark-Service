from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder 


# #챗봇 prompt 
# def rag_prompt() : 
#     prompt = ChatPromptTemplate.from_messages(
#         [
#             (
#                 "system" ,
#                 "질문에 간결하고 명확하게 답변하세요."
#             ),
#                 #대화기록을 변수로 사용 , history가 MessageHistory의 Key가 된다. 
#                 MessagesPlaceholder(variable_name="history") ,
#                 ("human" , "{question}"), #사용자의 입력을 변수로 사용 
#         ]
#         )
#     return prompt

def chat_prompt() : #챗봇 prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are a helpful assistant. 
                Answer questions using only the following context. 
                If you don't know the answer just say you don't know, don't make it up:
                \n\n
                {context}",
                """
            ),
            ("human", "{question}"),
        ]
    )
    return prompt