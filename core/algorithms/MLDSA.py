from importlib import import_module
from Crypto.Random import get_random_bytes

from core.subroutines.MLDSA_ import MLDSA_
from core.utils.bits import bytes_to_bits, int_to_bytes


class MLDSA:

    MLDSA44 = 'dsa44'
    MLDSA65 = 'dsa65'
    MLDSA87 = 'dsa87'

    def __init__(self, params_set=MLDSA44):
        self.config = import_module(f'core.constants.{params_set}')
        self._mldsa = MLDSA_(self.config)

    def keygen(self):
        seed = get_random_bytes(32)
        if seed is None:
            return None
        return self._mldsa.keygen(seed)

    def sign(self, private_key, message, ctx):
        assert len(private_key) == 128 + 32*((self.config.D * self.config.K) + (self.config.K + self.config.L) * (2*self.config.ETA).bit_length()), f'Length of private key should be 896 bytes. Not {len(private_key)}'

        if len(ctx) >= 256:
            return None
        randomness = get_random_bytes(32)
        if randomness is None:
            return None

        encoded_message = bytes_to_bits(int_to_bytes(0, 1) + int_to_bytes(len(ctx), 1) + ctx) + message
        return self._mldsa.sign(private_key, encoded_message, randomness)

    def verify(self, public_key, message, signature, ctx):
        if len(signature) >= 256:
            return False
        encoded_message = bytes_to_bits(int_to_bytes(0, 1) + int_to_bytes(len(ctx), 1) + ctx) + message
        return self._mldsa.verify(public_key, encoded_message, signature)
