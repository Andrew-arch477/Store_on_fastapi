from typing import Union
from pydantic import BaseModel
from fastapi import Query

class ProductBase(BaseModel):
    name: str
    price: float
    description: str


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    department_id: int
    class Config:
        from_attributes = True


class DepartmentBase(BaseModel):
    name: str


class DepartmentCreate(DepartmentBase):
    pass


class Department(DepartmentBase):
    id: int
    products: list[Product] = []
    class Config:
        from_attributes = True



class UserBase(BaseModel):
    name: str

class UserCreate(UserBase):
    password: str
    mail: str

class User(UserBase):

    class Config:
        from_orm = True









