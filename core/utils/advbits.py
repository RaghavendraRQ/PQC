from core.utils.bits import int_to_bits, bits_to_bytes, bytes_to_bits, bits_to_int


def simple_bit_pack(polynomial, end):
    """
    Encodes a polynomial into a byte string

    :param polynomial: A list of coefficients in range [0,end]
    :param end: A Natural Number

    :return: A byte string of length 32*bit len(b)
    """

    assert 0 <= all(element <= end for element in polynomial), "All Coefficients should be in range [0, end]"
    assert end > 0, "end should be a natural number"
    # assert len(polynomial) == 256, "Length of polynomial should be 256"

    z = ''
    for i in range(256):
        z += int_to_bits(polynomial[i], end.bit_length())

    return bits_to_bytes([int(i) for i in z])


def simple_bit_unpack(byte_string, end):
    """

    :param byte_string:
    :param end:
    :return:
    """

    c = end.bit_length()
    assert len(byte_string) == 32 * c, f"Length of byte string should be {32 * c} not {len(byte_string)}"
    z = bytes_to_bits(byte_string)
    w = []
    for i in range(256):
        w.append(bits_to_int(''.join([str(z[i*c + j]) for j in range(c)]), c))
    return w


def bit_pack(polynomial, start, end):
    """

    :param polynomial:
    :param start:
    :param end:
    :return:
    """

    z = ''
    for i in range(256):
        z += int_to_bits(end - polynomial[i], (start + end).bit_length())

    return bits_to_bytes([int(i) for i in z])


def bit_unpack(byte_string, start, end):
    """

    :param byte_string:
    :param start:
    :param end:
    :return:
    """

    c = (start + end).bit_length()
    z = bytes_to_bits(byte_string)
    w = []
    for i in range(256):
        w.append(end - bits_to_int(''.join([str(z[i * c + j]) for j in range(c)]), c))

    return w


def hint_bit_pack(polynomial_vector, K, OMEGA):
    """

    :param polynomial_vector:
    :param K:
    :param OMEGA:
    :return:
    """

    y = [0] * (K + OMEGA)
    index = 0
    for i in range(K):
        for j in range(256):
            if polynomial_vector[i][j] != 0:
                y[index] = j
                index += 1

        y[OMEGA + i] = index

    return bytes(y)


def hint_bit_unpack(byte_sting, K, OMEGA):
    """

    :param byte_sting:
    :param K:
    :param OMEGA:
    :return:
    """

    h = [[0] * 256 for _ in range(K)]
    index = 0
    for i in range(K):
        if byte_sting[OMEGA + i] < index or byte_sting[OMEGA + i] > OMEGA:
            return None
        first = index
        while index < byte_sting[OMEGA + i]:
            if index > first and byte_sting[index - 1] >= byte_sting[index]:
                return None
            h[i][byte_sting[index]] = 1
            index += 1

    for i in range(index, OMEGA):
        if byte_sting[i] != 0:
            return None
    return h
