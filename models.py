from sqlalchemy import Column, ForeignKey, Integer, String
from database import Base

class Department(Base):
    __tablename__ = 'departments'


    id = Column(Integer, primary_key=True, index=True)#primary_key is unique identifier for entire question that we would be saving in database
    name = Column(String, index=True)


class Officer(Base):
    __tablename__ = 'officers'


    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"))
