from schemas.post import PostCreate
from schemas.user import UserCreate
from config.encode_decode import enc, dec
import datetime as _dt
import database as _database
import sqlalchemy.orm as _orm
import models as _models


def create_database():
    """
    Initialice database instance
    """
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    """
    Call the session maker and create local session
    close in finally point
    """
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_by_email(db: _orm.Session, email: str):
    """
    Verify if the email already in use
    """
    return db.query(_models.User).filter(_models.User.email == email).first()


def create_user(db: _orm.Session, user: UserCreate):
    encode_password = enc(user.password)
    print(encode_password)
    db_user = _models.User(
        email=user.email, hashed_password=encode_password.decode("utf-8"))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_all_users(db: _orm.Session, skip: int, limit: int):
    return db.query(_models.User).offset(skip).limit(limit).all()


def get_user_by_id(db: _orm.Session, id: int):
    return db.query(_models.User).filter(_models.User.id == id).first()


def create_post(db: _orm.Session, post: PostCreate, user_id: int):
    post = _models.Post(**post.dict(), owner_id=user_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def get_all_posts(db: _orm.Session, skip: int, limit: int):
    return db.query(_models.Post).offset(skip).limit(limit).all()


def get_post_by_id(id: int, db: _orm.Session):
    return db.query(_models.Post).filter(_models.Post.id == id).first()


def delete_post(id: int, db: _orm.Session):
    db.query(_models.Post).filter(_models.Post.id == id).delete()
    db.commit()


def update_post(id: int, post: PostCreate, db: _orm.Session):
    db_post = get_post_by_id(db=db, id=id)
    db_post.tittle = post.tittle
    db_post.content = post.content
    db_post.date_last_update = _dt.datetime.utcnow()
    db.commit()
    db.refresh(db_post)
    return db_post