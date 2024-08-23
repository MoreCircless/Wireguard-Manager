#!/usr/bin/python3

import subprocess
import argparse
import os
from colorama import Fore, Back, Style

def install_vpn():

    user = str(input(Fore.BLUE + "Are you sure about installing WireGuard? [Y/N] "))

    if user.lower() == "y":

        if os.getuid() == 0:
            try:
                output=subprocess.run(["apt", "install","wireguard","-y"],check=True)
                output=subprocess.run(["apt", "install","resolvconf","-y"],check=True)
                
            
            except subprocess.CalledProcessError as e:
                print(e)
                return 
        else:
            print(Fore.RED + "Execute the script as root to install WireGuard properly!" + Fore.RESET)
            return
        
    user = input(Fore.GREEN + "WireGuard has been installed succesfully! Do you want to add a client to the service?[Y/N] " + Fore.RESET)
    
    if user.lower() == 'y':
        add_client()



def add_client():

    if os.getuid() == 0:
        user = str(input(Fore.BLUE + "Specify the absolute path of the configuration file: "))
        try:
            output=subprocess.run(["cp", user,"/etc/wireguard/wg0.conf"],check=True)
        except subprocess.CalledProcessError as e:
        
            print(Fore.RED)
            print(e)
            print(Fore.RESET)
            return 

    else:
        print(Fore.RED + "Execute the script as root to add the client!" + Fore.RESET)

        return 
    
    print(Fore.GREEN + "The client has been added succesfully to WireGuard!" + Fore.RESET)
    
    user = str(input(Fore.BLUE + "Do you want to enable the WireGuard daemon? [Y/N]: " + Fore.RESET))

    if user.lower() == 'y':
        try:
            output=subprocess.run(["systemctl", "enable","wg-quick@wg0"],check=True)
            output=subprocess.run(["systemctl", "start","wg-quick@wg0"],check=True)
        
        except subprocess.CalledProcessError as e:
            print(e)
            return 



    



def activate_vpn():

    try:
        subprocess.run(["systemctl","start", "wg-quick@wg0"],check=True)
        subprocess.run(["systemctl","enable", "wg-quick@wg0"],check=True)

    except subprocess.CalledProcessError as e:
    
        print(e)
        return 



def on_vpn():
    print(Fore.CYAN + "\nTrying to set up the VPN ...\n" + Fore.RESET)
    try:
        if status() == False:
            output = subprocess.run(['wg-quick', 'up', "wg0"], check=True, capture_output=True, text=True)
            print( Fore.GREEN + "VPN has been succesfully activated" + Fore.RESET)
            print(output.stdout)
        else:
            print(Fore.RED + "VPN is alredy active!" + Fore.RESET)

    except subprocess.CalledProcessError as e:
        print(e)
        return 

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
        return 


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
        return 
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
    
    parser.add_argument('action', choices=['u', 'd', 's', 'i', 'a'], help=f'Action:"u" for turn ON the VPN/ "d" for turn OFF the VPN/ "s" for check the status of the vpn')


    args = parser.parse_args()
    
    if args.action == 'u':
        on_vpn()
    elif args.action == 'd':
        off_vpn()
    elif args.action == "s":
        state = status()
        checkstatus(state)
    elif args.action == "i":
        install_vpn()
    elif args.action == "a":
        add_client()

    else:
        print(Fore.RED + "Invalid parameter!" + Fore.RESET)

