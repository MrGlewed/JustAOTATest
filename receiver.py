import threading, time, random, os, sys

# ----------------- Global state -----------------
last_packet_time = time.time()
IDLE_TIMEOUT = 30  # seconds before screensaver starts
screensaver_running = False
running = True

# ----------------- Terminal -----------------
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# ----------------- Screensaver Games -----------------
def snake_saver(duration=10):
    clear()
    width, height = 30, 10
    snake = [(width//2, height//2)]
    direction = (1, 0)
    for _ in range(duration * 5):
        head = (snake[-1][0] + direction[0], snake[-1][1] + direction[1])
        snake.append(head)
        if len(snake) > 5:
            snake.pop(0)
        clear()
        for y in range(height):
            line = ""
            for x in range(width):
                line += "O" if (x,y) in snake else "."
            print(line)
        direction = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
        time.sleep(0.2)
        if not screensaver_running: return

def pong_saver(duration=10):
    clear()
    width, height = 30, 10
    ball = [width//2, height//2]
    vel = [1,1]
    paddle_y = height//2
    for _ in range(duration * 5):
        ball[0] += vel[0]
        ball[1] += vel[1]
        if ball[0] <= 0 or ball[0] >= width-1: vel[0] *= -1
        if ball[1] <= 0 or ball[1] >= height-1: vel[1] *= -1
        paddle_y += random.choice([-1,0,1])
        clear()
        for y in range(height):
            line = ""
            for x in range(width):
                if x == 2 and y == paddle_y: line += "|"
                elif x == ball[0] and y == ball[1]: line += "O"
                else: line += " "
            print(line)
        time.sleep(0.1)
        if not screensaver_running: return

def tetris_saver(duration=10):
    clear()
    width, height = 20, 10
    for _ in range(duration * 5):
        field = [[" "]*width for _ in range(height)]
        for _ in range(random.randint(1,4)):
            x = random.randint(0,width-2)
            y = random.randint(0,height-2)
            field[y][x] = random.choice(["#", "@", "%", "&"])
        clear()
        for row in field:
            print("".join(row))
        time.sleep(0.2)
        if not screensaver_running: return

# ----------------- Screensaver Controller -----------------
def screensaver_loop():
    global screensaver_running
    while running:
        idle = time.time() - last_packet_time
        if idle >= IDLE_TIMEOUT:
            screensaver_running = True
            for game in [snake_saver, pong_saver, tetris_saver]:
                if not screensaver_running: break
                game(duration=15)
            screensaver_running = False
        time.sleep(1)

# ----------------- Packet update -----------------
def handle_packet(pkt):
    global last_packet_time, screensaver_running
    last_packet_time = time.time()  # reset idle timer
    screensaver_running = False      # stop screensaver immediately
    # dispatch effect/game/message as before...
