from typing import Union
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_version():
    return "0.0.0"
