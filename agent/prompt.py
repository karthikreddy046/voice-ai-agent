def get_prompt(user_input):
    return f"""
You are a clinical assistant helping patients book appointments.

Extract details from the user message.

Return ONLY JSON with:
- intent (book, cancel, reschedule, check)
- doctor (if mentioned)
- date (if mentioned)
- time (if mentioned)

User: "{user_input}"
"""