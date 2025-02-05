from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import Depends, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from bcrypt import hashpw, gensalt, checkpw

security = HTTPBasic()

def get_department(db: Session, department_id: int):
    return db.query(models.Department).filter(models.Department.id == department_id).first()


def get_departments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Department).offset(skip).limit(limit).all()

def create_department(db: Session, department: schemas.DepartmentCreate):
    db_department = models.Department(name = department.name)
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate, department_id: int):
    db_product = models.Product(**product.dict(), department_id=department_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    db.delete(db_product)
    db.commit()
    return True

def authenticate(db: Session, credentials: HTTPBasicCredentials):
    db_user = db.query(models.User).filter(models.User.login == credentials.username).first()
    
    if not db_user or not checkpw(credentials.password.encode("utf-8"), db_user.password.encode("utf-8")):
        return None
    
    return db_user

def add_user(db: Session, name: str, password: str, mail: str):
    hashed_password = hashpw(password.encode(), gensalt())
    new_user = models.User(name=name, password=hashed_password.decode("utf-8"), mail=mail)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user










