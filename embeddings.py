from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import tiktoken

def tiktoken_len(text):
    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = tokenizer.encode(text)
    return len(tokens)

def text_split(docs) :
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, 
                                                   chunk_overlap=10,
                                                   length_function = tiktoken_len)
    splits = text_splitter.split_documents(docs)
    return splits

def vector_store(splits) :
    vectorstore = FAISS.from_documents(documents=splits,
                                       embedding = GoogleGenerativeAIEmbeddings(model = "models/embedding-001"))
    return vectorstore

