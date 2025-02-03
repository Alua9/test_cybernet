from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base

class Department(Base):
    __tablename__ = 'departments'


    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    officers = relationship("Officer", back_populates="department")

class Officer(Base):
    __tablename__ = 'officers'


    id = Column(Integer, primary_key=True)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))

    department = relationship("Department", back_populates="officers")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, index=True, nullable=False)
    password = Column(String, nullable=False)

