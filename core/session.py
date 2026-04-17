sessions = {}

def create_session(user):
    sessions[user] = {"requests": 0}
    return sessions[user]