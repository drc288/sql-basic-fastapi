import datetime as _dt
import sqlalchemy as _sql
import sqlalchemy.orm as _orm

import database as _database

class User(_database.Base):
    __tablename__ = "users"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String(128), unique=True, nullable=False, index=True)
    hashed_password = _sql.Column(_sql.String)
    is_active = _sql.Column(_sql.String, default=True)

    posts = _orm.relationship("Post", back_populates="owner")


class Post(_database.Base):
    __tablename__ = "posts"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    tittle = _sql.Column(_sql.String, index=True)
    content = _sql.Column(_sql.String, index=True)
    owner_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"))
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    date_last_update = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

    owner = _orm.relationship("User", back_populates="posts")
     