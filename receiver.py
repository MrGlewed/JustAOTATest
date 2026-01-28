import socket, json, time, os, sys, random, platform, threading

PORT = 50555
PROJECT_ID = "ALL"

# ================= TERMINAL =================
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# ================= SAFE SOCKET =================
def create_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # allow reuse
    while True:
        try:
            s.bind(("", PORT))
            break
        except OSError as e:
            print(f"[!] Port {PORT} busy, retrying in 2s...")
            time.sleep(2)
    return s

sock = create_socket()
print(f"[+] Listening on UDP port {PORT}")

running = True

# ================= FASTFETCH++ =================
def fastfetch(value=False):
    clear()
    osys = platform.system()
    arch = platform.machine()
    cpu = platform.processor()
    py = sys.version.split()[0]

    logo = {
        "Linux": ["  ___", " | |_", " |___|"],
        "Windows": [" [###]", " |___|", "  |_| "],
        "Darwin": ["  ", " /|\\", "  | "]
    }.get(osys, [" ??? "])

    for l in logo:
        print(l)

    print(f"\nOS: {osys}")
    print(f"ARCH: {arch}")
    print(f"CPU: {cpu}")
    print(f"PY: {py}")

    if value:
        for _ in range(12):
            print(f"REG {random.randint(0,255):02X} -> {random.randint(0,65535):016b}")
            time.sleep(0.1)

# ================= MATRIX =================
def matrix(color="32"):
    clear()
    cols = os.get_terminal_size().columns
    try:
        while running:
            print("\033[" + color + "m" +
                  "".join(random.choice("01") for _ in range(cols)) +
                  "\033[0m")
            time.sleep(0.05)
    except:
        pass

# ================= HEXDUMP =================
def hexdump():
    clear()
    addr = 0
    for _ in range(80):
        row = " ".join(f"{random.randint(0,255):02X}" for _ in range(16))
        print(f"{addr:08X}  {row}")
        addr += 16
        time.sleep(0.03)

# ================= BITWISE CHAOS =================
def chaos():
    clear()
    v = random.randint(0,65535)
    for _ in range(120):
        v ^= (v << random.randint(1,4)) & 0xFFFF
        v ^= (v >> random.randint(1,4))
        print(f"{v:016b}  {v:04X}")
        time.sleep(0.03)

# ================= DNA LADDER =================
def dna():
    clear()
    width = 30
    for i in range(200):
        a = i % width
        b = width - a
        print(" " * a + "01====10" + " " * b)
        time.sleep(0.04)

# ================= TRAIN =================
def train():
    clear()
    train = "/|\\_/=|\\_/=|\\_/="
    for i in range(100):
        print(" " * i + train)
        time.sleep(0.05)
        clear()

# ================= SPIN ARROW =================
def arrow():
    clear()
    frames = ["→", "↓", "←", "↑"]
    for _ in range(100):
        print(random.choice(["101", "010"]) + " " + random.choice(frames))
        time.sleep(0.08)
        clear()

# ================= FAKE HACK =================
def fakehack():
    clear()
    lines = [
        "[*] Scanning ports",
        "[*] Injecting shellcode",
        "[+] Dumping memory",
        "[+] Decrypting blocks",
        "[!] ACCESS GRANTED"
    ]
    for l in lines:
        print(l)
        time.sleep(0.6)

# ================= BOOT =================
def boot():
    clear()
    logs = [
        "BIOS INIT",
        "MEMORY OK",
        "LOADING KERNEL",
        "INIT USERSACE",
        "LOGIN:"
    ]
    for l in logs:
        print(l)
        time.sleep(0.4)

# ================= EASTER EGGS =================
def easter_eggs(msg):
    triggers = {
        "0xdeadbeef": lambda: threading.Thread(target=hexdump).start(),
        "101010": lambda: threading.Thread(target=matrix).start(),
        "xor": lambda: threading.Thread(target=chaos).start(),
        "matrix": lambda: threading.Thread(target=matrix).start(),
        "overflow": lambda: threading.Thread(target=dna).start(),
    }
    for key in triggers:
        if key in msg.lower():
            triggers[key]()

# ================= DISPATCH =================
def handle(pkt):
    global running
    if pkt.get("target") not in (PROJECT_ID, "ALL"):
        return

    name = pkt.get("name")
    msg = pkt.get("message")

    if msg == "__KILL__":
        running = False
        clear()
        print("SYSTEM HALTED")
        sys.exit(0)

    if msg:
        easter_eggs(msg)
        print(msg)

    engines = {
        "FASTFETCH": lambda: threading.Thread(target=fastfetch, args=(False,), daemon=True).start(),
        "FASTFETCH_VALUE": lambda: threading.Thread(target=fastfetch, args=(True,), daemon=True).start(),
        "HEX_MATRIX": lambda: threading.Thread(target=matrix, daemon=True).start(),
        "HEX_DUMP_STREAM": lambda: threading.Thread(target=hexdump, daemon=True).start(),
        "BITWISE_CHAOS": lambda: threading.Thread(target=chaos, daemon=True).start(),
        "DNA": lambda: threading.Thread(target=dna, daemon=True).start(),
        "TRAIN_ASCII": lambda: threading.Thread(target=train, daemon=True).start(),
        "ROTATING_ARROW": lambda: threading.Thread(target=arrow, daemon=True).start(),
        "FAKE_HACK": lambda: threading.Thread(target=fakehack, daemon=True).start(),
        "BOOT": lambda: threading.Thread(target=boot, daemon=True).start(),
    }

    if name in engines:
        engines[name]()

# ================= MAIN LOOP =================
print("NUCLEAR ASCII RECEIVER ONLINE")
while True:
    try:
        data, _ = sock.recvfrom(65535)
        pkt = json.loads(data.decode())
        handle(pkt)
    except Exception as e:
        print(f"[!] Packet error: {e}")
