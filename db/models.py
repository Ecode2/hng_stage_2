import uuid
from db.db import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Boolean

class User(Base):
    __tablename__ = "users"

    userId = Column(String, primary_key=True, default=str(uuid.uuid4()), index=True, unique=True)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    organosation = relationship('DbArticle', back_populates='user')
    
class Organisation(Base):
  __tablename__= 'organisations'
  
  orgId = Column(String, primary_key=True, default=str(uuid.uuid4()), index=True, unique=True)
  name = Column(String, nullable=False)
  description = Column(String, nullable=False)

  user_id = Column(Integer, ForeignKey('users.userId'))
  user = relationship("DbUser", back_populates='items')