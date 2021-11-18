import binascii


testString = b'\x01\x02\x03'

print(testString)
print(binascii.hexlify(testString, ' '))

print(binascii.unhexlify(b'010203'))


        