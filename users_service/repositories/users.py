from sqlalchemy.orm import Session

from users_service.repositories import models, schemas


def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(first_name=user.first_name,
                          last_name=user.last_name,
                          date_of_birth=user.date_of_birth)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

