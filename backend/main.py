from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from db import engine

app = FastAPI(title="2anki New API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "https://2anki.net", "https://zoe.2anki.net"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def check_database_connection():
    """Check database connection on startup"""
    try:
        with engine.connect() as connection:
            # Execute a simple query to verify connection
            result = connection.execute(text("SELECT 1")).fetchone()
            if result[0] != 1:
                raise HTTPException(status_code=500, detail="Database connection failed")
    except OperationalError as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

DEFAULT_USER_INSTRUCTIONS = """Some extra rules and explanations:
- Read the document from start to finish and identify any question and answers. 
- Use the same language as the document or infer the language based on what is mostly used.
- Use the same text as in the document and do not make up any questions or answers.
- Cite the document as source for the text.
- Be complete by finding all of the questions and answer in the document.
- Do not limit the number of number of questions and answer but create all of them!
- Do not make up any questions and use the questions in the document!
- Create a ul for every question pair, not one ul for all of them with li!"""

@app.get("/status", tags=["health"])
async def status():
    """
    Health check endpoint that returns a playful response.
    
    Returns:
        dict: A dictionary containing the status message
    """
    return "Ping me maybe? 🎶"

@app.get("/napi/pdf-conversion/instructions", tags=["pdf-conversion"])
async def get_default_instructions():
    """
    Get the default user instructions for PDF conversion.
    
    Returns:
        dict: A dictionary containing the default instructions
    """
    return {"instructions": DEFAULT_USER_INSTRUCTIONS}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=31415)
