from fastapi import APIRouter
from typing import Optional

router = APIRouter()

@router.get("/info/{name}")
def info(name):
    return {"name" : name}

@router.get("/contact/{contact}")
def contact(contact):
    return {"contact" : contact}

@router.get("/address/{address}")
def address(address):
    return {"address" : address}        

@router.get("/data/{name}/{contact}")
def data(name : str,contact : int):
    return {
            "Name" : name,
            "Contact" : contact
            }

@router.get("/information/{name}")
def Data(name : str, age : Optional[int] = None):
    return {"name" : name,"age" : age}