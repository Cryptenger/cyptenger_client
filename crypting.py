# coding=utf-8
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

import uuid
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util.Padding import pad, unpad
import random

class Crypting():
    def __init__(self):
        self.server_pass = ""

        # BLOCK_SIZE = 16
        # self.pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
        # self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]

        self.paddingOAEP = padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )

        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
            backend=default_backend()
        )
        # Generating public key from the private one
        self.public_key = self.private_key.public_key()


        # Do know exactely but certainly generating public key text
        self.public_key_readable = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def asymEncrypt(self, public_key_readable, message): # Fonction pour chiffrer les messages asymétriques
        client_pub_key = serialization.load_pem_public_key(public_key_readable, backend=default_backend()) # TODO : Comprendre cette fonction et l'expliquer :kappa:

        return client_pub_key.encrypt(message.encode(), self.paddingOAEP)

    def asymDecrypt(self, message): # Fonction pour déchiffrer les messages asymétriques
        return self.private_key.decrypt(message, self.paddingOAEP).decode()


    # Partie Symmétrique
    def saveServerPass(self, password):
        self.server_pass = password

    def genServerPass(self):
        self.server_pass = hashlib.sha512(str(uuid.uuid4()).encode()).hexdigest()

    def sym_encrypt(self, raw):
        private_key = hashlib.sha256(self.server_pass.encode("utf-8")).digest()
        raw = pad(raw.encode('utf-8'), AES.block_size)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(private_key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw)).decode('utf8')

    def sym_decrypt(self, encrypted_text):
        private_key = hashlib.sha256(self.server_pass.encode("utf-8")).digest()
        encrypted_text = base64.b64decode(encrypted_text)
        iv = encrypted_text[:16]
        cipher = AES.new(private_key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(encrypted_text[16:]), AES.block_size).decode('utf8')
