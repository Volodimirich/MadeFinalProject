from typing import Optional
from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

from src.base_models import PydanticObjectId


class User(BaseModel):
    id: Optional[PydanticObjectId] = Field(
        default_factory=PydanticObjectId, alias="_id"
    )
    username: str
    password: str

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
