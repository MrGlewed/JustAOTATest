import socket, json, time, os, sys, random, platform, threading

PORT = 50555
PROJECT_ID = "ALL"

# ---------------- Terminal ----------------
def clear():
    os.system("cls" if os.name=="nt" else "clear")

# ---------------- Socket ----------------
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("", PORT))

# ---------------- Global State ----------------
running = True
last_packet = time.time()
IDLE_TIMEOUT = 40
screensaver = False

# ---------------- Screensaver Games ----------------
def snake():
    w,h=30,10; s=[(w//2,h//2)]; d=(1,0)
    while screensaver:
        x,y=s[-1]; nx,ny=(x+d[0])%w,(y+d[1])%h; s.append((nx,ny))
        if len(s)>6: s.pop(0)
        clear()
        for y in range(h): print("".join("O" if (x,y) in s else "." for x in range(w)))
        d=random.choice([(1,0),(-1,0),(0,1),(0,-1)]); time.sleep(0.2)

def pong():
    w,h=30,10; bx,by=w//2,h//2; vx,vy=1,1; py=h//2
    while screensaver:
        bx+=vx; by+=vy
        if bx<=0 or bx>=w-1: vx*=-1
        if by<=0 or by>=h-1: vy*=-1
        py+=random.choice([-1,0,1])
        clear()
        for y in range(h):
            print("".join("O" if (x,y)==(bx,by) else "|" if (x,y)==(2,py) else " " for x in range(w)))
        time.sleep(0.1)

def tetris():
    w,h=20,10
    while screensaver:
        clear()
        field=[[" "]*w for _ in range(h)]
        for _ in range(random.randint(1,4)):
            field[random.randint(0,h-1)][random.randint(0,w-1)]="#"
        for r in field: print("".join(r))
        time.sleep(0.2)

def screensaver_loop():
    global screensaver
    while running:
        if time.time()-last_packet>IDLE_TIMEOUT:
            screensaver=True
            for g in [snake,pong,tetris]:
                if not screensaver: break
                threading.Thread(target=g,daemon=True).start()
                time.sleep(15)
            screensaver=False
        time.sleep(1)

# ---------------- ASCII Effects ----------------
def matrix(): clear(); w=os.get_terminal_size().columns; [print("".join(random.choice("01") for _ in range(w))) or time.sleep(0.05) for _ in range(200)]
def hexdump(): clear(); a=0; [print(f"{a:08X} "+" ".join(f"{random.randint(0,255):02X}" for _ in range(16))) or time.sleep(0.03) or a.__iadd__(16) for _ in range(80)]
def chaos(): clear(); v=random.randint(0,65535); [print(f"{v:016b} {v:04X}") or time.sleep(0.03) or v.__ixor__((v<<1)&0xFFFF) for _ in range(150)]
def dna(): clear(); [print(" "* (i%20) +"01====10") or time.sleep(0.04) for i in range(200)]
def train(): clear(); t="/|\\_/=|\\_/=|\\_/="; [clear() or print(" "*i+t) or time.sleep(0.05) for i in range(80)]
def arrow(): clear(); f=["↑","→","↓","←"]; [clear() or print(random.choice(["101","010"]),random.choice(f)) or time.sleep(0.08) for _ in range(120)]
def fakehack(): clear(); [print(l) or time.sleep(0.6) for l in ["[*] Scanning...","[*] Dumping memory","[+] Decrypting blocks","[!] ACCESS GRANTED"]]
def boot(): clear(); [print(l) or time.sleep(0.4) for l in ["BIOS INIT","LOADING KERNEL","STARTING USERSPACE","login:"]]

# ---------------- Fastfetch ----------------
def fastfetch(value=False):
    clear()
    print(f"OS: {platform.system()}\nARCH: {platform.machine()}\nCPU: {platform.processor()}\nPY: {sys.version.split()[0]}")
    if value:
        for _ in range(15): print(f"{random.randint(0,65535):016b}  {random.randint(0,255):02X}"); time.sleep(0.08)

# ---------------- RISC-V Boot Emulation ----------------
def riscv_boot():
    clear()
    stages=[("OpenSBI v1.3",0.6),("QEMU virt",0.4),("Hart0 ready",0.3),("Jumping to supervisor mode",0.5),("U-Boot 2024.01",0.6),
            ("DRAM: 512MiB",0.3),("Loading Linux kernel...",0.6),("Starting kernel...",0.4)]
    kernel_logs=[
        "[0.000000] Linux 6.7.0-riscv",
        "[0.112341] SBI v1.0 detected",
        "[0.223512] Zone ranges:",
        "[0.338291] Memory: 498MB available",
        "[0.551901] RCU init",
        "[0.892314] Mounting root filesystem",
        "[1.203912] systemd[1]: systemd 255 running",
        "[1.412332] systemd: Starting services",
        "[2.112981] Network initialized",
        "[2.804212] Reached target Multi-User",
    ]
    for t,d in stages: print(t); time.sleep(d)
    for l in kernel_logs: print(l); time.sleep(random.uniform(0.15,0.35))
    print("\nArch Linux RISC-V\nriscv64 login:")

# ---------------- Easter Eggs ----------------
def easter(msg):
    triggers={"0xdeadbeef":hexdump,"101010":matrix,"xor":chaos,"matrix":matrix,"overflow":dna}
    for k,v in triggers.items():
        if k in msg.lower(): threading.Thread(target=v,daemon=True).start()

# ---------------- Dispatch ----------------
def handle(pkt):
    global last_packet,screensaver
    last_packet=time.time(); screensaver=False

    if pkt.get("target") not in ("ALL",PROJECT_ID): return
    if pkt.get("message")=="__KILL__": clear(); print("HALTED"); sys.exit(0)
    if pkt.get("message"): print(pkt["message"]); easter(pkt["message"])

    cmds={
        "HEX_MATRIX":matrix,
        "HEX_DUMP_STREAM":hexdump,
        "BITWISE_CHAOS":chaos,
        "DNA":dna,
        "TRAIN_ASCII":train,
        "ROTATING_ARROW":arrow,
        "FAKE_HACK":fakehack,
        "BOOT":boot,
        "FASTFETCH":lambda:fastfetch(False),
        "FASTFETCH_VALUE":lambda:fastfetch(True),
        "RISC_V_BOOT":riscv_boot
    }
    if pkt.get("name") in cmds: threading.Thread(target=cmds[pkt.get("name")],daemon=True).start()

# ---------------- Main ----------------
threading.Thread(target=screensaver_loop,daemon=True).start()
print("☢️ MODULAR ASCII RECEIVER ONLINE")
while True:
    data,_=sock.recvfrom(65535)
    try: handle(json.loads(data.decode()))
    except: pass
