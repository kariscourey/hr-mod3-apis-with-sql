from typing import Literal
from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel

from db import TruckQueries
from routers.users import UserOut

router = APIRouter()


class TruckIn(BaseModel):
    name: str
    website: str
    category: Literal[
        "American",
        "Asian",
        "French",
        "Mediterranean",
        "Indian",
        "Italian",
        "Latin",
    ]
    vegetarian_friendly: bool
    owner_id: int


class TruckOut(BaseModel):
    id: int
    name: str
    website: str
    category: Literal[
        "American",
        "Asian",
        "French",
        "Mediterranean",
        "Indian",
        "Italian",
        "Latin",
    ]
    vegetarian_friendly: bool
    owner: UserOut

class TruckWithPriceOut(TruckOut):
    average_price: float | None

class TrucksOut(BaseModel):
    trucks: list[TruckWithPriceOut]


@router.get("/api/trucks/{truck_id}", response_model=TruckOut)
def get_truck(
    truck_id: int,
    response: Response,
    queries: TruckQueries = Depends(),
):
    record = queries.get_truck(truck_id)
    if record is None:
        response.status_code = 404
    else:
        return record


@router.get("/api/trucks", response_model=TrucksOut)
def get_trucks(queries: TruckQueries = Depends()):
    return {"trucks": queries.get_trucks()}


@router.post("/api/trucks", response_model=TruckOut)
def create_truck(
    truck: TruckIn,
    queries: TruckQueries = Depends(),
):
    return queries.create_truck(truck)

@router.delete("/api/trucks/{truck_id}", response_model=bool)
def delete_truck(truck_id: int, queries: TruckQueries = Depends()):
    queries.delete_truck(truck_id)
    return True