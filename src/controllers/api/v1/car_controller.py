from fastapi import APIRouter
from typing import Optional

router = APIRouter()

@router.get("/{name}")
def car(name : str):
    return {"Car Name" : name}

@router.get("/{name}/{numPlate}")
def carInfo(name : str, numPlate : str):
    return {
            "Car Name" : name,
            "Num Plate" : numPlate
            }

@router.get("/{name}")
def carInformation(name : str, numPlate : Optional[str] = None):
    return {
            "Car Name" : name,
            "Num Plate" : numPlate
            }