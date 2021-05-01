def binary(item):
    x = bin(int(str(item), 0))[2:]
    pad = ''
    if len(x)<32:
        pad = '0'*(32-len(x))
    x = pad + x
    return x
print(binary(32))

def trunc(item, length):
    item = binary(item)
    if len(item) > length:
            rem = len(item) - length
            item = item[rem:]
    return int(item, 2)

def _left_rotate(n, b):
    n = str(n)
    if n[:2] == '0b':
        n = n[2:]
    else:
        n = binary(n)
    n = n[b:] + n[:b]
    return int(n, 2)

"""Divide the input into tokens of charachter"""
Input = input()
split_in = [char for char in Input]
print(split_in)

"""Get the ASCII of each token in an Array"""
ascii_in = [ord(split_in[i]) for i in range(len(split_in))]
print(ascii_in)

"""Now create an array of binary ASCII values from previous array"""
ascii_bin = [bin(ascii_in[i])[2:] for i in range(len(ascii_in))]
print(ascii_bin)

"""Add 0 in front of each binary no. till they are of 8 length each"""
for i in range(len(ascii_bin)):
    padding = '0'*(8-len(ascii_bin[i]))
    ascii_bin[i] = padding + ascii_bin[i]
print(ascii_bin)

"""join the binary Array and add 1 in front"""
str_ascii = ''.join(ascii_bin) + '1'
print(str_ascii)

"""Add 0 till the legth of binary ASCII string is 512 mod 448 doing like this is neccassry for big messages 
   for small you can simpy do this will length is mod 448"""
while(len(str_ascii) % 512 != 448):
    str_ascii += '0'
print(str_ascii, len(str_ascii))
"""Use the binary ASCII array of 8bits each and add the length of each array element convert that to 64 bit binary
   number and concatenate in the end of 448 bit ASCII string sp you can get 512 bit binay message denoting length of the
   message in the Least Significant 64 bit and message in remaining bits"""
length = 0
for i in ascii_bin:
    length += len(i)
length_bin = bin(length)[2:]
padding = '0' * (64-len(length_bin))
length_bin = padding + length_bin
print(length_bin)
str_ascii += length_bin
print(str_ascii, len(str_ascii))

"""Divide the message int0 chunks of 512 bits"""
import textwrap
item = ''
chunks = textwrap.wrap(str_ascii, 512)
print(chunks)

"""Divide each chunk into sixteen 32-bit word"""
chunkword = []
chunkword = [textwrap.wrap(i, 32) for i in chunks]
print(chunkword)

"""Perform operatios to get Eighty 32-bit words"""
for i in range(len(chunkword)):
    for j in range(16, 80):
        wordA = int(chunkword[i][j-3], 2)
        wordB = int(chunkword[i][j-8], 2)
        wordC = int(chunkword[i][j-14], 2)
        wordD = int(chunkword[i][j-16], 2)
        xorA = wordA ^ wordB
        xorB = xorA ^ wordC
        xorC = xorB ^ wordD
        xorC = bin(xorC)[2:]
        xorC = '0'*(32-len(xorC)) + xorC
        xorC = xorC[1:] + xorC[0]
        chunkword[i].append(xorC)
print(chunkword)

"""NOw loop throught each chunk to get  standard results"""
h0 = 0b01100111010001010010001100000001
h1 = 0b11101111110011011010101110001001
h2 = 0b10011000101110101101110011111110
h3 = 0b00010000001100100101010001110110
h4 = 0b11000011110100101110000111110000
a = h0
b = h1
c = h2
d = h3
e = h4
new_word = chunkword[0]
for i in range(80):
    if 0 <= i <= 19:
        f = d ^ (b & (c ^ d))
        k = 0b01011010100000100111100110011001
    elif 20 <= i <= 39:
        f = b ^ c ^ d
        k = 0b01101110110110011110101110100001
    elif 40 <= i <= 59:
        f = (b & c) | (b & d) | (c & d)
        k = 0b10001111000110111011110011011100
    elif 60 <= i <= 79:
        f = b ^ c ^ d
        k = 0b11001010011000101100000111010110
    word = new_word[i]
    word = int(word, 2)
    a, b, c, d, e = trunc((_left_rotate(a, 5) + f + e + k + word), 32), a, _left_rotate(b, 30), c, d


h0 = trunc((h0 + a), 32)
h1 = trunc((h1 + b), 32)
h2 = trunc((h2 + c), 32)
h3 = trunc((h3 + d), 32)
h4 = trunc((h4 + e), 32)

print(hex(h0)+hex(h1)[2:]+hex(h2)[2:]+hex(h3)[2:]+hex(h4)[2:])

import hashlib
result = hashlib.sha1(Input.encode())
print(result.hexdigest())