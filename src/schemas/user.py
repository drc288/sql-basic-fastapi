from typing import List
import pydantic as _pydantic
from schemas.post import Post


class _UserBase(_pydantic.BaseModel):
    email: str

class UserCreate(_UserBase):
    password: str

class User(_UserBase):
    id: int
    is_active: bool
    posts: List[Post] = []

    class Config:
        orm_mode = True
