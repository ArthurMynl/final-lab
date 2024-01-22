import uuid
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Awards(BaseModel):
    wins: Optional[int]
    nominations: Optional[int]
    text: Optional[str]

class IMDB(BaseModel):
    rating: Optional[float]
    votes: Optional[int]
    id: Optional[int]

class Viewer(BaseModel):
    rating: Optional[float]
    numReviews: Optional[int]
    meter: Optional[int]

class Critic(BaseModel):
    rating: Optional[float]
    numReviews: Optional[int]
    meter: Optional[int]

class Tomatoes(BaseModel):
    viewer: Optional[Viewer]
    fresh: Optional[int]
    critic: Optional[Critic]
    rotten: Optional[int]
    lastUpdated: Optional[datetime] = Field(None, alias="$date")
    
    @validator('lastUpdated', pre=True)
    def parse_last_updated(cls, value):
        if isinstance(value, dict) and '$date' in value:
            return datetime.fromisoformat(value['$date'])
        elif isinstance(value, datetime):
            return value
        return None

class Movie(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    plot: Optional[str]
    genres: Optional[List[str]]
    runtime: Optional[int]
    cast: Optional[List[str]]
    poster: Optional[str]
    title: Optional[str]
    fullplot: Optional[str]
    languages: Optional[List[str]]
    released: Optional[datetime] = Field(None, alias="released")
    directors: Optional[List[str]]
    rated: Optional[str]
    awards: Optional[Awards]
    lastUpdated: Optional[datetime] = None
    year: Optional[int]
    imdb: Optional[IMDB]
    countries: Optional[List[str]]
    type: Optional[str]
    tomatoes: Optional[Tomatoes]
    num_mflix_comments: Optional[int]
    
    @validator('released', pre=True)
    def parse_release_date(cls, value):
        if isinstance(value, dict) and '$date' in value:
            # Assuming the date is stored in ISO format
            return datetime.fromisoformat(value['$date'])
        elif isinstance(value, datetime):
            # If value is already a datetime object, return it directly
            return value
        return None
    
    class Config:
        json_encoders = {
            ObjectId: lambda oid: str(oid),
            datetime: lambda dt: dt.isoformat(),
        }
        allow_population_by_field_name = True


class MovieUpdate(BaseModel):
    plot: Optional[str]
    genres: Optional[List[str]]
    runtime: Optional[int]
    cast: Optional[List[str]]
    poster: Optional[str]
    title: Optional[str]
    fullplot: Optional[str]
    languages: Optional[List[str]]
    released: Optional[datetime] = Field(None, alias="released")
    directors: Optional[List[str]]
    rated: Optional[str]
    awards: Optional[Awards]
    lastUpdated: Optional[datetime] = None
    year: Optional[int]
    imdb: Optional[IMDB]
    countries: Optional[List[str]]
    type: Optional[str]
    tomatoes: Optional[Tomatoes]
    num_mflix_comments: Optional[int]
    
    @validator('released', pre=True)
    def parse_release_date(cls, value):
        if isinstance(value, dict) and '$date' in value:
            return datetime.fromisoformat(value['$date'])
        elif isinstance(value, datetime):
            return value
        return None
    
    class Config:
        json_encoders = {
            ObjectId: lambda oid: str(oid),
            datetime: lambda dt: dt.isoformat(),
        }
        allow_population_by_field_name = True