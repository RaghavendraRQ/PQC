from core.subroutines.KPke import KPke
from core.utils.hash import sha3_256, sha3_512, shake256


class MLKEM_:
    def __init__(self, const):
        """
        Initializes a ml_kem_internal object never use it directly use MLKEM instead

        :param const: a constant file
        """
        self.const = const
        self.kpke = KPke(const)
        self.encapsulation_key = b''
        self.decapsulation_key = b''

    def keygen(self, d, z):
        """
        Generates a pair of keys for encapsulation and decapsulation

        Args:
            d: a 32 byte random seed
            z: a 32 byte random for randomness

        Returns:
            Tuple of encapsulation_key, decapsulation_key
        """

        self.encapsulation_key, self.decapsulation_key = self.kpke.keygen(d)
        self.decapsulation_key = b''.join([self.decapsulation_key, self.encapsulation_key, sha3_256(
            self.encapsulation_key), z])
        return self.encapsulation_key, self.decapsulation_key

    def encapsulation(self, m, encapsulation_key):
        """
        Generates a shared_secret key of length 32 and a cipher

        Args:
            m:  32 byte random seed
            encapsulation_key: encapsulation_key of length 384k+32

        Returns:
            Tuple: Shared secret key, cipher
        """

        self.encapsulation_key = encapsulation_key
        shared_secret_key, r = sha3_512(m + sha3_256(self.encapsulation_key))
        cipher = self.kpke.encrypt(m, r, self.encapsulation_key)
        return shared_secret_key, cipher

    def decapsulation(self, c, decapsulation_key):
        """
        Reconstructs the shared_secret_key using cipher and decapsulation_key

        Args:
            c: 32(duk) sized cipher
            decapsulation_key: 786k+96 sized decryption_key

        Returns:
            bytes: shared_secret_key using kpke
        """

        self.decapsulation_key = decapsulation_key
        decryption_key = self.decapsulation_key[0: 384 * self.const.K]
        encryption_key = self.decapsulation_key[384 * self.const.K:768 * self.const.K + 32]
        h = self.decapsulation_key[768 * self.const.K + 32: 768 * self.const.K + 64]
        z = self.decapsulation_key[768 * self.const.K + 64:768 * self.const.K + 96]
        m = self.kpke.decrypt(c, decryption_key)
        shared_secret_key, r = sha3_512(b''.join([m, h]))
        shared_secret_key_check = shake256(b''.join([z, m]))
        c_check = self.kpke.encrypt(m, r, encryption_key)
        if c != c_check:
            shared_secret_key = shared_secret_key_check
        return shared_secret_key
