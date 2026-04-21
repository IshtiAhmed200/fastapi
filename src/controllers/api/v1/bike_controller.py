from fastapi import APIRouter
from typing import Optional

router = APIRouter()


@router.get("/info")
def bike(name : str = ...):
    return {"Bike Name" : name}

@router.get("/details/{numPlate}")
def bikeInfo(numPlate: str):
    return {"Num Plate" : numPlate}

@router.get("/information")
def bikeInformation(name: str, numPlate: Optional[str] = None):
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