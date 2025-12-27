# mmgpt_drive_bridge.py
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Create the FastAPI app
app = FastAPI(
    title="MMGPT Drive Bridge",
    description="API bridge between MMGPT and Google Drive",
    version="1.0.0"
)

# Root endpoint - health/status check
@app.get("/", response_class=JSONResponse)
async def root():
    return {"status": "MMGPT Drive Bridge running"}

# Simple test endpoint
@app.get("/ping", response_class=JSONResponse)
async def ping():
    return {"message": "pong"}

# Example placeholder for future Google Drive route
@app.get("/drive/list", response_class=JSONResponse)
async def list_drive_files():
    return {"message": "Google Drive integration coming soon"}
