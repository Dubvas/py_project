class CeasarCrypter(object):
    def __init__(self, key='7'):
        self.shift = int(key)

    def encrypt_message(self, msg):
        result = list()
        for i in msg:
            result.append((i + self.shift) % 256)
        return b''.join(list(map(lambda x: x.to_bytes(1, 'big'), result)))

    def decrypt_message(self, msg):
        result = list()
        for i in msg:
            result.append((i - self.shift) % 256)
        return b''.join(list(map(lambda x: x.to_bytes(1, 'big'), result)))
