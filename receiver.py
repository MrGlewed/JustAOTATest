import socket
import json
import time
import random
import os
import subprocess

PROJECT_ID = "ascii_project"  # change if needed
PORT = 50555

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("", PORT))
sock.setblocking(False)

print(f"[RECEIVER] Listening as '{PROJECT_ID}' on port {PORT}\n")

# ---------------- ASCII EFFECTS ----------------

def train_ascii(repeat, loop_forever, delay):
    chars = ["/", "|", "\\", "_", "="]
    width = 60
    while loop_forever or repeat > 0:
        for x in range(width):
            print(" " * x + "".join(random.choice(chars) for _ in range(12)), end="\r")
            time.sleep(delay)
        repeat -= 1
    print()

def rotating_arrow_01(repeat, loop_forever, delay):
    frames = [
        "1\n 1\n  1\n   1",
        "   0\n  0\n 0\n0"
    ]
    while loop_forever or repeat > 0:
        for f in frames:
            print(f)
            time.sleep(delay)
        repeat -= 1

def chromosome_ladder(repeat, loop_forever, delay):
    ladder = ["0 | 1", "1 | 0", "0-1", "1-0"]
    while loop_forever or repeat > 0:
        for row in ladder:
            print(row)
            time.sleep(delay)
        print()
        repeat -= 1

def binary_loop(repeat, loop_forever, delay):
    while loop_forever or repeat > 0:
        print("".join(random.choice("01") for _ in range(128)))
        time.sleep(delay)
        repeat -= 1

# ---------------- COMMAND EXECUTION ----------------

def run_command(cmd):
    try:
        output = subprocess.check_output(cmd, shell=True, text=True)
        print(output)
    except Exception as e:
        print(f"[COMMAND ERROR] {e}")

# ---------------- PACKET HANDLER ----------------

def handle_packet(pkt):
    t = pkt.get("type")
    repeat = pkt.get("repeat", 1)
    loop_forever = pkt.get("loop_forever", False)
    delay = pkt.get("delay", 0.1)

    if t == "TRAIN_ASCII":
        train_ascii(repeat, loop_forever, delay)
    elif t == "ROTATING_ARROW_01":
        rotating_arrow_01(repeat, loop_forever, delay)
    elif t == "CHROMOSOME":
        chromosome_ladder(repeat, loop_forever, delay)
    elif t == "BINARY":
        binary_loop(repeat, loop_forever, delay)
    elif t == "MESSAGE":
        print(f"[MESSAGE] {pkt.get('message','')}")
    elif t == "COMMAND":
        print(f"[COMMAND] {pkt.get('command')}")
        run_command(pkt.get("command",""))
    elif t == "UPDATE":
        print(f"[OTA] {pkt.get('file')} <- {pkt.get('url')}")
    else:
        print("[UNKNOWN PACKET]", pkt)

# ---------------- MAIN LOOP ----------------

while True:
    try:
        data, _ = sock.recvfrom(8192)
        pkt = json.loads(data.decode())
        if pkt.get("target") in (PROJECT_ID, "ALL"):
            handle_packet(pkt)
    except BlockingIOError:
        pass
    time.sleep(0.05)
