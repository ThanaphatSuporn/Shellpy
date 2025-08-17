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
    # get current local time
    local_time = t.localtime()
    # format it nicely
    formatted = t.strftime("%Y-%m-%d %H:%M:%S", local_time)
    print(formatted)

def tree(folder=".", prefix=""):
    if not os.path.exists(folder):
        print(f"Folder '{folder}' not found.")
        return

    try:
        files = os.listdir(folder)
        for i, f in enumerate(files):
            path = os.path.join(folder, f)
            connector = "└── " if i == len(files) - 1 else "├── "
            print(prefix + connector + f)

            if os.path.isdir(path):
                extension = "    " if i == len(files) - 1 else "│   "
                tree(path, prefix + extension)
    except PermissionError:
        print(prefix + "[Permission Denied]")
        


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
""")

def commands(cmds):
    cmds = cmds.strip()
    if not cmds:
        return

    # exit shell
    if cmds in ["exit", "quit"]:
        print("Exiting shell...")
        exit(0)

    elif cmds == "help":
        help()
    elif cmds == "date":
        date()
    # change directory
    elif cmds.startswith("cd "):
        target = cmds[3:].strip()
        try:
            os.chdir(os.path.expanduser(target))
        except Exception as e:
            print(f"cd: {e}")

    # print working directory
    elif cmds == "pwd":
        print(os.getcwd())
    elif cmds.startswith("tree "):
        tree(cmds[5:])
    elif cmds == "tree":
        tree()
    # clear screen
    elif cmds == "clear":
        os.system("cls" if os.name == "nt" else "clear")
    # list directory contents
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
    else:
        print(f"{Fore.RED}Unknown command: {cmds}")

def shell():
    user = getpass.getuser()
    # check if admin/root
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
