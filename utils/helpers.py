import time


def generate_random_email() -> str:
    timestamp = int(time.time() * 1000)
    return f"test{timestamp}@example.com"
