import os
import platform
import socket

sysinfo = platform.platform()

s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
def send_os():
    #print(f"system info = {sysinfo}")
    return sysinfo



