import core.constants_ as const
from numpy import array, floor


def bits_to_bytes(bit_array):
    """
    Converts a bit array of length (multiple of 8) into a byte array.

    :param bit_array: List of bits (0 or 1) with length 8 * l.

    :returns: Byte array of length l.
    """
    if len(bit_array) % 8 != 0:
        raise ValueError("Bit array length must be a multiple of 8.")

    byte_array = bytearray(len(bit_array) // 8)

    for i in range(len(bit_array)):
        byte_index = i // 8
        bit_position = i % 8
        byte_array[byte_index] += bit_array[i] * (1 << bit_position)

    return bytes(byte_array)


def bytes_to_bits(byte_array):
    """
    Converts a byte array into a bit array.

    :param byte_array: Byte array of length l.

    :returns: Bit array of length 8 * l.
    """
    bit_array = []

    for byte in byte_array:
        for _ in range(8):
            bit_array.append(byte % 2)
            byte //= 2

    return bit_array


def byte_encode(f, d):
    """
    Encodes an array of d-bit integers into a byte array.

    :param f: Array of integers.
    :param d: Bit-length of the integers (1 <= d <= 12).

    :returns: Encoded byte array.
    """
    if not (1 <= d <= 12):
        raise ValueError("d must be between 1 and 12.")

    assert len(f) == 256, f"Int array must be of length {256}. Not {len(f)} "

    b = [0] * (256 * d)
    for i in range(256):
        a = f[i]
        for j in range(d):
            b[i * d + j] = a % 2
            a = (a - b[i * d + j]) // 2
    byte_array = bits_to_bytes(b)
    return byte_array


def byte_decode(byte_array, d):
    """
    Decodes a byte array into an array of d-bit integers.

    :param byte_array: Byte array of length 32 * d.
    :param d: Bit-length of the integers (1 <= d <= 12).

    :returns: Array of integers F.
    """
    if not (1 <= d <= 12):
        raise ValueError("d must be between 1 and 12.")

    assert len(byte_array) == 32 * d, f"The byte array must be of length {32 * d}. Not {len(byte_array)}."

    bit_array = bytes_to_bits(byte_array)

    f = [0] * 256

    for i in range(256):
        for j in range(d):
            f[i] += bit_array[i * d + j] * (2 ** j)
        m = (2 ** d) if d < 12 else const.Q
        f[i] %= m

    return f


def compress(x, d, q=3329):
    """
    Compress function for arrays.
    Compress_d : Z_q -> Z_{2^d}
    x -> floor((2^d / q) * x + 0.5) mod 2^d

    :param x: Array of integers in Z_q.
    :param d : The bit length of the compressed range.
    :param q : The modulus, default is 3329.

    :returns: Array of compressed values in Z_{2^d}.
    """
    x = array(x)
    scale = (2 ** d) / q
    return floor(scale * x + 0.5).astype(int) % (2 ** d)


def decompress(y, d, q=3329):
    """
    Decompress function for arrays.
    Decompress_d : Z_{2^d} -> Z_q
    y -> floor((q / 2^d) * y + 0.5)

    :param y: Array of compressed values in Z_{2^d}.
    :param d: The bit length of the compressed range.
    :param q: The modulus, default is 3329.

    :returns: Array of decompressed values in Z_q.
    """
    y = array(y)
    scale = q / (2 ** d)
    return floor(scale * y + 0.5).astype(int)


def int_to_bits(integer, length):
    """
    Computes a base-2 representation of integer mod 2^length using little-endian order.

    :param integer: A Non-Negative integer
    :param length: A Positive integer

    :return: bit string of given length
    """

    assert integer >= 0 and length >= 0, "Integer and  length must be positive."

    integer_ = integer
    bit_string = ''
    for i in range(length):
        bit_string += str(integer_ % 2)
        integer_ //= 2

    return bit_string


def bits_to_int(bit_string, length):
    """
    Computes the integer value expressed by a bit string using little-endian order

    :param bit_string: bit_string to be converted
    :param length: length of the bit_string

    :return: Non-Negative integer
    """

    assert len(bit_string) == length >= 0, "Length should be positive and equals to the bit_string."

    integer = 0
    for i in range(1, length + 1):
        integer = 2 * integer + int(bit_string[length - i])

    return integer


def int_to_bytes(integer, length):
    """
    Computes a base-256 representation of integer mod 256^length using little-endian order

    :param integer: A Non-Negative integer
    :param length: A Positive integer

    :return: A byte string of given length
    """

    assert integer >= 0 and length >= 0, "Integer and  length must be positive."

    integer_ = integer
    y = []
    for i in range(length):
        y.append(integer_ % 256)
        integer_ //= 2

    return bytes(y)


def coeff_from_three_bytes(b0, b1, b2, q=8380417):
    """
    Generates an element of {0 - q-1} or None

    :param q: modulus
    :param b0: byte b0
    :param b1: byte b1
    :param b2: another byte b2

    :return: an integer % q or none
    """

    b2_ = int.from_bytes(b2)
    b1_ = int.from_bytes(b1)
    b0_ = int.from_bytes(b0)
    if b2_ > 127:
        b2_ = b2_ - 128
    integer = (2 ** 16) * b2_ + (2 ** 8) * b1_ + b0_
    return integer if integer < q else None


def coeff_from_half_byte(b, ETA):
    """
    Let eta ∈ {2, 4}. Generates an element of {−eta, −eta + 1, ... , eta} or None

    :param ETA: Constant for the algorithm
    :param b: int b/w 0 - 15

    :return: int b/w -eta to eta or None
    """

    assert 0 <= b <= 15, "integer b should in range(0,16)."

    if ETA == 2 and b < 15:
        return 2 - b % 5
    elif ETA == 4 and b < 9:
        return 4 - b

    return None

