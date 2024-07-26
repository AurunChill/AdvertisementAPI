from pydantic import BaseModel, Field

class AdvertisementBase(BaseModel):
    title: str = Field(...)
    author: str = Field(...)
    views_count: int = Field(default=0, ge=0)
    position: int | None = Field(ge=1, default=None)

    class Config:
        orm_mode = True



class AdvertisementCreate(AdvertisementBase):
    pass


class AdvertisementRead(AdvertisementBase):
    id: int


class AdvertisementUpdate(AdvertisementRead):
    pass
