import socket
import json
import urllib.request
import shutil
import os
import time

# Configuration
PROJECT_ID = "example_project"  # Change for each project
PORT = 50555

# Setup UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("", PORT))
sock.setblocking(False)  # Non-blocking socket

print(f"[OTA] Project '{PROJECT_ID}' listening for messages on port {PORT}")


def handle_packet(packet):
    if packet["type"] == "MESSAGE":
        print("[OTA MESSAGE]:", packet["content"])

    elif packet["type"] == "UPDATE":
        github_url = packet["url"]
        target_file = packet["file"]
        apply_update(github_url, target_file)


def apply_update(url, target_file):
    print(f"[OTA] Updating {target_file} from GitHub: {url}")

    tmp_file = target_file + ".new"
    backup_file = target_file + ".bak_" + str(int(time.time()))

    try:
        urllib.request.urlretrieve(url, tmp_file)
        shutil.copy2(target_file, backup_file)
        shutil.move(tmp_file, target_file)
        print("[OTA] Update applied successfully")
    except Exception as e:
        print("[OTA] Update failed:", e)


# Main loop
while True:
    try:
        # Try to read any incoming message
        data, addr = sock.recvfrom(8192)
        try:
            packet = json.loads(data.decode())
        except Exception:
            continue

        # Only process if targeted to this project or ALL
        if packet.get("target") == PROJECT_ID or packet.get("target") == "ALL":
            handle_packet(packet)

    except BlockingIOError:
        # No message received, continue main loop
        pass

    # ===== Main project logic goes here =====
    # Example: simulate work or game loop
    print("Project running main loop...")
    time.sleep(1)  # Replace with real work
