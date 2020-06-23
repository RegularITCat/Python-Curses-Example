def atbash_encode(plaintext):
    atbash_table = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "ZYXWVUTSRQPONMLKJIHGFEDCBA"))
    ciphertext = [atbash_table[i] if i.isalpha() else i for i in plaintext.upper()]
    return ("".join(ciphertext))


def atbash_decode(ciphertext):
    return atbash_encode(ciphertext)


def caesar_encode(plaintext, key):
    L2I = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", range(26)))
    I2L = dict(zip(range(26), "ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
    return "".join([I2L[(L2I[i] + key) % 26] if i.isalpha() else i for i in plaintext.upper()])


def caesar_decode(ciphertext, key):
    L2I = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", range(26)))
    I2L = dict(zip(range(26), "ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
    return "".join([I2L[(L2I[i] - key) % 26] if i.isalpha() else i for i in ciphertext.upper()])


def gronsfeld_encode(plaintext, key):
    key = str(key)
    key *= len(plaintext) // len(key) + 1
    return "".join([caesar_encode(e, int(key[k])) if e.isalpha() else e for k, e in enumerate(plaintext)])


def gronsfeld_decode(ciphertext, key):
    key = str(key)
    key *= len(ciphertext) // len(key) + 1
    return "".join([caesar_decode(e, int(key[k])) if e.isalpha() else e for k, e in enumerate(ciphertext)])


def polibius_encode(plaintext):
    polibius_square = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"  # 6x6
    return "".join([polibius_square[(polibius_square.find(e) + 6) % 36] if polibius_square.find(e) != -1 else e for e in
                    plaintext.upper()])


def polibius_decode(ciphertext):
    polibius_square = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(
        [polibius_square[(polibius_square.find(e) + 30) % 36] if polibius_square.find(e) != -1 else e for e in
         ciphertext.upper()])


def xor_encode(plaintext, key):
    plaintext = str(plaintext)
    key = str(key)
    return "".join([chr(ord(plaintext[i]) ^ ord(key[i % len(key)])) for i in range(len(plaintext))])


def xor_decode(ciphertext, key):
    return xor_encode(ciphertext, key)
