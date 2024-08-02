from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import tiktoken
from db import get_db
from models import Bookmark, ContentEmbedding
from sqlalchemy.orm import Session
from datetime import datetime   

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

def store_embeddings(bookmark_id, embedding, db: Session):
    new_embedding = ContentEmbedding(
        bookmark_id=bookmark_id,
        embedding=embedding,
        registrant="system",
        registration_date=datetime.now(),
        update_date=datetime.now()
    )
    db.add(new_embedding)
    db.commit()


# def vector_store(splits) :

#     vectorstore = FAISS.from_documents(documents=splits,
#                                        embedding = GoogleGenerativeAIEmbeddings(model = "models/text-embedding-004"))
#     return vectorstore

def vector_store(splits, db: Session):
    vectorstore = FAISS.from_documents(documents=splits,
                                       embedding=GoogleGenerativeAIEmbeddings(model="models/text-embedding-004"))
    for split in splits:
        bookmark = db.query(Bookmark).filter(Bookmark.url == split.metadata['source']).first()
        if bookmark:
            embedding = vectorstore.get_vector(split)  
            store_embeddings(bookmark.bookmark_id, embedding, db)
    return vectorstore

