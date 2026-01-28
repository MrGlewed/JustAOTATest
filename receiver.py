import socket, json, time, os, sys, threading, random

PORT = 50555

# ---------------- Terminal ----------------
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# ---------------- Socket ----------------
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("", PORT))

last_packet = time.time()
IDLE_TIMEOUT = 40
screensaver = False
running = True

# ---------------- RISC‑V Boot Emulation ----------------
def riscv_boot():
    clear()
    stages = [
        ("OpenSBI v1.3", 0.6),
        ("Platform: QEMU virt", 0.4),
        ("Hart 0 ready", 0.3),
        ("Jumping to supervisor mode", 0.5),
        ("U-Boot 2024.01 (riscv64)", 0.6),
        ("DRAM: 512 MiB", 0.3),
        ("Loading Linux kernel...", 0.6),
        ("Starting kernel...", 0.4),
    ]

    kernel = [
        "[    0.000000] Linux version 6.7.0-riscv",
        "[    0.112341] SBI specification v1.0 detected",
        "[    0.223512] Zone ranges:",
        "[    0.338291] Memory: 498MB available",
        "[    0.551901] RCU init",
        "[    0.892314] Mounting root filesystem",
        "[    1.203912] systemd[1]: systemd 255 running",
        "[    1.412332] systemd: Starting services",
        "[    2.112981] Network initialized",
        "[    2.804212] Reached target Multi-User",
    ]

    for t, d in stages:
        print(t)
        time.sleep(d)

    for line in kernel:
        print(line)
        time.sleep(random.uniform(0.15, 0.35))

    print("\nArch Linux RISC-V")
    print("riscv64 login:")

# ---------------- Screensaver ----------------
def idle_loop():
    global screensaver
    while running:
        if time.time() - last_packet > IDLE_TIMEOUT:
            screensaver = True
            ascii_spinner()
            screensaver = False
        time.sleep(1)

def ascii_spinner():
    clear()
    frames = ["|", "/", "-", "\\"]
    while screensaver:
        for f in frames:
            print(f"System idle {f}")
            time.sleep(0.15)
            clear()

# ---------------- Dispatch ----------------
def handle(pkt):
    global last_packet, screensaver
    last_packet = time.time()
    screensaver = False

    cmd = pkt.get("command")

    if cmd == "RISC_V_BOOT":
        threading.Thread(target=riscv_boot, daemon=True).start()

    if cmd == "CLEAR":
        clear()

    if cmd == "KILL":
        clear()
        print("System halted.")
        sys.exit(0)

# ---------------- Main ----------------
threading.Thread(target=idle_loop, daemon=True).start()

print("RISC‑V ASCII RECEIVER ONLINE")
while True:
    data, _ = sock.recvfrom(65535)
    try:
        handle(json.loads(data.decode()))
    except:
        pass
