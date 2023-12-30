import rsa


class EncryptionHandler:
    @staticmethod
    def gen():
        return rsa.newkeys(1024)

    @staticmethod
    def encrypt(data: bytes, pubkey: rsa.PublicKey):
        return rsa.encrypt(data, pubkey)

    @staticmethod
    def decrypt(data: bytes, privatekey: rsa.PrivateKey):
        return rsa.decrypt(data, privatekey)

    @staticmethod
    def save_keys(pubkey: rsa.PublicKey, privkey: rsa.PrivateKey):
        with open("public.pem", "wb") as f:
            f.write(pubkey.save_pkcs1())
        with open("private.pem", "wb") as f:
            f.write(privkey.save_pkcs1())
