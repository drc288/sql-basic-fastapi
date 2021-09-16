import datetime as _dt
import pydantic as _pydantic

class _PostBase(_pydantic.BaseModel):
    tittle: str
    content: str

class PostCreate(_PostBase):
    pass

class Post(_PostBase):
    id: int
    owner_id: int
    date_created: _dt.datetime
    date_last_update: _dt.datetime

    class Config:
        orm_mode = True
