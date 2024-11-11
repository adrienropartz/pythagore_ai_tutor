from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Set up logging properly for production
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Pythagore Math Tutor",
    description="AI-powered math tutoring API",
    version="1.0.0"
)

# Add CORS middleware with environment variables
allowed_origins = os.getenv('ALLOWED_ORIGINS', '*').split(',')
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize tutor lazily to save memory
tutor = None

class TutorRequest(BaseModel):
    message: str
    config: dict

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

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