from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .enums import ContentType

from chats import models as chat_models
from app.database import Base


class Content(Base):

    __tablename__ = 'content'

    id = Column(Integer, primary_key=True, index=True)
    content_type = Column(String, nullable=False)

    content_consume = relationship('ContentConsume', back_populates='content')


class ContentConsume(Base):

    __table__ = 'content_consume'

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, nullable=False)
    chat_id = Column(ForeignKey(chat_models.Chat.id), index=True)

    chat = relationship(chat_models.Chat, back_populates='content_consume')
    content = relationship(Content, back_populates='content_consume')


class Compliment(Content):

    __tablename__ = 'compliments'

    content_type = ContentType.COMPLIMENT.value

    id = Column(Integer, ForeignKey("content.id"), primary_key=True)
    text = Column(String, nullable=False)
