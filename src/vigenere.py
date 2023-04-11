class VigenereCrypter(object):
    def __init__(self, key='DUBVAS'):
        self.keyword = key

    def encrypt_message(self, msg):
        result = list()
        for i in msg:
            result.append((i + ord(self.keyword[i % len(self.keyword)])) % 256)
        return b''.join(list(map(lambda x: x.to_bytes(1, 'big'), result)))

    def decrypt_message(self, msg):
        result = list()
        for i in msg:
            result.append((i - ord(self.keyword[i % len(self.keyword)])) % 256)
        return b''.join(list(map(lambda x: x.to_bytes(1, 'big'), result)))
