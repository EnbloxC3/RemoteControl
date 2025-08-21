from flask import Flask, request, jsonify, render_template
import os
from config import TOKEN, PORT, HOST, DEBUG, ALLOWED_DIRS, ENABLE_TRYLOCK, RATE_LIMIT_FOR_PATHS, BACKLIST_IPS
from utils import system_ops, popup, server
from utils.security import check_rate_limit, check_token_lock, register_failed_token
import gconsole as gcs
import threading
import socket
import time
import sys
import subprocess

app = Flask(__name__, template_folder="templates")

@app.before_request
def global_protection():
    path = request.path
    if request.remote_addr in BACKLIST_IPS:
        try:
            if path == "/":
                return render_template("banned.html"), 403
            else:
                return f"Forbidden", 403
        except Exception:
            return f"Forbidden", 403
        
    if path in RATE_LIMIT_FOR_PATHS:
        if not check_rate_limit():
            return "Too Many Requests", 429

    if ENABLE_TRYLOCK and path != "/":
        response = check_token_lock()
        if response:
            return response

def check_token(req):
    token = req.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return False
    if token == TOKEN:
        return True
    register_failed_token()
    return False


@app.route("/")
def interface():
    try:
        return render_template("interface.html")
    except Exception:
        return f"Welcome to RemoteControl<br>Server is running on target device: {socket.gethostbyname(socket.gethostname())}:{PORT}<br>(templates/interface.html - not found)", 200

@app.route("/check_token")
def check_token_endpoint():
    if check_token(request):
        return "OK", 200
    return "Unauthorized", 401

@app.route("/shutdown")
def shutdown_pc():
    if not check_token(request):
        return "Unauthorized", 401
    system_ops.shutdown()
    return "Shutting down..."

@app.route("/reboot")
def reboot_pc():
    if not check_token(request):
        return "Unauthorized", 401
    system_ops.reboot()
    return "Rebooting..."

@app.route("/get_device_info")
def get_device_info():
    if not check_token(request):
        return "Unauthorized", 401
    return jsonify(system_ops.get_device_info())

@app.route("/get_processes")
def get_processes():
    if not check_token(request):
        return "Unauthorized", 401
    return jsonify(system_ops.get_processes())

@app.route("/run_command")
def run_command():
    if not check_token(request):
        return "Unauthorized", 401
    command = request.args.get("command", "")
    if not command:
        return "No command provided", 400
    return jsonify(system_ops.run_command(command))

@app.route("/popup")
def popup_message():
    if not check_token(request):
        return "Unauthorized", 401
    msg = request.args.get("msg", "No message provided")
    type = request.args.get("type", "info")
    ontop = request.args.get("ontop", "1")
    popup.show_message(msg, type, bool(int(ontop)))
    return f"Displayed: {msg}"

@app.route("/create_file", methods=["POST"])
def create_file():
    if not check_token(request):
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    data = request.get_json()
    path = data.get("path")
    filename = data.get("filename", "newfile.txt")
    content = data.get("content", "")
    if not any(os.path.commonpath([os.path.abspath(path), os.path.abspath(allowed)]) == os.path.abspath(allowed) for allowed in ALLOWED_DIRS):
        return jsonify({"status": "error", "message": "Forbidden path"}), 403
    result = system_ops.create_file(path, filename, content)
    return jsonify({"status": "ok", "path": result})

@app.route("/stop")
def stop_server():
    if not check_token(request):
        return "Unauthorized", 401
    gcs.Console.style_print("Server stopping...", "red")
    threading.Thread(target=stop).start()
    return "Stopped (within 1000ms), check the target device.", 200

@app.route("/restart")
def restart_server():
    if not check_token(request):
        return "Unauthorized", 401
    gcs.Console.style_print("Server restarting...", "yellow")
    threading.Thread(target=restart).start()
    return "Restarted (within 1000ms), check the target device.", 200

def stop():
    time.sleep(1) 
    server.stop()

def restart():
    time.sleep(1)
    python = sys.executable
    script = os.path.abspath(sys.argv[0])
    subprocess.Popen([python, script] + sys.argv[1:])
    os._exit(0)


if __name__ == "__main__":
    gcs.Console.style_print("RemoteControl server is starting directly...", "green")
    try:
        app.run(host=HOST, port=PORT, debug=DEBUG)
    except Exception as e:
        gcs.Console.style_print(f"Server Start Error: {e}", "red")