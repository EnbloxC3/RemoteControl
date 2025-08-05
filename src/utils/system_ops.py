import os
import socket
import platform
import datetime
import psutil
import sys
import subprocess

def shutdown():
    os.system("shutdown /s /t 0")

def reboot():
    os.system("shutdown /r /t 0")

def create_file(path, filename="newfile.txt", content=""):
    full_path = os.path.join(path, filename)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    return full_path

def get_device_info():
    try:
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.datetime.now() - boot_time
        cpu_freq = psutil.cpu_freq()
        memory = psutil.virtual_memory()
        if platform.system() == "Windows":
            disk = psutil.disk_usage('C:\\')
        else:
            disk = psutil.disk_usage('/')
        load_avg = ("N/A", "N/A", "N/A")

        return {
            # System
            "hostname": socket.gethostname(),
            "ip": socket.gethostbyname(socket.gethostname()),
            "user": os.getlogin(),
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "os_name": os.name,
            "uptime": str(uptime),
            "last_boot": boot_time.strftime("%Y-%m-%d %H:%M:%S"),
            "system_load": load_avg,

            # Hard
            "cpu_count": psutil.cpu_count(logical=True),
            "cpu_freq": f"{cpu_freq.current:.2f} MHz" if cpu_freq else "N/A",
            "memory_total": f"{memory.total / (1024**3):.2f} GB",
            "memory_used": f"{memory.used / (1024**3):.2f} GB",
            "memory_free": f"{memory.available / (1024**3):.2f} GB",

            # Disk
            "disk_total": f"{disk.total / (1024**3):.2f} GB",
            "disk_used": f"{disk.used / (1024**3):.2f} GB",
            "disk_free": f"{disk.free / (1024**3):.2f} GB",

            # Python
            "python_version": sys.version.split()[0],
            "python_executable": sys.executable,
            "python_platform": sys.platform,
            "python_implementation": platform.python_implementation(),
            "python_build": platform.python_build(),
            "python_architecture": platform.architecture()[0],
            "python_compiler": platform.python_compiler(),
        }

    except Exception as e:
        return {"error": str(e)}

def get_processes():
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'create_time', 'cpu_percent', 'memory_info']):
            processes.append({
                "pid": proc.info['pid'],
                "name": proc.info['name'],
                "username": proc.info['username'],
                "create_time": datetime.datetime.fromtimestamp(proc.info['create_time']).strftime("%Y-%m-%d %H:%M:%S"),
                "cpu_percent": proc.info['cpu_percent'],
                "memory_info": {
                    "rss": proc.info['memory_info'].rss / (1024**2), 
                    "vms": proc.info['memory_info'].vms / (1024**2)
                }
            })
        return processes
    except Exception as e:
        return {"error": str(e)}

def run_command(command):
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            encoding='utf-8',
            errors='replace'
        )
        
        output, error = process.communicate()
        if error:
            return {"output": error.strip(), "error": True}
        return {"output": output.strip(), "error": False}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("This module is not meant to be run directly.")