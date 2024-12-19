from core.utils.bits import int_to_bits, bits_to_bytes, bytes_to_bits, bits_to_int
from core.utils.overflow.stubborn import NTTModified, VectorNTT

import core.constants.dsa44 as const


def simple_bit_pack(polynomial, end):
    """
    Encodes a polynomial into a byte string

    Args:
        polynomial: A list of coefficients in range [0,end]
        end: A Natural Number

    Returns:
        bytes: A byte string of length 32*bit_len(b)
    """

    if not polynomial.check(0, end):
        raise ValueError("All Coefficients should be in range [0, end].")
    if not end > 0:
        raise ValueError("End should be greater than 0.")

    z = ''
    for i in range(256):
        z += int_to_bits(polynomial[i], end.bit_length())

    return bits_to_bytes([int(i) for i in z])


def simple_bit_unpack(byte_string, end):
    """
    Reverses the procedure simple_bit_pack

    Args:
        byte_string: Byte string of length 32*bit_len(end)
        end: A Natural number

    Returns:
        NTTModified: Newly created NTT Object from byte string
    """

    c = end.bit_length()
    if not len(byte_string) == 32 * c:
        raise ValueError(f"Length of byte string should be {32 * c} not {len(byte_string)}")

    z = bytes_to_bits(byte_string)
    w = NTTModified(const)
    for i in range(256):
        w.polynomial[i] = (bits_to_int(''.join([str(z[i*c + j]) for j in range(c)]), c))
    return w


def bit_pack(polynomial, start, end):
    """
    Encodes a polynomial into a byte string

    Args:
        polynomial: A NTTModified Object
        start: Starting coefficient > 0
        end: Ending Coefficient > start

    Returns:
        bytes: A byte string of length 32*bit_len(b)
    """
    if not polynomial.check(-start, end):
        raise ValueError("All Coefficients should be in range [0, end].")

    z = ''
    for i in range(256):
        z += int_to_bits(end - polynomial[i], (start + end).bit_length())

    return bits_to_bytes([int(i) for i in z])


def bit_unpack(byte_string, start, end):
    """
    Reverses the procedure bit_pack

    Args:
        byte_string: Byte string of length 32*bit_len(end)
        start: Starting coefficient > 0
        end: Ending Coefficient > start

    Returns:
        NTTModified: Newly created NTT Object from byte string
    """
    c = (start + end).bit_length()
    if not len(byte_string) == 32 * c:
        raise ValueError(f"Length of byte string should be {32 * c} not {len(byte_string)}")

    z = bytes_to_bits(byte_string)
    w = NTTModified(const)
    for i in range(256):
        w.polynomial[i] = (end - bits_to_int(''.join([str(z[i * c + j]) for j in range(c)]), c))
    return w


def hint_bit_pack(polynomial_vector, K, OMEGA):
    """
    Encodes a NTT polynomial h with binary coefficients into a byte string

    Args:
        polynomial_vector: A VectorNTT object
        K: Algorithm specific constant
        OMEGA: Algorithm specific constant

    Returns:
        bytes: A byte string of len OMEGA+K that encodes h
    """
    if not polynomial_vector.check(0, 1):
        raise ValueError('All the coefficients should be in binary')

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
    Reverses the procedure of hint_bit_pack

    Args:
        byte_sting: byte string of len K+OMEGA
        K: Algorithm specific constant
        OMEGA: Algorithm specific constant

    Returns:
        VectorNTT: A newly created VectorNTT object
    """
    if not len(byte_sting) == K + OMEGA:
        raise ValueError(f"byte string should be {K+OMEGA}. Not {len(byte_sting)}")

    h = VectorNTT(const)
    index = 0
    # Reconstruct h
    for i in range(K):
        if byte_sting[OMEGA + i] < index or byte_sting[OMEGA + i] > OMEGA:
            return None
        first = index
        while index < byte_sting[OMEGA + i]:
            if index > first and byte_sting[index - 1] >= byte_sting[index]:    # Malformed Input
                return None
            h[i][byte_sting[index]] = 1
            index += 1

    for i in range(index, OMEGA):
        if byte_sting[i] != 0:
            return None
    return h
