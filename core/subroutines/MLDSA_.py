from Crypto.Hash import SHAKE256

from core.utils.bits import int_to_bytes
from core.utils.dsa.sampling import Sample
# from core.utils.overflow.stubborn import ConstantMeta


class MLDSA_:

    def __init__(self, const):
        self.const = const
        self.sample = Sample(const)

    def keygen(self, seed):
        """
        Generates a public private key pair from seed
        Args:
            seed: A Random 32 byte seed

        Returns:
            Tuple: Public key, Private key
        """
        assert len(seed) == 32, "lengthgth of the seed should be 32 bytes."

        shake_256 = SHAKE256.new()
        shake_256.update(seed + int_to_bytes(self.const.K, 1) + int_to_bytes(self.const.K, 1))
        hashed = shake_256.read(128)
        seed_A, seed_S, k = hashed[:32], hashed[32:96], hashed[96:]
        A = self.sample.expand_A(seed_A)
        s1, s2 = self.sample.expand_S(seed_S)

