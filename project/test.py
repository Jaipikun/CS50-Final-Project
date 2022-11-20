import struct
import binascii
x = struct.pack("<h",233)
print(x)
x = struct.unpack("<h",x)
print(x[0])