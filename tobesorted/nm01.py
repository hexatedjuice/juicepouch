from pwn import *

s = remote('ggcs-nm01.allyourbases.co',6167)

stuff = s.recv(1024)
print(stuff)
s.sendline(str(56154))
stuff = s.recv(1024) 
# print(stuff)
s.sendline(str(1764))
stuff = s.recv(1024)
print(stuff)
s.close()