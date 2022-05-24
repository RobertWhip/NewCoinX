# External
import socket

# Internal
import configs.constants as constants

# The Challenger's software
# It should connect to the blockchain core's challenger 
# service. Challengers (same as bitcoin miners) should 
# get/complete challenges via this software.

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((constants.HOST, constants.PORT))
    s.sendall(b"Hello, world")
    data = s.recv(1024)

print(f"Received {data!r}")