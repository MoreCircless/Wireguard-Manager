#!/usr/bin/python3

import subprocess
import argparse
from colorama import Fore, Back, Style


def levantar_vpn():
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

def cerrar_vpn():
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
    """La funcion devuelve Checkea si existe la wg0 en las interfaces de red, devuelve True si existe, si no, devuelve False"""
    try:
        output = subprocess.run(["ip", "a"], check=True, capture_output=True, text=True)
        flag = None
        if "wg0" in output.stdout:
            flag = True
        else:
            flag = False

    except subprocess.CalledProcessError as e:
        print(e)

    return flag 


def checkstatus(flag: bool):
    if flag == True:
        print(Fore.GREEN + "  ✓ -> VPN is Up \n" + Fore.RESET)
    else:
        print(Fore.RED + "  x -> VPN is Down" + Fore.RESET)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
                    prog='VPN Setter',
                    description='Activa o desactiva la VPN',
                    epilog= Fore.MAGENTA + "Script hecho por Pavlo y @morcircles" + Fore.RESET,
                    )
    
    parser.add_argument('action', choices=['u', 'd', "s"], help=f'Acción a realizar con la VPN: "u" para levantarla, "d" para cerrarla o "s" para ver el estado')
    
    args = parser.parse_args()
    
    if args.action == 'u':
        levantar_vpn()
    elif args.action == 'd':
        cerrar_vpn()
    elif args.action == "s":
        estado = status()
        checkstatus(estado)

