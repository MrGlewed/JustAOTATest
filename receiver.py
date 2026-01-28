import socket, json, time, os, sys, random, platform, threading

PORT = 50555
PROJECT_ID = "ALL"

# ================= TERMINAL =================
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# ================= SAFE SOCKET =================
def create_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    while True:
        try:
            s.bind(("", PORT))
            break
        except OSError:
            print("[!] Port busy, retrying...")
            time.sleep(2)
    return s

sock = create_socket()

running = True
last_packet_time = time.time()
IDLE_TIMEOUT = 30
screensaver_running = False

# ================= FASTFETCH++ =================
def fastfetch(value=False):
    clear()
    osys = platform.system()
    print(f"OS: {osys}")
    print(f"ARCH: {platform.machine()}")
    print(f"PY: {sys.version.split()[0]}")
    if value:
        for _ in range(15):
            print(f"{random.randint(0,65535):016b}  {random.randint(0,255):02X}")
            time.sleep(0.08)

# ================= EFFECTS =================
def matrix():
    clear()
    w = os.get_terminal_size().columns
    while running:
        print("".join(random.choice("01") for _ in range(w)))
        time.sleep(0.05)

def hexdump():
    clear()
    a = 0
    for _ in range(80):
        print(f"{a:08X} " + " ".join(f"{random.randint(0,255):02X}" for _ in range(16)))
        a += 16
        time.sleep(0.03)

def chaos():
    clear()
    v = random.randint(0,65535)
    for _ in range(150):
        v ^= (v << 1) & 0xFFFF
        print(f"{v:016b} {v:04X}")
        time.sleep(0.03)

def dna():
    clear()
    for i in range(200):
        s = i % 20
        print(" " * s + "01====10")
        time.sleep(0.04)

def train():
    clear()
    t = "/|\\_/=|\\_/=|\\_/="
    for i in range(80):
        clear()
        print(" " * i + t)
        time.sleep(0.05)

def arrow():
    clear()
    frames = ["↑","→","↓","←"]
    for _ in range(120):
        clear()
        print(random.choice(["101","010"]), random.choice(frames))
        time.sleep(0.08)

def fakehack():
    clear()
    for l in [
        "[*] Scanning...",
        "[*] Dumping memory",
        "[+] Decrypting blocks",
        "[!] ACCESS GRANTED"
    ]:
        print(l)
        time.sleep(0.6)

def boot():
    clear()
    for l in ["BIOS INIT","LOADING KERNEL","STARTING USERSPACE","login:"]:
        print(l)
        time.sleep(0.4)

# ================= SCREENSAVER GAMES =================
def snake():
    w,h = 30,10
    s = [(15,5)]
    d = (1,0)
    while screensaver_running:
        x,y = s[-1]
        nx,ny = (x+d[0])%w,(y+d[1])%h
        s.append((nx,ny))
        if len(s)>6: s.pop(0)
        clear()
        for y in range(h):
            print("".join("O" if (x,y) in s else "." for x in range(w)))
        d = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        time.sleep(0.2)

def pong():
    w,h = 30,10
    bx,by = 15,5
    vx,vy = 1,1
    py = 5
    while screensaver_running:
        bx+=vx; by+=vy
        if bx<=0 or bx>=w-1: vx*=-1
        if by<=0 or by>=h-1: vy*=-1
        py += random.choice([-1,0,1])
        clear()
        for y in range(h):
            print("".join(
                "O" if (x,y)==(bx,by) else "|" if (x,y)==(2,py) else " "
                for x in range(w)
            ))
        time.sleep(0.1)

def tetris():
    w,h=20,10
    while screensaver_running:
        clear()
        field=[[" "]*w for _ in range(h)]
        for _ in range(random.randint(1,4)):
            field[random.randint(0,h-1)][random.randint(0,w-1)]="#"
        for r in field: print("".join(r))
        time.sleep(0.2)

def screensaver_loop():
    global screensaver_running
    while running:
        if time.time()-last_packet_time>IDLE_TIMEOUT:
            screensaver_running=True
            for g in [snake,pong,tetris]:
                if not screensaver_running: break
                threading.Thread(target=g,daemon=True).start()
                time.sleep(15)
            screensaver_running=False
        time.sleep(1)

# ================= DISPATCH =================
def handle(pkt):
    global last_packet_time, screensaver_running
    last_packet_time=time.time()
    screensaver_running=False

    if pkt.get("target") not in ("ALL",PROJECT_ID): return

    if pkt.get("message")=="__KILL__":
        clear(); print("HALTED"); sys.exit(0)

    if pkt.get("message"):
        print(pkt["message"])

    cmds={
        "FASTFETCH":lambda:fastfetch(False),
        "FASTFETCH_VALUE":lambda:fastfetch(True),
        "HEX_MATRIX":matrix,
        "HEX_DUMP_STREAM":hexdump,
        "BITWISE_CHAOS":chaos,
        "DNA":dna,
        "TRAIN_ASCII":train,
        "ROTATING_ARROW":arrow,
        "FAKE_HACK":fakehack,
        "BOOT":boot
    }

    if pkt.get("name") in cmds:
        threading.Thread(target=cmds[pkt["name"]],daemon=True).start()

# ================= START =================
threading.Thread(target=screensaver_loop,daemon=True).start()
print("☢️ NUCLEAR RECEIVER ONLINE")
while True:
    data,_=sock.recvfrom(65535)
    try: handle(json.loads(data.decode()))
    except: pass
