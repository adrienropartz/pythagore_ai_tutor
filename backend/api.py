from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging properly
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware with environment variables
allowed_origins = os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000').split(',')
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize tutor lazily
tutor = None

class TutorRequest(BaseModel):
    message: str
    config: dict

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/tutor")
async def chat_with_tutor(request: TutorRequest):
    global tutor
    try:
        if tutor is None:
            from .main import PythagoreTutor
            tutor = PythagoreTutor()
        response = tutor.chat(request.message, request.config)
        return {"response": response}
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# test