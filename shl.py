import os
import colorama
import random
import requests
import getpass
import subprocess
import sys
import time as t
from colorama import Fore, Style, init

init(autoreset=True)

# map extensions to filetypes
filetypes = {
    ".py": "Python File",
    ".lua": "Lua File",
    ".luau": "Luau File",
    ".ini": "initialization File",
    ".txt": "Text File Document",
    ".Ink": "Windows Shortcut File",
}

def date():
    local_time = t.localtime()
    formatted = t.strftime("%Y-%m-%d %H:%M:%S", local_time)
    print(formatted)

def tree(folder="", prefix=""):
    if not os.path.exists(folder):
        print(f"Folder '{folder}' not found.")
        return
    try:
        files = os.listdir(folder if folder == "" else os.getcwd())
        for i, f in enumerate(files):
            path = os.path.join(folder, f)
            connector = "└── " if i == len(files) - 1 else "├── "
            print(prefix + connector + f)
            if os.path.isdir(path):
                extension = "    " if i == len(files) - 1 else "│   "
                tree(path, prefix + extension)
    except PermissionError:
        print(prefix + "[Permission Denied]")

def touch(filename=None):
    try:
        if not filename:
            open("New document text", 'a').close()
            print(f"File '{filename}' created.")
        else:
            open(filename, 'a').close()
            print(f"File '{filename}' created.")
    except Exception as e:
        print(f"touch: {e}")

def checkupdate():
    VERSION_URL = "https://raw.githubusercontent.com/ThanaphatSuporn/Shellpy/main/version.txt"
    LOCAL_VERSION_FILE = r"C:\Users\admin\OneDrive\เดสก์ท็อป\Folder_clean\Code\Pystarp\version.txt"
    try:
        remote_version = requests.get(VERSION_URL, timeout=5).text.strip()
        if os.path.exists(LOCAL_VERSION_FILE):
            with open(LOCAL_VERSION_FILE, "r") as f:
                local_version = f.read().strip()
        else:
            local_version = "unknown"
        if remote_version != local_version:
            print(f"{Fore.YELLOW}Update available! Now running auto updater{Style.RESET_ALL}")
            os.system(r"python 'C:\Users\admin\OneDrive\เดสก์ท็อป\Folder_clean\Code\Pystarp\autoupdater.py'")
        else:
            print(f"{Fore.GREEN}You are up to date. Version: {local_version}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Update check failed: {e}{Style.RESET_ALL}")

def help():
    print("""
-------> Help <-------
    exit/quit -> Quit shell
    cd [filepath/..] -> go to that path/return to previous path
    pwd -> show current path [deprecated]
    clear -> clear output
    ls ->  check all file/dir in directory
    del [filename/path] -> delete file or directory
    tree [blank/path] -> tree in directory if access denied it will give error
    lookforupdate -> Check update if it available it will run auto updater
    touch [Filename/blank] ->  Create new files
""")

def commands(cmds):
    cmds = cmds.strip()
    if not cmds:
        return
    if cmds in ["exit", "quit"]:
        print("Exiting shell...")
        exit(0)
    elif cmds == "help":
        help()
    elif cmds == "date":
        date()
    elif cmds.startswith("cd "):
        target = cmds[3:].strip()
        try:
            os.chdir(os.path.expanduser(target))
        except Exception as e:
            print(f"cd: {e}")
    elif cmds == "pwd":
        print(os.getcwd())
    elif cmds.startswith("tree "):
        tree(cmds[5:])
    elif cmds == "tree":
        tree()
    elif cmds == "clear":
        os.system("cls" if os.name == "nt" else "clear")
    elif cmds == "ls":
        lists = os.listdir()
        path = os.getcwd()
        files = 0
        folders = 0
        print(f"--->[{path}]<---")
        for i in lists:
            if os.path.isdir(i):
                print(f"{Fore.BLUE}{i}{Style.RESET_ALL} [Directory]")
                folders += 1
            elif os.path.isfile(i):
                ext = os.path.splitext(i)[1].lower()
                if ext in filetypes:
                    print(f"{Fore.GREEN}{i}{Style.RESET_ALL} [File - {filetypes[ext]}]")
                else:
                    print(f"{i} [File]")
                files += 1
        print("-------")
        print(f"{files} Found files | {folders} Found directory")
    elif cmds.startswith("del "):
        target = cmds[4:].strip()
        try:
            os.remove(os.path.expanduser(target))
        except FileExistsError as notexisted:
            print(f"del: {notexisted}")
        except Exception as e:
            print(f"del: {e}")
    elif cmds == "lookforupdate":
        checkupdate()
    else:
        print(f"{Fore.RED}Unknown command: {cmds}")

def shell():
    user = getpass.getuser()
    if os.name == "nt":
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            is_admin = False
    else:
        is_admin = (os.geteuid() == 0)
    role = "admin" if is_admin else "user"
    while True:
        try:
            path = os.getcwd()
            print(f"{Fore.LIGHTMAGENTA_EX}[{user}@{role}]&[{path}]")
            cmd = input(f"{Fore.LIGHTGREEN_EX}$ ")
            commands(cmd)
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit.")
        except EOFError:
            print("\nExiting shell.")
            break

if __name__ == "__main__":
    shell()
