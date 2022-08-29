from . import models, schemas
from sqlalchemy.orm import Session


def get_chat(db: Session, chat_id: int) -> models.Chat:
    return db.query(models.Chat).filter(models.Chat.chat_id == chat_id).first()


def create_chat(db: Session, chat: schemas.ChatCreate) -> models.Chat:
    chat = models.Chat(**chat.dict())
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


def create_chat_message(db: Session, message: schemas.ChatMessageCreate) -> models.ChatMessage:

    chat = get_chat(db, message.chat_id)
    if chat is None is None:
        create_chat(db, schemas.ChatCreate(chat_id=message.chat_id))

    chat_message = models.ChatMessage(chat_id=chat.id, text=message.text)

    db.add(chat_message)
    db.commit()
    db.refresh(chat_message)
    return chat_message


def get_messages_by_chat_id(db: Session, chat_id: int) -> list[models.ChatMessage]:
    return db.query(models.ChatMessage)\
        .filter(models.ChatMessage.chat_id == chat_id)\
        .order_by(models.ChatMessage.id).all()
