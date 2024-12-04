from core.utils.bits import byte_encode, byte_decode, compress, decompress
from core.utils.ntt import NTT
from core.utils.shake import sha3_512, prf
from Crypto.Random import get_random_bytes
import core.constants as const


class KPke:
    def __init__(self, seed, ntt):
        """
        Initializes a KPke object with a random seed
        :param seed: a 32 byte seed
        :param k: a constant value for the algorithm
        """
        assert len(seed) == 32, "Seed must be 32 bytes"
        self.seed = seed
        self.k = const.k
        self.ntt = ntt
        self.encryption_key = None
        self.decryption_key = None
        self.A = [[[0] * const.N] * self.k] * self.k
        self.s_cap = [[0] * self.k] * self.k
        self.e_cap = [[0] * self.k] * self.k
        self.e = [0] * self.k
        self.s = [0] * self.k

    def keygen(self):
        if self.encryption_key is not None and self.decryption_key is not None:
            return self.encryption_key, self.decryption_key
        d = get_random_bytes(32)
        ro, sigma = sha3_512(d + self.k.to_bytes())
        n = 0
        for i in range(self.k):
            for j in range(self.k):
                self.A[i][j] = self.ntt.get_sample_ntt(ro + j.to_bytes() + i.to_bytes())
        for i in range(self.k):
            self.s[i] = self.ntt.get_sample_polyCBD(prf(sigma, n.to_bytes()))
            n += 1
        for j in range(self.k):
            self.e[j] = self.ntt.get_sample_polyCBD(prf(sigma, n.to_bytes()))
            n += 1
        self.s_cap = [self.ntt.ntt(self.s[i]) for i in range(self.k)]
        self.e_cap = [self.ntt.ntt(self.e[i]) for i in range(self.k)]
        t_cap = self._add_vectors(self._multiply_array_vector(self.A, self.s_cap), self.e_cap)
        self.encryption_key = b''.join([byte_encode(t_cap[i], const.D) for i in range(self.k)]) + ro
        self.decryption_key = b''.join([byte_encode(self.s[i], const.D) for i in range(self.k)])
        return self.encryption_key, self.decryption_key

    def encrypt(self, message, randomness):
        n = 0
        t_cap = [byte_decode(self.encryption_key[i * 384: (i + 1) * 384], const.D) for i in range(self.k)]
        y = [[0] * self.k] * self.k
        e1 = [[0] * self.k] * self.k
        for i in range(self.k):
            y[i] = self.ntt.get_sample_polyCBD(prf(randomness, n.to_bytes()))
            n += 1
        for j in range(self.k):
            e1[j] = self.ntt.get_sample_polyCBD(prf(randomness, n.to_bytes(), const.ETA_2), const.ETA_2)
            n += 1
        e2 = self.ntt.get_sample_polyCBD(prf(randomness, n.to_bytes(), const.ETA_2), const.ETA_2)
        y_cap = [self.ntt.ntt(y[i]) for i in range(self.k)]
        a_transpose = self._transpose(self.A)
        u = self._multiply_array_vector_modified(a_transpose, y_cap)
        u = [self.ntt.ntt_inverse(u[i]) for i in range(self.k)]
        u = [self._add_vectors(u[i], e1[i]) for i in range(self.k)]
        mu = decompress(byte_decode(message, 1), 1)
        print(f'mu: {mu}')
        t_transpose = self._transpose(t_cap)
        print(f't_transpose: {t_transpose}')



    def _multiply_vectors(self, vec1, vec2):
        """
        Multiplies two vectors
        :param vec1:
        :param vec2:
        :return:
        """
        return [x * y for x, y in zip(vec1, vec2)]

    def _transpose(self, matrix):
        """
        Transposes a matrix
        :param matrix:
        :return:
        """
        return [list(row) for row in zip(*matrix)]

    def _multiply_array_vector(self, array, vector):
        """
        Computes the multiplication of 2d array and list
        :param array:
        :param vector:
        :return:
        """
        result = [[0] * len(array)] * len(array)
        for i in range(len(array)):
            for j in range(len(array)):
                result[i][j] = sum(self._multiply_vectors(array[i][j], vector[j])) % const.Q
        return result

    def _multiply_array_vector_modified(self, array, vector):
        result = [[0] * const.N] * self.k
        for i in range(len(array)):
            for j in range(len(array[0])):
                result[i] = self.ntt.multiply_ntt(array[i][j], vector[j])

        return result

    def _add_vectors(self, vec1, vec2):
        """
        Adds two vectors
        :param vec1:
        :param vec2:
        :return:
        """
        return [x + y for x, y in zip(vec1, vec2)]


ntt = NTT()
kpke = KPke(get_random_bytes(32), ntt)
enc_key, dec_key = kpke.keygen()

# print(f'Encryption key: {enc_key}')
# print(f'Decryption key: {dec_key}')
# print(f'len(enc_key): {len(enc_key)}')
# print(f'len(dec_key): {len(dec_key)}')
kpke.encrypt(get_random_bytes(32), get_random_bytes(32))
