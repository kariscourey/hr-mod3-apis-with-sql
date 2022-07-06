from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel

from db import TruckQueries
from routers.users import UserOut

router = APIRouter()


class TruckOut(BaseModel):
    id: int
    name: str
    website: str
    category: str
    vegetarian_friendly: bool
    owner: UserOut


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
