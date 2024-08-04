# models.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String)
    type = Column(String)
    status = Column(String)
    admin_memo = Column(String, nullable=True)
    updater = Column(String)
    update_date = Column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    update_reason = Column(String, nullable=True)
    registrant = Column(String)
    registration_date = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    bookmarks = relationship("Bookmark", back_populates="user")
    chats = relationship("Chat", back_populates="user")

class Bookmark(Base):
    __tablename__ = 'bookmark'
    bookmark_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    bookmark_name = Column(String)
    url = Column(String)
    summary = Column(String, nullable=True)
    updater = Column(String, nullable=True)
    update_date = Column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    update_reason = Column(String, nullable=True)
    registrant = Column(String)
    registration_date = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    user = relationship("User", back_populates="bookmarks")
    content_embeddings = relationship("ContentEmbedding", back_populates="bookmark")

class ContentEmbedding(Base):
    __tablename__ = 'content_embedding'
    content_id = Column(Integer, primary_key=True, index=True)
    bookmark_id = Column(Integer, ForeignKey('bookmark.bookmark_id'))
    embedding = Column(String)  # 임베딩을 저장할 데이터 타입을 결정하세요.
    updater = Column(String, nullable=True)
    update_date = Column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    update_reason = Column(String, nullable=True)
    registrant = Column(String)
    registration_date = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    bookmark = relationship("Bookmark", back_populates="content_embeddings")

class Chat(Base):
    __tablename__ = 'chat'
    chat_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    start_time = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    end_time = Column(DateTime, nullable=True)
    updater = Column(String, nullable=True)
    update_date = Column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    update_reason = Column(String, nullable=True)
    registrant = Column(String)
    registration_date = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    user = relationship("User", back_populates="chats")
    chat_logs = relationship("ChatLog", back_populates="chat")

class ChatLog(Base):
    __tablename__ = 'chat_log'
    chat_id = Column(Integer, ForeignKey('chat.chat_id'), primary_key=True)
    input = Column(String)
    output = Column(String)
    updater = Column(String, nullable=True)
    update_date = Column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    update_reason = Column(String, nullable=True)
    registrant = Column(String)
    registration_date = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    chat = relationship("Chat", back_populates="chat_logs")
