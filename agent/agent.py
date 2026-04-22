from agent.tools import check_availability, book_appointment, cancel_appointment


def process_user_input(text):
    # simple rule-based parsing (fast + predictable for now)

    text_lower = text.lower()

    # intent detection
    if "book" in text_lower:
        intent = "book"
    elif "cancel" in text_lower:
        intent = "cancel"
    elif "reschedule" in text_lower:
        intent = "reschedule"
    else:
        intent = "unknown"

    # doctor detection (very basic)
    doctor = None
    if "cardio" in text_lower:
        doctor = "cardiologist"
    elif "derma" in text_lower:
        doctor = "dermatologist"

    # date detection
    date = "tomorrow" if "tomorrow" in text_lower else "today"

    return {
        "intent": intent,
        "doctor": doctor,
        "date": date
    }


def handle_agent_logic(data):
    intent = data["intent"]

    if intent == "book":
        slots = check_availability(data["doctor"], data["date"])

        # picking first slot for now (can improve later)
        return book_appointment(data["doctor"], data["date"], slots[0])

    elif intent == "cancel":
        return cancel_appointment()

    elif intent == "reschedule":
        return "Rescheduling not fully implemented yet"

    return "Sorry, I didn’t understand that"