import time
from flask import request, make_response
from config import RATE_LIMIT, TOKEN_SECURITY

rate_log = {}
token_attempts = {}
banned_ips = {}

def get_ip():
    return request.remote_addr

def check_rate_limit():
    ip = get_ip()
    now = time.time()

    log = rate_log.setdefault(ip, [])
    log[:] = [t for t in log if now - t < 1] 
    log.append(now)

    if len(log) > RATE_LIMIT["MAX_REQ_PER_SECOND"]:
        return False
    return True

def check_token_lock():
    ip = get_ip()
    now = time.time()

    ban_info = banned_ips.get(ip)
    if ban_info == "PERMANENT":
        return "Banned", 403
    elif isinstance(ban_info, float) and now < ban_info:
        reponse = make_response("Temp Banned", 423)
        reponse.headers["Retry-After"] = int(ban_info - now) 
        return reponse

    return None

def register_failed_token():
    ip = get_ip()
    now = time.time()
    entry = token_attempts.setdefault(ip, {"failures": 0, "ban_level": 0})

    entry["failures"] += 1

    if entry["failures"] >= TOKEN_SECURITY["MAX_ATTEMPTS"]:
        ban_level = entry["ban_level"]
        if ban_level < len(TOKEN_SECURITY["BAN_DELAYS"]):
            delay = TOKEN_SECURITY["BAN_DELAYS"][ban_level]
            banned_ips[ip] = now + delay
            entry["failures"] = 0
            entry["ban_level"] += 1
        else:
            banned_ips[ip] = "PERMANENT"

if __name__ == "__main__":
    print("This module is not meant to be run directly.")