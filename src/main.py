from typing import List
from schemas.user import User, UserCreate
from schemas.post import Post, PostCreate

import fastapi as _fastapi
import sqlalchemy.orm as _orm
import services as _services


app = _fastapi.FastAPI()

_services.create_database()


@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    """
    Create a user

    db: _orm.Session verifica primero si get_db esta inicializado primero
    """
    db_user = _services.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise _fastapi.HTTPException(
            status_code=400, detail="Woops the email is in use")
    return _services.create_user(db=db, user=user)


@app.get("/users/", response_model=List[User])
def get_all_user(skip: int = 0, limit: int = 10, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return _services.get_all_users(db=db, skip=skip, limit=limit)


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_user = _services.get_user_by_id(db=db, id=user_id)
    if db_user is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="This user does not exist"
        )
    return db_user


@app.post("/users/{user_id}/posts/", response_model=Post)
def create_post(user_id: int, post: PostCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_user = _services.get_user_by_id(db=db, id=user_id)
    if db_user is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="This user does not exist"
        )
    return _services.create_post(db=db, post=post, user_id=user_id)


@app.get("/posts/", response_model=List[Post])
def get_post(skip: int = 0, limit: int = 10, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return _services.get_all_posts(db=db, skip=skip, limit=limit)


@app.get("/posts/{post_id}", response_model=Post)
def get_post_by_id(post_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    post = _services.get_post_by_id(id=post_id, db=db)
    if post is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="This post does not exist"
        )
    return post


@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    _services.delete_post(id=post_id, db=db)
    return {"message": f"successfully delete post with id: {post_id}"}


@app.put("/posts/{post_id}")
def update_post(post_id: int, post: PostCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    post = _services.get_post_by_id(id=post_id, db=db)
    if post is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="This post does not exist"
        )
    return _services.update_post(id=post_id, post=post, db=db)
