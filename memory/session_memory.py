# simple in-memory store for now
# later we can switch to Redis

session_store = {}

def get_session(session_id):
    return session_store.get(session_id, {})

def update_session(session_id, data):
    if session_id not in session_store:
        session_store[session_id] = {}

    session_store[session_id].update(data)


def clear_session(session_id):
    if session_id in session_store:
        del session_store[session_id]