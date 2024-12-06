from core.subroutines.ML_KEM_Internal import ML_KEM_Internal

from Crypto.Random import get_random_bytes


class ML_KEM:
    def __init__(self, ml_kem_internal: ML_KEM_Internal = None):
        self.ml_kem_internal = ml_kem_internal
        self.encapsulation_key = None
        self.decapsulation_key = None
        self.cipher = None
        self.shared_secret = None

    def key_gen(self):
        d = get_random_bytes(32)
        z = get_random_bytes(32)
        if d is None or z is None:
            return None
        self.ml_kem_internal = ML_KEM_Internal(d, z)
        self.encapsulation_key, self.decapsulation_key = self.ml_kem_internal.keygen(d, z)
        return self.encapsulation_key, self.decapsulation_key

    def encapsulation(self, encapsulation_key):
        # TODO: Input Check for the encapsulation method
        m = get_random_bytes(32)
        if m is None:
            return None
        self.shared_secret, self.cipher = self.ml_kem_internal.encapsulation(m)
        return self.cipher, self.shared_secret

    def decapsulation(self, decapsulation_key, c):
        # TODO: Input check for decapsulation method
        self.shared_secret = self.ml_kem_internal.decapsulation(c)
        return self.shared_secret


mlkem = ML_KEM()
e, d = mlkem.key_gen()
print(f'e: {e}')
print(f'd: {d}')
s, c = mlkem.encapsulation(e)
# s_ = mlkem.decapsulation(d, c)
print(f's: {s}')
print(f'c: {len(c)}')
# print(f's_: {s_}')
