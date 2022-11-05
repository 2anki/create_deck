from typing import Union
from fastapi import FastAPI

from version import version

app = FastAPI()


@app.get("/")
def read_version():
    return version
