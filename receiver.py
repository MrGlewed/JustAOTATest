import socket, json, time, os, random, math, platform

PORT = 50555
PROJECT_ID = "ALL"

# ================== TERMINAL ==================
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# ================== STATE ==================
state = {
    "stop": False,
    "priority": 0,
    "last_packet": time.time(),
    "screensaver": False
}

# ================== NETWORK ==================
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", PORT))

# ================== EFFECT HELPERS ==================
def rand_hex(n):
    return "".join(random.choice("0123456789ABCDEF") for _ in range(n))

def rand_bin(n):
    return "".join(random.choice("01") for _ in range(n))

# ================== 1️⃣ HEXDUMP ENGINE ==================
def hex_dump_stream(delay=0.05):
    addr = 0x7FFFA000
    while True:
        lines = []
        for _ in range(16):
            bytes_ = [random.randint(0, 255) for _ in range(8)]
            hexs = " ".join(f"{b:02X}" for b in bytes_)
            ascii_ = "".join(chr(b) if 32 <= b < 127 else "." for b in bytes_)
            lines.append(f"{addr:08X}: {hexs:<23} |{ascii_}|")
            addr += 8
        clear()
        print("\n".join(lines))
        time.sleep(delay)

# ================== 2️⃣ BINARY REGISTERS ==================
def binary_registers(delay=0.1):
    regs = ["RAX", "RBX", "RCX", "RDX", "RSP", "RBP"]
    values = {r: random.getrandbits(32) for r in regs}

    while True:
        clear()
        for r in regs:
            values[r] ^= random.getrandbits(3)
            print(f"{r}: {values[r]:032b}")
        time.sleep(delay)

# ================== 3️⃣ BITWISE CHAOS + VALUE FLOW ==================
def bitwise_chaos(delay=0.08):
    val = random.randint(0, 255)
    ops = ["XOR", "SHL", "SHR", "ROL"]

    while True:
        op = random.choice(ops)
        old = val

        if op == "XOR":
            val ^= random.randint(1, 255)
        elif op == "SHL":
            val = (val << 1) & 0xFF
        elif op == "SHR":
            val >>= 1
        elif op == "ROL":
            val = ((val << 1) | (val >> 7)) & 0xFF

        clear()
        print(f"[ VALUE FLOW ]\n")
        print(f"DEC : {old}")
        print(f"HEX : 0x{old:02X}")
        print(f"BIN : {old:08b}")
        print("\n ↓ " + op + " ↓\n")
        print(f"DEC : {val}")
        print(f"HEX : 0x{val:02X}")
        print(f"BIN : {val:08b}")
        time.sleep(delay)

# ================== 4️⃣ HEX MATRIX + BINARY WALL ==================
def hex_matrix(delay=0.04):
    width = os.get_terminal_size().columns
    while True:
        line = []
        for _ in range(width):
            if random.random() < 0.3:
                line.append(random.choice("01"))
            else:
                line.append(random.choice("0123456789ABCDEF"))
        clear()
        print("".join(line))
        time.sleep(delay)

def binary_wall(delay=0.03):
    width = os.get_terminal_size().columns
    while True:
        clear()
        for _ in range(20):
            print(rand_bin(width))
        time.sleep(delay)

# ================== 5️⃣ FASTFETCH++ ==================
def fastfetch(value_mode=False):
    clear()
    uptime = int(time.time() - ps_start)
    cpu = random.randint(10, 90)
    ram = random.randint(20, 95)

    if value_mode:
        print("FASTFETCH++ (VALUE MODE)\n")
        print(f"CPU_BIN     : {cpu:08b}")
        print(f"RAM_HEX     : 0x{ram:02X}")
        print(f"UPTIME_TICK : {uptime:016b}")
    else:
        print("FASTFETCH++\n")
        print(f"OS      : {platform.system()} {platform.release()}")
        print(f"CPU     : {'█'* (cpu//10)}{'░'*(10-cpu//10)} {cpu}%")
        print(f"RAM     : {'█'* (ram//10)}{'░'*(10-ram//10)} {ram}%")
        print(f"UPTIME  : {uptime}s")

# ================== 6️⃣ EASTER EGGS ==================
def easter_eggs(msg):
    triggers = {
        "0xdeadbeef": lambda: hex_dump_stream(0.02),
        "101010": lambda: binary_wall(0.02),
        "xor": lambda: bitwise_chaos(0.05),
        "matrix": lambda: hex_matrix(0.03),
        "overflow": lambda: binary_registers(0.05),
    }

    for key in triggers:
        if key in msg.lower():
            triggers[key]()

# ================== DISPATCH ==================
def dispatch(packet):
    name = packet.get("name", "")
    msg = packet.get("message", "")

    if msg:
        easter_eggs(msg)
        clear()
        print(msg)
        return

    if name == "HEX_DUMP_STREAM":
        hex_dump_stream()
    elif name == "BINARY_REGISTERS":
        binary_registers()
    elif name == "BITWISE_CHAOS":
        bitwise_chaos()
    elif name == "HEX_MATRIX":
        hex_matrix()
    elif name == "BINARY_WALL":
        binary_wall()
    elif name == "FASTFETCH":
        fastfetch(False)
    elif name == "FASTFETCH_VALUE":
        fastfetch(True)

# ================== MAIN ==================
ps_start = time.time()
print("Receiver running...")

while True:
    data, _ = sock.recvfrom(65535)
    packet = json.loads(data.decode())

    if packet.get("target") not in ("ALL", PROJECT_ID):
        continue

    dispatch(packet)
