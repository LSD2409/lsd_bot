from sqlalchemy import Column, Integer, ForeignKey, Text, Enum, DateTime, func
from sqlalchemy.orm import relationship

from .enums import ContentType

from chats import models as chat_models
from app.database import Base


class Content(Base):

    __tablename__ = 'content'

    id = Column(Integer, primary_key=True, index=True)
    content_type = Column(Enum(ContentType), nullable=False, default=ContentType.COMPLIMENT.value)
    content = Column(Text, nullable=False)

    content_consumed = relationship('ContentConsume', back_populates='content')


class ContentConsume(Base):

    __tablename__ = 'content_consume'

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(ForeignKey(Content.id), nullable=False)
    chat_id = Column(ForeignKey(chat_models.Chat.id), index=True)
    watched_at = Column(DateTime, server_default=func.now())

    chat = relationship(chat_models.Chat, back_populates='content_consumed')
    content = relationship(Content, back_populates='content_consumed')
