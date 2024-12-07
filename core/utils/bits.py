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
