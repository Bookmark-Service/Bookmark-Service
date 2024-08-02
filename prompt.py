from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder 

def summary(text) :
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a specialized tool for summarizing documents.",
            ),
            (
                "human", 
                '''
                내가 제공하는 문서는 웹사이트의 body를 모두 긁어온거야. 
                문서를 5줄 이내의 한국어 문장으로 간결하게 요약해줘. 
                요약된 문장은 문서의 핵심 내용만 포함해야 하고, 핵심 내용과 관련 없는 문장은 제외해야 해. 
                광고나 목차가 있을 수 있지만 본문만 고려해야 해.
                '''
            ),
            (
                "human", 
                {text}
            )
        ]
    )

    return prompt

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