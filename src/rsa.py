class RSACrypter(object):
    __size = 64

    def __init__(self, key):
        self.exponent, self.modulo = key.split(',')

    def _mod_pow_(self, a, b):
        if b == 0:
            return a % self.modulo
        result = self._mod_pow_(a, b // 2)
        result *= result
        result %= self.modulo
        if b % 2 == 1:
            result = (result * a) % self.modulo
        return result

    def encrypt_message(self, msg):
        result = list()
        block_size = RSACrypter.__size - 1
        for i in range(0, len(msg), block_size):
            _bytes = b''.join(list(map(lambda x: x.to_bytes(1, 'little'), msg[i:min(i + block_size, len(msg))])))
            elem = int.from_bytes(_bytes, 'little')
            result.append(self._mod_pow_(elem, self.exponent))
        return b''.join(list(map(lambda x: x.to_bytes(RSACrypter.__size, 'little'), result)))

    def decrypt_message(self, msg):
        result = list()
        for i in range(0, len(msg), RSACrypter.__size):
            _bytes = b''.join(list(map(lambda x: x.to_bytes(1, 'little'), msg[i:min(i + RSACrypter.__size, len(msg))])))
            elem = int.from_bytes(_bytes, 'little')
            result.append(self._mod_pow_(elem, self.exponent))
        return b''.join(list(map(lambda x: x.to_bytes(RSACrypter.__size - 1, 'little'), result)))
