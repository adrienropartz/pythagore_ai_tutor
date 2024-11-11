from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from .main import PythagoreTutor

# Set up logging properly
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Development
        "http://127.0.0.1:3000",  # Alternative local URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the tutor
tutor = PythagoreTutor()

class TutorRequest(BaseModel):
    message: str
    config: dict

@app.get("/")
async def root():
    return {"message": "Welcome to Pythagore Math Tutor API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/tutor")
async def chat_with_tutor(request: TutorRequest):
    try:
        # Process the message using your tutor logic
        response = tutor.chat(request.message, request.config)
        return {"response": response}
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        # Properly raise an HTTPException instead of returning a tuple
        raise HTTPException(status_code=500, detail=str(e))

# test