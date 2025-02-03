from fastapi import FastAPI
from api.departments import router as departments_router
from api.officers import router as officers_router
from api.auth import router as auth_router


app = FastAPI()
# Base.metadata.create_all(bind=engine)

app.include_router(departments_router)
app.include_router(officers_router)
app.include_router(auth_router)










