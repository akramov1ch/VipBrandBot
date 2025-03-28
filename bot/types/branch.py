from pydantic import BaseModel

class BranchCreate(BaseModel):
    branch_type: str
    name: str
    name_ru: str
    address: str
    phone: str
    longitude: float
    latitude: float
    opening_hours: str
    closing_hours: str
    instagram_have: bool
    instagram_link: str = ""

    class Config:
        from_attributes = True
