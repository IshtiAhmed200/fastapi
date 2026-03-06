from src.config.database import Base
from sqlalchemy import Column,Integer,String

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)
    email = Column(String(100),unique=True,index=True,nullable=False)
    first_name = Column(String(50),nullable=True)
    last_name = Column(String(50),nullable=True)
