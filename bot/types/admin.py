from pydantic import BaseModel


class AdminCreate(BaseModel):
    tg_id: int
    full_name: str
