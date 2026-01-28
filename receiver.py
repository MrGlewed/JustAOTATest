import socket
import json
import time
import random
import sys
import os

PROJECT_ID = "ascii_project"  # change per device/project
PORT = 50555

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("", PORT))
sock.setblocking(False)

print(f"[ASCII RECEIVER] '{PROJECT_ID}' listening on port {PORT}...")

# ---------------- ASCII Animations ----------------
def giant_arrow(repeat, loop_forever, delay):
    arrows = [
        "   ^   \n  ^^^  \n ^^^^^ \n^^^^^^^\n   |   ",
        "   >   \n   >>  \n >>>>> \n>>>>>>>\n   |   ",
        "   v   \n  vvv  \n vvvvv \nvvvvvvv\n   |   ",
        "   <   \n  <<   \n <<<<< \n<<<<<<<\n   |   "
    ]
    count = 0
    while loop_forever or count < repeat:
        for a in arrows:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(a)
            time.sleep(delay)
        count += 1

def ascii_train(repeat, loop_forever, delay):
    train = "🚂===>"
    width = 50
    count = 0
    while loop_forever or count < repeat:
        for pos in range(width):
            print(" " * pos + train, end="\r")
            time.sleep(delay)
        count += 1
    print()

def center_spinner(repeat, loop_forever, delay):
    frames = ["   |   \n   |   \n   |   ", "   /   \n   /   \n   /   ",
              "   -   \n   -   \n   -   ", "   \\   \n   \\   \n   \\   "]
    count = 0
    while loop_forever or count < repeat:
        for f in frames:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f)
            time.sleep(delay)
        count += 1

def matrix_rain(repeat, loop_forever, delay, color="green"):
    COLORS = {"green":"\033[32m", "red":"\033[31m", "blue":"\033[34m",
              "cyan":"\033[36m", "reset":"\033[0m"}
    rain_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    color_code = COLORS.get(color, COLORS["green"])
    count = 0
    while loop_forever or count < repeat:
        os.system('cls' if os.name == 'nt' else 'clear')
        for _ in range(20):
            line = "".join(random.choice(rain_chars + " ") for _ in range(80))
            print(color_code + line + COLORS["reset"])
        count += 1
        time.sleep(delay)

def binary_loop(repeat, loop_forever, delay):
    count = 0
    while loop_forever or count < repeat:
        print("".join(random.choice("01") for _ in range(128)))
        count += 1
        time.sleep(delay)

# ---------------- Packet Dispatcher ----------------
def handle_packet(packet):
    pkt_type = packet.get("type")
    repeat = packet.get("repeat", 1)
    loop_forever = packet.get("loop_forever", False)
    delay = packet.get("delay", 0.1)
    color = packet.get("color", "green")

    if pkt_type == "GIANT_ARROW":
        giant_arrow(repeat, loop_forever, delay)
    elif pkt_type == "ASCII_TRAIN":
        ascii_train(repeat, loop_forever, delay)
    elif pkt_type == "CENTER_SPINNER":
        center_spinner(repeat, loop_forever, delay)
    elif pkt_type == "MATRIX_RAIN":
        matrix_rain(repeat, loop_forever, delay, color)
    elif pkt_type == "BINARY":
        binary_loop(repeat, loop_forever, delay)
    elif pkt_type == "UPDATE":
        print(f"[UPDATE] {packet.get('file')} <- {packet.get('url')}")
    else:
        print(f"[UNKNOWN] {packet}")

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
