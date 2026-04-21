from fastapi import APIRouter
from typing import Optional

router = APIRouter()

@router.get("/info")
def car(name : str = ...):
    return {"Car Name" : name}

@router.get("/details/{numPlate}")
def carInfo(numPlate: str):
    return {"Num Plate" : numPlate}

@router.get("/information")
def carInformation(name: str, numPlate: Optional[str] = None):
    return {
            "Car Name" : name,
            "Num Plate" : numPlate
            }