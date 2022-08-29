from . import models, schemas
from sqlalchemy.orm import Session

from chats import crud as chat_crud


def create_content(db: Session, content: schemas.ContentCreate) -> models.Content:
    content = models.Content(**content.dict())
    db.add(content)
    db.commit()
    db.refresh(content)
    return content


def create_content_consume(db: Session, content_consume: schemas.ContentConsumeCreate) -> models.ContentConsume:
    content_consume = models.ContentConsume(**content_consume.dict())
    db.add(content_consume)
    db.commit()
    db.refresh(content_consume)
    return content_consume


def get_not_consumed_content(db: Session, not_consumed_content: schemas.NotConsumedContent) -> models.Content:
    chat = chat_crud.get_chat(db, not_consumed_content.chat_id)
    consumed_content_id = [
        q.content_id for q in
        db.query(models.ContentConsume).filter(
            models.ContentConsume.chat_id == chat.id)
    ]

    content = db.query(models.Content)\
        .filter(
        models.Content.id.notin_(consumed_content_id),
        models.Content.content_type == not_consumed_content.content_type
    ).\
        order_by(models.Content.id).first()

    create_content_consume(
        db, schemas.ContentConsumeCreate(
            chat_id=chat.id,
            content_id=content.id
        )
    )

    return content
