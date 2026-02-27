from fastapi import APIRouter
from src.controllers.api.v1 import home_controller
from src.controllers.api.v1 import bike_controller
from src.controllers.api.v1 import car_controller

router = APIRouter()
router.include_router(home_controller.router,prefix="/home",tags=["home"])
router.include_router(bike_controller.router,prefix="/bike",tags=["bike"])
router.include_router(car_controller.router,prefix="/car",tags=["car"])