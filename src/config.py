TOKEN = "TOKEN" # Your token here
PORT = 4390
HOST = "0.0.0.0"
DEBUG = False

ALLOWED_DIRS = [
    "C:/Users/",
]

RATE_LIMIT = {
    "MAX_REQ_PER_SECOND": 3
}
RATE_LIMIT_FOR_PATHS = [
    "/",
    "/check_token"
]
ENABLE_TRYLOCK = True
TOKEN_SECURITY = {
    "MAX_ATTEMPTS": 5,
    "BAN_DELAYS": [30, 60, 180, 300],  # second
    "PERMANENT_AFTER": 4  # 5th try > ban
}

BACKLIST_IPS = [
    "192.168.1.31",
] # Your blacklisted local IPv4 addresses

if __name__ == "__main__":
    print("This module is not meant to be run directly.")
