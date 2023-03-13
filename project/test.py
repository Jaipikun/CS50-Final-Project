import struct
import binascii

t = []
for i in range(-32767,32767+1):
    
    if i == 32767 or i == round(-32767) or i == 0:
        t.append(struct.pack("<h",i))

t2 = []
print(t[0][1])
for i in t:
    t2.append(struct.unpack("<h",i))
    
print(t2[0][0])


