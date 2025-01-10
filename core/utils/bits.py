import core.constants_ as const
from numpy import array, floor


def bits_to_bytes(bit_array):
    """
    Converts a bit array of length (multiple of 8) into a byte array.

    Args:
        bit_array: List of bits (0 or 1) with length 8 * l.

    Returns:
        Byte array of length l.
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

    Args:
        byte_array: Byte array of length l

    Returns:
        Bit array of length 8 * l.

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

    Args:
        f: Array of integers.
        d: Bit-length of the integers (1 <= d <= 12).

    Returns:
        Encoded byte array.
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

    Args:
        byte_array: Byte array of length 32 * d.
        d: Bit-length of the integers (1 <= d <= 12).

    Returns:
        Array of integers F.
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

    Args:
        x: Array of integers in Z_q.
        d: The bit length of the compressed range.
        q: The modulus, default is 3329.

    Returns:
         Array of compressed values in Z_{2^d}.
    """
    x = array(x)
    scale = (2 ** d) / q
    return floor(scale * x + 0.5).astype(int) % (2 ** d)


def decompress(y, d, q=3329):
    """
    Decompress function for arrays.
    Decompress_d : Z_{2^d} -> Z_q
    y -> floor((q / 2^d) * y + 0.5)

    Args:
        y:  Array of compressed values in Z_{2^d}.
        d: The bit length of the compressed range.
        q: The modulus, default is 3329.

    Returns:
        Array of decompressed values in Z_q.
    """
    y = array(y)
    scale = q / (2 ** d)
    return floor(scale * y + 0.5).astype(int)


def int_to_bits(integer, length):
    """
    Computes a base-2 representation of integer mod 2^length using little-endian order.

    Args:
        integer: A Non-Negative integer
        length: A Positive integer

    Returns:
        str: A bit string y of given length
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

    Args:
        bit_string: bit_string to be converted
        length: length of the bit_string

    Returns:
        int: integer representing the bit array
    """
    assert len(bit_string) == length >= 0, "Length should be positive and equals to the bit_string."

    integer = 0
    for i in range(1, length + 1):
        integer = 2 * integer + int(bit_string[length - i])

    return integer


def int_to_bytes(integer, length):
    """
    Computes a base-256 representation of integer mod 256^length using little-endian order

    Args:
        integer:  A Non-Negative integer
        length: A Positive integer

    Returns:
        A byte string of given length
    """
    assert integer >= 0 and length >= 0, "Integer and  length must be positive."

    integer_ = integer
    y = []
    for _ in range(length):
        y.append(integer_ % 256)
        integer_ //= 2

    return bytes(y)

def bytes_to_int(byte_string, length):
    """
    Computes the integer value expressed by a byte string using little-endian order

    Args:
        byte_string: byte_string to be converted

    Returns:
        int: integer representing the byte array
    """
    integer = 0
    for i in range(length):
        integer = 256 * integer + int.from_bytes(byte_string[i:i+1])

    return integer

def truncate(byte_string, length):
    """
    Truncates a byte string to a given length

    Args:
        byte_string: byte_string to be truncated
        length: length of the truncated byte_string

    Returns:
        bytes: truncated byte string
    """
    return byte_string[length:]


def coeff_from_three_bytes(b0, b1, b2, q=8380417):
    """
    Generates an element of {0 - q-1} or None

    Args:
        b0: byte b0
        b1: byte b1
        b2: another byte b2
        q: modulus

    Returns:
        int: An integer % q or none
    """

    b2_ = int.from_bytes(b2)
    b1_ = int.from_bytes(b1)
    b0_ = int.from_bytes(b0)
    # Setting the top bit of b2 to zero
    if b2_ > 127:
        b2_ -= 128

    # z = 2^16.b2 + 2^8.b1 + b0
    integer = 65536 * b2_ + 256 * b1_ + b0_
    return integer if integer < q else None  # Reject Sampling


def coeff_from_half_byte(b, ETA):
    """
    Let eta ∈ {2, 4}. Generates an element of {−eta, −eta + 1, ... , eta} or None

    Args:
        b: int b/w 0 - 15
        ETA: Constant for the algorithm

    Returns:
        int: An integer b/w -eta to eta or None
    """
    assert 0 <= b <= 15, "integer b should in range(0,16)."

    if ETA == 2 and b < 15:     # rejection sampling from -2,...,2
        return 2 - (b % 5)
    elif ETA == 4 and b < 9:    # rejection sampling from -4,...,4
        return 4 - b

    return None
