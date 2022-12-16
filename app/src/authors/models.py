from typing import Optional
from pydantic import BaseModel, Field

from src.base_models import PydanticObjectId


class Author(BaseModel):
    id: Optional[PydanticObjectId] = Field(
        default_factory=PydanticObjectId, alias="_id"
    )
    name: str = ""
    org: Optional[str] = None
    gid: Optional[str] = None
