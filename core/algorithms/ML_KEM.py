from Crypto.Random import get_random_bytes

from core.subroutines.ML_KEM_Internal import ML_KEM_Internal
import core.constants as const


class ML_KEM:
    def __init__(self):
        self.ml_kem_internal = ML_KEM_Internal(const)
        self.encapsulation_key = None
        self.decapsulation_key = None
        self.cipher = None
        self.shared_secret = None

    def key_gen(self):
        """
        Generates an encapsulation key and a corresponding decapsulation key
        :return: Tuple of encapsulation_key, decapsulation_key
        """
        d = get_random_bytes(32)
        z = get_random_bytes(32)
        if d is None or z is None:
            return None
        self.encapsulation_key, self.decapsulation_key = self.ml_kem_internal.keygen(d, z)
        return self.encapsulation_key, self.decapsulation_key

    def encapsulation(self, encapsulation_key):
        """
        Uses the encapsulation key to generate a shared secret key and an associated ciphertext
        :param encapsulation_key: (Byte) a 384K+32 sized byte key
        :return: Tuple of Shared_secret_key and cipher_text
        """
        # TODO: Input Check for the encapsulation method
        self.encapsulation_key = encapsulation_key
        m = get_random_bytes(32)
        if m is None:
            return None
        self.shared_secret, self.cipher = self.ml_kem_internal.encapsulation(m, self.encapsulation_key)
        return self.shared_secret, self.cipher

    def decapsulation(self, decapsulation_key, cipher):
        """
        Uses the decapsulation key to produce a shared secret key from a ciphertext
        :param decapsulation_key: (Byte) a 786k+96 sized byte key
        :param cipher: (Byte) 32(duk) sized cipher text
        :return:
        """
        # TODO: Input check for decapsulation method
        self.decapsulation_key = decapsulation_key
        self.shared_secret = self.ml_kem_internal.decapsulation(cipher, self.decapsulation_key)
        return self.shared_secret
