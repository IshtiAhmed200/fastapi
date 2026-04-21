from src.config.database import Base
from sqlalchemy import Column,Integer,String
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)
    email = Column(String(100),unique=True,index=True,nullable=False)
    first_name = Column(String(50),nullable=True)
    last_name = Column(String(50),nullable=True)
    password = Column(String(255), nullable=False)

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password)
    
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)
