import cv2
import numpy as np


def bitfield(n):
    return [int(digit) for digit in bin(n)[2:]]


def gerar_mensagem(mensagem):
    lista = []
    for m in mensagem:
        val = ord(m)
        bits = bitfield(val)

        if len(bits) < 8:
            for a in range(8 - len(bits)):
                bits.insert(0, 0)
        lista.append(bits)
    arr = np.array(lista)
    arr = arr.flatten()
    return arr


def converter_mensagem(saida):
    bits = np.array(saida)
    mensagem_out = ''
    bits = bits.reshape((int(len(saida) / 8), 8))
    for b in bits:
        sum = 0
        for i in range(8):
            sum += b[i] * (2 ** (7 - i))
        mensagem_out += chr(sum)
    return mensagem_out


texto = "A"
arrayBits = gerar_mensagem(texto)
print(texto)
print(arrayBits)
textoTraduzido = converter_mensagem(arrayBits)
print(textoTraduzido)
