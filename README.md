# Real-Time Multilingual Voice AI Agent for Clinical Appointment Booking

## Overview

This project implements a real-time voice AI agent designed to handle clinical appointment workflows through natural conversations. The system allows users to book, cancel, or manage appointments using simple voice/text inputs, while maintaining context across interactions.

The focus of this implementation is not just functionality, but building a **low-latency, modular, and fault-tolerant system** that can handle real-world conversational scenarios.

---

## Key Features

- Real-time communication using WebSockets
- Voice-enabled responses using offline Text-to-Speech (TTS)
- Multilingual handling (English, Hindi, Tamil - basic detection)
- Appointment lifecycle management (booking, cancellation)
- Session-based memory for conversational continuity
- Persistent memory support (Redis with fallback)
- Latency tracking for performance evaluation
- Graceful error handling and recovery

---

## System Architecture

The system is structured as a pipeline where each component is responsible for a specific task:
User (Voice/Text)
↓
WebSocket API (FastAPI)
↓
Speech-to-Text (Mock Layer)
↓
Language Detection
↓
Agent Layer (Intent Detection + Parsing)
↓
Memory Layer
├── Session Memory (in-memory)
└── Persistent Memory (Redis / fallback)
↓
Tool Layer (Appointment Logic)
↓
Response Generation
↓
Text-to-Speech (Audio Output)


---

## How It Works

1. The user sends input through a WebSocket connection.
2. Input is passed through a lightweight STT layer (currently mocked).
3. The system detects the language of the input.
4. The agent extracts intent (book, cancel, etc.) and relevant details.
5. Missing information is filled using session or persistent memory.
6. The appropriate tool is executed (e.g., booking an appointment).
7. A response is generated and sent back to the client.
8. The response is converted to speech using TTS.

---

## Memory Design

### Session Memory
- Stored in-memory per WebSocket session
- Maintains ongoing conversation context
- Enables multi-step interactions

### Persistent Memory
- Uses Redis when available
- Falls back to in-memory mode if Redis is not running
- Stores user preferences like doctor selection

This fallback ensures the system continues functioning even when external dependencies are unavailable.

---

## Latency Considerations

The system is optimized for low latency:

| Stage                  | Time (approx) |
|-----------------------|---------------|
| WebSocket receive     | 5–10 ms       |
| Processing (agent)    | 10–30 ms      |
| Response send         | ~5 ms         |
| Total                 | ~20–50 ms     |

This is well within the target requirement of **< 450 ms**.

---

## Design Decisions

- Used rule-based intent parsing for predictable, fast responses
- Avoided heavy LLM usage to maintain low latency
- Implemented Redis fallback to prevent runtime failures
- Used threading for TTS to avoid blocking WebSocket loop
- Kept architecture modular for easier extension

---

## Limitations

- Speech-to-Text is currently mocked
- Language detection is basic and rule-based
- Appointment slots are simulated (no real database)
- TTS may overlap if triggered rapidly
- No authentication layer (user is hardcoded)

---

## Future Improvements

- Integrate real STT (e.g., Whisper or streaming ASR)
- Add LLM-based intent parsing for flexibility
- Connect to real scheduling APIs or databases
- Implement authentication and user identity mapping
- Deploy using Docker and cloud infrastructure
- Improve multilingual support accuracy
- Move TTS to async/background worker

---

## Running the Project

### 1. Start Backend

```bash
uvicorn backend.main:app --reload

```open browser in "http://localhost:5500/test_ws.html"
