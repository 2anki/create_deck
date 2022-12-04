from fastapi import FastAPI

from __version__ import version

description = """
The create_deck API helps you create Anki flashcards fast. 🌟
"""

tos = "https://alemayhu.notion.site/Terms-of-services-931865161517453b99fb6495e400061d"

app = FastAPI(
    title="create_deck API",
    description=description,
    version=version,
    terms_of_service=tos,
    contact={
        "name": "Alexander Alemayhu",
        "url": "https://alemayhu.com",
        "email": "alexander@alemayhu.com"
    },
    license_info={
        "name": "MIT LICENSE",
        "url": "https://github.com/2anki/create_deck/blob/main/LICENSE"
    }
)


@app.get("/")
def read_version():
    return version.encode("utf-8")
