from pydantic import BaseModel


class UserCreate(BaseModel):
    tg_id: int
    full_name: str
    language: str
