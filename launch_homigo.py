import subprocess
import time

print("🚀 Booting up the Homigo Ecosystem...")

# These specific flags (--server.address 0.0.0.0 and CORS false) 
# force GitHub Codespaces to let the connection through.
cmd_template = "python -m streamlit run {file} --server.port {port} --server.address 0.0.0.0 --server.enableCORS false --server.enableXsrfProtection false"

apps = [
    {"file": "main.py", "port": 8504, "name": "Customer Hub"},
    {"file": "service_dashboard.py", "port": 8505, "name": "Expert Dashboard"},
    {"file": "cktmonitoring.py", "port": 8506, "name": "Pulse IoT"}
]

processes = []

for app in apps:
    print(f"Starting {app['name']} on Port {app['port']}...")
    cmd = cmd_template.format(file=app["file"], port=app["port"])
    # Launch in the background
    p = subprocess.Popen(cmd, shell=True)
    processes.append(p)
    # Stagger startups by 2 seconds so the Codespace doesn't run out of memory
    time.sleep(2) 

print("✅ All systems go! Open your PORTS tab now.")

try:
    # Keep the script running
    for p in processes:
        p.wait()
except KeyboardInterrupt:
    print("\n🛑 Shutting down the Homigo Ecosystem...")
    for p in processes:
        p.kill()
