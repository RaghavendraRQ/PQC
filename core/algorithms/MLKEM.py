from Crypto.Random import get_random_bytes
from importlib import import_module

from core.subroutines.ML_KEM_Internal import ML_KEM_Internal


class MLKEM:
    MLKEM512 = 'kem512'
    MLKEM768 = 'kem768'
    MLKEM1024 = 'kem1024'

    def __init__(self, params_set=MLKEM512):
        self.config = import_module(f'core.constants.{params_set}')
        self._ml_kem_internal = ML_KEM_Internal(self.config)
        self.encapsulation_key = b''
        self.decapsulation_key = b''
        self.cipher = b''
        self.shared_secret = b''

    def key_gen(self):
        """
        Generates an encapsulation key and a corresponding decapsulation key

        :return: Tuple of encapsulation_key, decapsulation_key
        """
        d = get_random_bytes(32)
        z = get_random_bytes(32)
        if d is None or z is None:
            return None
        self.encapsulation_key, self.decapsulation_key = self._ml_kem_internal.keygen(d, z)
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
        self.shared_secret, self.cipher = self._ml_kem_internal.encapsulation(m, self.encapsulation_key)
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
        self.shared_secret = self._ml_kem_internal.decapsulation(cipher, self.decapsulation_key)
        return self.shared_secret
