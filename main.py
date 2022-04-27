#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    #Generar los test de ejemplo en la misma validacion con "example."
    city: str = Field(
        ...,
        min_length = 1,
        max_length = 50,
        example="Neza"
    )
    state: str = Field(
        ...,
        min_length = 1,
        max_length = 50,
        example="Mexico"
    )
    country: str = Field(
        ...,
        min_length = 1,
        max_length = 50,
        example="Mexico"
    )

class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length = 1,
        max_length = 50
    )
    lasta_name: str = Field(
        ...,
        min_length = 1,
        max_length = 50
    )
    age: int = Field(
        ...,
        gt = 0,
        lt = 115
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)

    # Generar test automatico de la api.
    class Config:
        schema_extra = {
            "example": {
                "first_name": "Carlos",
                "lasta_name": "Vazquez Lara",
                "age": 33,
                "hair_color": "black",
                "is_married": False
            }
        }

@app.get("/")
def home():
    return {"Hello": "World"}

# Request and Response Body

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

# Validaciones: Query Parameters

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="Person Name.",
        description="This is the person name. It's between 1 and 50 characters",
        example="Jesus"
    ),
    age: str = Query(
        ...,
        title="Person Age.",
        description="This is the person age. It's required",
        example=29
    )
):
    return {name: age}

# Validaciones: Path Parameters

@app.get("/person/detail/{person_id}")
def show_person(
    title="Id Person.",
    description="Showing person with id",
    person_id: int = Path(
        ...,
        gt = 0,
        example=777
    )
):
    return {person_id: "It exists!"}

# Validaciones: Request Body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt= 0,
        example=12
    ),

    person: Person = Body(...),
    location: Location = Body(...)
):
    """results = person.dict()
    results.update(location.dict())"""
    results = dict(person)
    results.update(dict(location))

    return results