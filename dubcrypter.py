import src.globals as globals
import sys
from collections import defaultdict
from src.ceasar import CeasarCrypter
from src.vigenere import VigenereCrypter
from src.vernam import VernamCrypter
from src.rsa import RSACrypter


globals.crypters["ceasar"] = CeasarCrypter
globals.crypters["vigenere"] = VigenereCrypter
globals.crypters["vernam"] = VernamCrypter
globals.crypters["rsa"] = RSACrypter


class InvalidArgument(Exception):
    pass


def process_file(in_filename: str, out_filename: str, func):
    '''Applies given function do data in in_file, saves result out_file'''
    with open(in_filename, 'rb') as inp:
        with open(out_filename, 'wb') as out:
            s = inp.read()
            s = func(s)
            out.write(s)


def encrypt_file(crypter, filename: str):
    '''Encrypts file with given crypter'''
    process_file(filename, filename + globals.extension, crypter.encrypt_message)


def decrypt_file(crypter, filename: str):
    '''Decrypts file with crypter, raises error if file exception is not globals.extension'''
    if not filename.endswith(globals.extension):
        raise InvalidArgument from Exception
    process_file(filename, filename[:-len(globals.extension)], crypter.decrypt_message)


def rate_message(msg):
    '''Rates how well text matches english letter distribution'''
    cnt = defaultdict(int)
    latin_cnt = 0
    for cr in msg:
        cnt[cr] += 1
        latin_cnt += 1 if ord('a') <= cr <= ord('z') else 0

    result = 0.0
    for pr in globals.letter_distribution.items():
        letter = ord(pr[0])
        rate = pr[1]
        result += ((cnt[letter] / latin_cnt * 100.0) - rate) ** 2

    return result


if __name__ == "__main__":
    args = dict()
    args["mode"] = sys.argv[1].lower()
    ptr = 2
    if args["mode"] != 'crack':
        args["crypter"] = sys.argv[2].lower()
        args["key"] = sys.argv[3]
        ptr = 4
        if args["key"] == "--filename":
            ptr = 5
            with open(sys.argv[4], 'r') as key_inp:
                args["key"] = key_inp.read()

    if args["mode"] != 'crack':
        crypter = globals.crypters[args["crypter"]](args["key"])

    if args["mode"].startswith('enc'):
        for i in range(ptr, len(sys.argv)):
            encrypt_file(crypter, sys.argv[i])

    if args["mode"].startswith('dec'):
        for i in range(ptr, len(sys.argv)):
            decrypt_file(crypter, sys.argv[i])

    if args["mode"] == 'crack':
        for i in range(ptr, len(sys.argv)):
            with open(sys.argv[i], 'rb') as inp:
                msg = inp.read()

            crypter = CeasarCrypter(0)
            current_rating = rate_message(msg)
            for shift in range(1, 26):
                new_crypter = CeasarCrypter(shift)
                msg_variant = new_crypter.decrypt_message(msg)
                msg_variant = list(msg_variant.lower())
                new_rating = rate_message(msg_variant)
                if new_rating < current_rating:
                    current_rating = new_rating
                    crypter = new_crypter

            decrypt_file(crypter, sys.argv[i])
            print(f'#{i- ptr + 1} file had shift of', crypter.shift)
