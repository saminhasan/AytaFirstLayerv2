import socket
hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname + ".local")
print("Computer Name is : "+hostname)
print("Computer IP Address is : "+IPAddr)
