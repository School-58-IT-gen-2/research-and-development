from fastapi import FastAPI
from pydantic import BaseModel
from main import choose

app = FastAPI()

class Create(BaseModel):
    gender: str
    rac: str
    clas: str

@app.post("/register/")
async def register_user(user: Create):
    return choose(user.gender, user.rac, user.clas)
