from core.utils.ntt import NTT
from core.utils.shake import sha3_512
from Crypto.Random import get_random_bytes

import core.constants as const


class KPke:
    def __init__(self, seed, ntt):
        """
        Initializes a KPke object with a random seed
        :param seed: a 32 byte seed
        :param k: a constant value for the algorithm
        """
        self.seed = seed
        self.k = const.k
        self.encryption_key = ""
        self.decryption_key = ""
        self.ntt = ntt
        self.A = [[0] * self.k] * self.k
        self.e = [0] * self.k
        self.s = [0] * self.k

    def keygen(self):
        d = get_random_bytes(32)
        ro, sigma = sha3_512(d + self.k.to_bytes())
        n = 0
        for i in range(self.k):
            for j in range(self.k):
                self.A[i][j] = self.ntt.get_sample_ntt(ro + j.to_bytes() + i.to_bytes())
        for i in range(self.k):
            self.s[i] = self.ntt.get_sample_polyCBD(sigma)
        for j in range(self.k):
            self.e[j] = self.ntt.get_sample_polyCBD(sigma)



    def get_encryption_key(self):
        return self.encryption_key

    def get_decryption_key(self):
        return self.decryption_key
