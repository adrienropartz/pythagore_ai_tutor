from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from main import PythagoreTutor, TutorConfig
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI(title="Pythagore Math Tutor API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the tutor instance
try:
    tutor = PythagoreTutor()
    logger.info("PythagoreTutor initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize PythagoreTutor: {str(e)}")
    raise

class TutorConfigRequest(BaseModel):
    depth: str
    learning_style: str = "Active"
    communication_style: str = "Socratic"
    tone_style: str = "Encouraging"
    reasoning_framework: str = "Causal"
    use_emojis: bool = True
    language: str = "English"

class TutorRequest(BaseModel):
    message: str
    config: TutorConfigRequest
    chat_history: Optional[str] = ""

@app.get("/")
async def read_root():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Pythagore Math Tutor API is running"}

@app.post("/api/tutor")
async def process_message(request: TutorRequest):
    """
    Process a message from the student and return the tutor's response.
    
    Args:
        request (TutorRequest): Contains the message, configuration, and chat history
        
    Returns:
        JSONResponse: The tutor's response
        
    Raises:
        HTTPException: If there's an error processing the message
    """
    try:
        logger.info(f"Processing message with depth: {request.config.depth}")
        
        # Create TutorConfig instance from request
        config = TutorConfig(
            depth=request.config.depth,
            learning_style=request.config.learning_style,
            communication_style=request.config.communication_style,
            tone_style=request.config.tone_style,
            reasoning_framework=request.config.reasoning_framework,
            use_emojis=request.config.use_emojis,
            language=request.config.language
        )
        
        # Process the message using the tutor
        response = await tutor.process_message(
            message=request.message,
            config=config,
            chat_history=request.chat_history
        )
        
        return JSONResponse(
            content={"response": response},
            status_code=200
        )
        
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing message: {str(e)}"
        )

@app.get("/api/health")
async def health_check():
    """
    Check if all components are working properly.
    """
    try:
        # Verify environment variables
        if not os.getenv("ANTHROPIC_API_KEY"):
            raise ValueError("ANTHROPIC_API_KEY not found")
            
        return {
            "status": "healthy",
            "components": {
                "api": "ok",
                "tutor": "ok",
                "environment": "ok"
            }
        }
    except Exception as e:
        return JSONResponse(
            content={
                "status": "unhealthy",
                "error": str(e)
            },
            status_code=500
        )

if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment variable or default to 8000
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=port,
        reload=True  # Set to False in production
    )