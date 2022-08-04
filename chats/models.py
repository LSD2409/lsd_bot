from app.database import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship


class Chat(Base):

    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, index=True)
    last_message_at = Column(DateTime, server_default=func.now())

    messages = relationship('Message', back_populates='chat')
    consumed_content = relationship('ContentConsume', back_populates='chat')


class ChatMessage(Base):

    __tablename__ = 'chat_messages'

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(ForeignKey('chats.id'), index=True)
    text = Column(Text, nullable=False, default='')
    received_at = Column(DateTime, server_default=func.now())

    chat = relationship('Chat', back_populates='messages')
