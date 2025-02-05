from fastapi import Depends, FastAPI, Security, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from fastapi.security.api_key import APIKeyHeader

from db import crud, models, schemas
from db.database1 import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
security = HTTPBasic()

#uvicorn main:app --reload

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


API_KEY = "api_key"
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key



@app.post("/department/", response_model=schemas.Department)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):

    # db_user = crud.authenticate(db, credentials)
    
    # if not db_user:
    #     raise HTTPException(status_code=401, detail="Invalid credentials")

    return crud.create_department(db=db, department=department)

@app.get("/departments/", response_model=list[schemas.Department])
def read_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):

    departments = crud.get_departments(db, skip=skip, limit=limit)
    return departments


@app.get("/departments/{department_id}", response_model=schemas.Department)
def read_department(department_id: int, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):

    db_department = crud.get_department(db, department_id=department_id)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return db_department


#Сторінка для робота з книгами

@app.post("/departments/{department_id}/products/", response_model=schemas.Product)
def create_product_for_department( department_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    
    return crud.create_product(db=db, product=product, department_id=department_id)


@app.get("/products/", response_model=list[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(security)):

    db_user = crud.authenticate(db, credentials)
    
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    products = crud.get_products(db, skip=skip, limit=limit)
    return products

@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):

    products = crud.delete_product(db, product_id)
    if not products:
        raise {"Product not found"}


@app.post("/users/add", response_model=schemas.User)
def create_user(name: str, password: str, mail: str, db: Session = Depends(get_db)):
    return crud.add_user(db=db, name=name, password=password, mail=mail)

    