from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .database1 import Base

class Department(Base):
   __tablename__ = "departments"
   id = Column(Integer, primary_key=True, index=True)
   name = Column(String, unique=True, index=True)

   products = relationship("Product", back_populates="parent")


class Product(Base):
   __tablename__ = "products"
   id = Column(Integer, primary_key=True, index=True)
   name = Column(String, index=True)
   price = Column(Float, index=True)
   description = Column(String, index=True)

   department_id = Column(Integer, ForeignKey("departments.id"))
   parent = relationship("Department", back_populates="products")


class User(Base):
   __tablename__ = "users"
   name = Column(String, primary_key=True, index=True)
   password = Column(String, index=True)
   mail = Column(String, index=True)

