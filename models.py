from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field
from pydantic.json import ENCODERS_BY_TYPE
from fastapi.encoders import jsonable_encoder
from bson import ObjectId


class PydanticObjectId(ObjectId):
    """
    Object Id field. Compatible with Pydantic.
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return PydanticObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema: dict):
        field_schema.update(
            type="string",
            examples=["5eb7cf5a86d9755df3a6c593", "5eb7cfb05e32e07750a1756a"],
        )


ENCODERS_BY_TYPE[PydanticObjectId] = str


class Author(BaseModel):
    id: Optional[PydanticObjectId] = Field(
        default_factory=PydanticObjectId, alias="_id"
    )
    name: str = ""
    org: Optional[str] = None
    gid: Optional[str] = None


class Venue(BaseModel):
    raw: Optional[str] = None
    raw_zh: Optional[str] = None
    publisher: Optional[str] = None
    type: Optional[int] = None


class Paper(BaseModel):
    id: Optional[PydanticObjectId] = Field(
        default_factory=PydanticObjectId, alias="_id"
    )
    title: str
    authors: Optional[List[Author]]
    venue: Optional[Venue]
    year: int
    keywords: Optional[List[str]]
    fos: Optional[List[str]]
    n_citation: Optional[int]
    page_start: Optional[str]
    page_end: Optional[str]
    lang: Optional[str]
    volume: Optional[str]
    issue: Optional[str]
    issn: Optional[str]
    isbn: Optional[str]
    doi: Optional[str]
    pdf: Optional[str]
    url: Optional[List[str]]
    abstract: Optional[str]

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        if data.get("_id") is None:
            data.pop("_id", None)
        return data

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "53e99784b7602d9701f3e4f4",
                "title": "2BTextures",
                "authors": [
                    {"_id": "53f45ad4dabfaee1c0b3e206", "name": "Bonnie Mitchell"}
                ],
                "venue": {
                    "_id": "5736ae3ad39c4f40a7976060",
                    "type": 10,
                    "raw": "SIGGRAPH Computer Animation Fesitval",
                },
                "year": 2009,
                "keywords": [
                    "visual source material",
                    "minute sound",
                    "integrated journey temporally",
                    "abstract environment",
                    "intricate detail",
                    "particulated image",
                    "artists delve",
                    "visual experience",
                    "multi-faceted granular complexity",
                    "stylized natural element",
                ],
                "fos": [
                    "Agronomy",
                    "Moisture",
                    "Hydrology",
                    "Environmental science",
                    "Dry weight",
                    "Water content",
                    "Stomatal conductance",
                    "Transpiration",
                    "Irrigation",
                    "Soil water",
                    "Canopy",
                ],
                "n_citation": 0,
                "page_start": "8",
                "page_end": "8",
                "lang": "en",
                "volume": "",
                "issue": "",
                "issn": "",
                "isbn": "",
                "doi": "10.1145/1596685.1596687",
                "pdf": "",
                "url": [
                    "http://dx.doi.org/10.1145/1596685.1596687",
                    "http://doi.acm.org/10.1145/1596685.1596687",
                    "db/conf/siggraph/siggraph2009festival.html#Mitchell09",
                    "https://doi.org/10.1145/1596685.1596687",
                ],
                "abstract": '"2BTextures", a two-movement audio/visual experience, leads viewers through abstract environments influenced by nature and life. This integrated journey temporally explores the multi-faceted granular complexity inherent in its sonic and visual source material. By fragmenting and simulating stylized natural elements, the artists delve into the intricate detail found in minute sounds and particulated images. As each movement unfolds, viewers traverse a macro-landscape or shift their focus to micro-elements.',
            }
        }


class UpdatePaper(BaseModel):
    title: str
    authors: Optional[List[Dict[str, Any]]]
    venue: Dict[str, Any]
    year: int
    keywords: List[str]
    n_citation: Optional[int]
    page_start: Optional[str]
    page_end: Optional[str]
    lang: Optional[str]
    volume: Optional[str]
    issue: Optional[str]
    issn: Optional[str]
    isbn: Optional[str]
    doi: Optional[str]
    pdf: Optional[str]
    url: Optional[List[str]]
    abstract: Optional[str]

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        if data.get("_id") is None:
            data.pop("_id", None)
        return data

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "3GIO.",
                "venue": {"type": 0},
                "year": 2011,
                "keywords": [],
                "n_citation": 0,
                "lang": "en",
            }
        }
