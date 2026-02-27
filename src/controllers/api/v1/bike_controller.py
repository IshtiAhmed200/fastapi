from fastapi import APIRouter
from typing import Optional

router = APIRouter()


@router.get("/{name}")
def bike(name : str):
    return {"Bike Name" : name}

@router.get("/{name}/{numPlate}")
def bikeInfo(name : str, numPlate : str):
    return {
            "Bike Name" : name,
            "Num Plate" : numPlate
            }

@router.get("/{name}")
def bikeInformation(name : str, numPlate : Optional[str] = None):
    return {
            "Bike Name" : name,
            "Num Plate" : numPlate
            }