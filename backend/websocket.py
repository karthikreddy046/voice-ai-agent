from fastapi import APIRouter, WebSocket
import time
import uuid
import threading

from services.stt import speech_to_text
from services.language import detect_language
from services.tts import speak

from agent.agent import process_user_input, handle_agent_logic
from memory.session_memory import get_session, update_session

# --- SAFE REDIS IMPORT (IMPORTANT FIX) ---
try:
    from memory.persistent_memory import get_user_memory, update_user_memory
except:
    # fallback if Redis is not running
    def get_user_memory(user_id):
        return {}

    def update_user_memory(user_id, data):
        pass


router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    # temporary session + user mapping
    session_id = str(uuid.uuid4())
    user_id = "user_123"  # later replace with real user

    print("new session:", session_id)

    while True:
        try:
            start_time = time.time()

            data = await ws.receive_text()

            # basic guard
            if not data.strip():
                await ws.send_text("didn't catch that, can you repeat?")
                continue

            # ----------- PIPELINE ----------- #

            # STT (mock)
            text = speech_to_text(data)

            # language detection
            lang = detect_language(text)

            # memory fetch
            session = get_session(session_id)
            user_memory = get_user_memory(user_id)

            # intent parsing
            parsed = process_user_input(text)

            # ----------- CONTEXT MERGE ----------- #

            if not parsed.get("doctor"):
                parsed["doctor"] = (
                    session.get("doctor") or user_memory.get("doctor")
                )

            if not parsed.get("date"):
                parsed["date"] = (
                    session.get("date") or user_memory.get("date")
                )

            # ----------- MEMORY UPDATE ----------- #

            update_session(session_id, parsed)
            update_user_memory(user_id, parsed)

            # ----------- TOOL EXECUTION ----------- #

            result = handle_agent_logic(parsed)

            response = f"[{lang}] {result}"

            await ws.send_text(response)

            # ----------- TTS (NON-BLOCKING) ----------- #

            threading.Thread(target=speak, args=(result,)).start()

            # ----------- LATENCY ----------- #

            end_time = time.time()
            print(f"[Latency] {round((end_time - start_time)*1000, 2)} ms")

        except Exception as e:
            print("connection closed:", e)
            break