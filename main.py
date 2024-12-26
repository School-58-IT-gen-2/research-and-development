from fastapi import FastAPI
from pydantic import BaseModel
import json
import random
from db_source import DBSource
import uvicorn
from dotenv import load_dotenv
import os


if __name__ == "__main__":
    uvicorn.run(
        app="rnd_fastapi_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
#test1