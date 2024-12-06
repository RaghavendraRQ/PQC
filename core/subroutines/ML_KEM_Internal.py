from core.subroutines.KPke import KPke
from core.utils.ntt import NTT
from core.utils.shake import sha3_256, sha3_512, shake256
import  core.constants as const
from Crypto.Random import get_random_bytes


class ML_KEM_Internal:
    def __init__(self, d, z, kpke: KPke = None, ntt: NTT = None):
        self.d = d
        self.z = z
        self.kpke = kpke or KPke(d, ntt or NTT())
        self.encapsulation_key = b''
        self.decapsulation_key = b''

    def keygen(self, d=None, z=None):
        self.d = d or self.d
        self.z = z or self.z
        self.encapsulation_key, self.decapsulation_key = self.kpke.keygen()
        self.decapsulation_key = b''.join([self.decapsulation_key, self.encapsulation_key, sha3_256(self.encapsulation_key), self.z])
        return self.encapsulation_key, self.decapsulation_key

    def encapsulation(self, m: bytes):
        shared_secret_key, r = sha3_512(m + sha3_256(self.encapsulation_key))
        print(f'shared secret key: {shared_secret_key}')
        print(f'r: {r}')
        cipher = self.kpke.encrypt(m, r)
        return shared_secret_key, cipher

    def decapsulation(self, c):
        decryption_key = self.decapsulation_key[0: 384 * const.K]
        encryption_key = self.decapsulation_key[384 * const.K:768 * const.K + 32]
        h = self.decapsulation_key[768 * const.K + 32: 768 * const.K + 64]
        z = self.decapsulation_key[768 * const.K + 64:768 * const.K + 96]
        m = self.kpke.decrypt(c)
        shared_secret_key, r = sha3_512(b''.join([m, h]))
        shared_secret_key_check = shake256(b''.join([z, m]))
        c_check = self.kpke.encrypt(m, r)
        if c != c_check:
            shared_secret_key = shared_secret_key_check
        return shared_secret_key


ml_kem = ML_KEM_Internal(get_random_bytes(32), get_random_bytes(32))
print(ml_kem.keygen()[0])
