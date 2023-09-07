RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
GRAY="\033[37m"
NOCOLOR="\033[0m"

def success(text):
    """Return success status message"""
    return GREEN + "[+] " + NOCOLOR + text

def failure(text):
    """Return failure status message"""
    return RED + "[!] " + NOCOLOR + text

def warning(text):
    """Return warning status message"""
    return YELLOW + "[+] " + NOCOLOR + text

def info(text):
    """Return info status message"""
    return GRAY + "[+] " + NOCOLOR + text
