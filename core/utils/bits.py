import core.constants as const


def bits_to_bytes(bit_array):
    """
    Converts a bit array of length (multiple of 8) into a byte array.
    :param bit_array: List of bits (0 or 1) with length 8 * ℓ.
    :return: Byte array of length ℓ.
    """
    # Ensure the bit array length is a multiple of 8
    if len(bit_array) % 8 != 0:
        raise ValueError("Bit array length must be a multiple of 8.")

    byte_array = bytearray(len(bit_array) // 8)

    # Convert bits to bytes
    for i in range(len(bit_array)):
        byte_index = i // 8
        bit_position = i % 8
        byte_array[byte_index] += bit_array[i] * (1 << bit_position)

    return bytes(byte_array)


def bytes_to_bits(byte_array):
    """
    Converts a byte array into a bit array.
    :param byte_array: Byte array of length ℓ.
    :return: Bit array of length 8 * ℓ.
    """
    bit_array = []

    # Iterate through each byte in the byte array
    for byte in byte_array:
        for _ in range(8):
            # Extract the least significant bit (LSB)
            bit_array.append(byte % 2)
            # Shift the byte to the right (divide by 2)
            byte //= 2

    return bit_array


def byte_encode(f, d):
    """
    Encodes an array of d-bit integers into a byte array.
    :param f: Array of integers in Z256.
    :param d: Bit-length of the integers (1 <= d <= 12).
    :return: Encoded byte array.
    """
    # Validate d
    if not (1 <= d <= 12):
        raise ValueError("d must be between 1 and 12.")
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
    :return: Array of integers F.
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


def compress(vector, d):
    return [round((2 ** d / const.Q) * x) % (2 ** d) for x in vector]


def decompress(vector, d):
    return [round((const.Q / (2 ** d)) * x) % const.Q for x in vector]

