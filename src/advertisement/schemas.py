from pydantic import BaseModel, Field

class AdvertisementBase(BaseModel):
    title: str = Field(...)
    author: str = Field(...)
    views_count: int = Field(default=0, ge=0)
    position: int = Field(None, ge=1)

    class Config:
        orm_mode = True



class AdvertisementCreate(AdvertisementBase):
    pass


class AdvertisementRead(AdvertisementBase):
    id: int


class AdvertisementUpdate(AdvertisementBase):
    pass
