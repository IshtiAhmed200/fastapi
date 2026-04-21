from fastapi import APIRouter
from src.controllers.api.v1 import home_controller
from src.controllers.api.v1 import bike_controller
from src.controllers.api.v1 import car_controller
from src.controllers.api.v1 import user_controller
from src.controllers.api.v1 import auth_controller

router = APIRouter()
router.include_router(home_controller.router,prefix="/home",tags=["home"])
router.include_router(bike_controller.router,prefix="/bike",tags=["bike"])
router.include_router(car_controller.router,prefix="/car",tags=["car"])
router.include_router(user_controller.router,prefix="/users",tags=["users"])
router.include_router(auth_controller.router,prefix="/auth",tags=["auth"])