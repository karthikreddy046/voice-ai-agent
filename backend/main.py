from fastapi import FastAPI
from backend.websocket import router as ws_router

app = FastAPI()

# simple health check
@app.get("/")
def health():
    return {"status": "running"}

# plug websocket routes
app.include_router(ws_router)