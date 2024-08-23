#!/usr/bin/python3

import subprocess
import argparse
from colorama import Fore, Back, Style

def on_vpn():
    print(Fore.CYAN + "\nTrying to set up the VPN ...\n" + Fore.RESET)
    try:
        if status() == False:
            output = subprocess.run(['wg-quick', 'up', "wg0"], check=True, capture_output=True, text=True)
            print( Fore.GREEN + "VPN has been succesfully set UP" + Fore.RESET)
            print(output.stdout)
        else:
            print(Fore.RED + "VPN is alredy active!" + Fore.RESET)

    except subprocess.CalledProcessError as e:
        print(e)

def off_vpn():
    print(Fore.CYAN + "\nTrying to set down the VPN...\n" + Fore.RESET)
    try:
        if status() == True:
            output = subprocess.run(['wg-quick', 'down', "wg0"], check=True, capture_output=True, text=True)
            print(Fore.GREEN + "VPN has been closed succesfully" + Fore.RESET)
            print(output.stdout)
        else:
            print(Fore.RED + "VPN is alredy down!" + Fore.RESET)


    except subprocess.CalledProcessError as e:
        print(e)


def status() -> bool:
    """Function checks if "wg0" exist in the net interfaces, returns True if it exist, else, returns False"""
    try:
        output = subprocess.run(["ip", "a"], check=True, capture_output=True, text=True)
        state = None
        if "wg0" in output.stdout:
            state = True
        else:
            state = False

    except subprocess.CalledProcessError as e:
        print(e)

    return state


def checkstatus(state: bool):
    if state == True:
        print(Fore.GREEN + "  ✓ -> VPN is Up \n" + Fore.RESET)
    else:
        print(Fore.RED + "  x -> VPN is Down" + Fore.RESET)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
                    prog='VPN Setter for WireGuard',
                    description='Controls the normal flow of putting on and off the VPN',
                    epilog= Fore.MAGENTA + "Script made by @PdotG y @morecircless" + Fore.RESET,
                    )
    
    parser.add_argument('action', choices=['u', 'd', "s"], help=f'Action:"u" for turn ON the VPN/ "d" for turn OFF the VPN/ "s" for check the status of the vpn')


    args = parser.parse_args()
    
    if args.action == 'u':
        on_vpn()
    elif args.action == 'd':
        off_vpn()
    elif args.action == "s":
        state = status()
        checkstatus(state)
    else:
        print(Fore.RED + "Not valid parameter!" + Fore.RESET)

