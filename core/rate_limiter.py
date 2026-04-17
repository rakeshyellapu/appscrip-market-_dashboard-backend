import time

requests_log = {}
LIMIT = 5
WINDOW = 60  # seconds

def check_rate_limit(user: str):
    now = time.time()

    if user not in requests_log:
        requests_log[user] = []

    # remove old requests
    requests_log[user] = [t for t in requests_log[user] if now - t < WINDOW]

    if len(requests_log[user]) >= LIMIT:
        raise Exception("Rate limit exceeded")

    requests_log[user].append(now)