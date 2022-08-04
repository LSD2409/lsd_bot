from . import models, schemas
from sqlalchemy.orm import Session


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
    consumed_content_id = db.query(models.ContentConsume)\
        .filter(
        models.ContentConsume.chat_id == not_consumed_content.chat.chat_id,
        models.ContentConsume.content_type == not_consumed_content.content_type
    )\
        .values(models.ContentConsume.content_id)

    content = db.query(models.Content)\
        .filter(
        models.Content.id.notin_(consumed_content_id),
        models.Content.content_type == not_consumed_content.content_type
    ).\
        order_by(models.Content.id).first()

    return content
