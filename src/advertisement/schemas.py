from pydantic import BaseModel, Field

class AdvertisementBase(BaseModel):
    """
    Base model for advertisements containing common attributes.
    """
    title: str = Field(...)
    author: str = Field(...)
    views_count: int = Field(default=0, ge=0)
    position: int | None = Field(ge=1, default=None)  


class AdvertisementCreate(AdvertisementBase):
    """
    Model for creating new advertisements.
    Inherits from AdvertisementBase, no additional fields required.
    """
    pass


class AdvertisementRead(AdvertisementBase):
    """
    Model for reading advertisement data, including an ID.
    Inherits from AdvertisementBase and adds the ID field.
    """
    id: int


class AdvertisementUpdate(AdvertisementRead):
    """
    Model for updating existing advertisements.
    Inherits from AdvertisementRead, no additional fields required.
    """
    pass
