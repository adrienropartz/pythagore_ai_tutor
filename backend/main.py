from fastapi import FastAPI, HTTPException
from .tutor import PythagoreTutor, TutorConfig  # Import from your existing code
from .api import app  # Import the FastAPI app from api.py

# Initialize the tutor
tutor = None

@app.on_event("startup")
async def startup_event():
    global tutor
    try:
        tutor = PythagoreTutor()
    except Exception as e:
        print(f"Error initializing tutor: {e}")

@app.post("/chat")
async def chat(message: str, config: dict = None):
    if tutor is None:
        raise HTTPException(status_code=500, detail="Tutor not initialized")
    
    if config is None:
        config = TutorConfig.default().__dict__
    
    try:
        response = await tutor.chat(message, config)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
