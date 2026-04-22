from fastapi import FastAPI
from fastapi.responses import FileResponse
from backend.websocket import router as ws_router

from fastapi import Request
from agent.agent import process_user_input, handle_agent_logic
from services.language import detect_language

app = FastAPI()


# ✅ Serve your frontend (IMPORTANT for Render)
@app.get("/")
def home():
    return FileResponse("test_ws.html")  # rename to index.html if needed


# ✅ Optional API (useful for testing / Streamlit)
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    text = data.get("message", "")

    if not text.strip():
        return {"response": "Please say something"}

    parsed = process_user_input(text)
    result = handle_agent_logic(parsed)
    lang = detect_language(text)

    return {"response": f"[{lang}] {result}"}


# ✅ Health check (Render uses this sometimes)
@app.get("/health")
def health():
    return {"status": "running"}


# ✅ Include WebSocket routes
app.include_router(ws_router)