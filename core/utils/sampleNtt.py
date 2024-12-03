from Crypto.Hash import SHAKE128

from core.utils.bits import bytes_to_bits


def sample_ntt(byte_array, q=3329):
    """
    Samples a pseudorandom element of T_q using a 34-byte seed and two indices.
    :param byte_array: 34-byte seed (input as a byte array).
    :param q: Modulus for the field T_q (default 3329).
    :return: Array of coefficients a ∈ ℤ_256 (NTT coefficients).
    """
    assert len(byte_array) == 34, f"The byte array must be 34 bytes in length. Not {len(byte_array)}."

    # Initialize XOF (using SHAKE128)
    shake = SHAKE128.new()
    shake.update(byte_array)

    # Array to store the NTT coefficients
    a = [0] * 256
    j = 0

    # Sampling loop
    while j < 256:
        # Get 3 fresh bytes from XOF
        c = shake.read(3)

        # Extract d1 and d2 from the 3-byte array
        d1 = c[0] + 256 * (c[1] % 16)
        d2 = (c[1] // 16) + 16 * c[2]

        # If d1 is within range, store it in the array
        if d1 < q:
            a[j] = d1
            j += 1

        # If d2 is within range and we haven't filled the array, store it in the array
        if d2 < q and j < 256:
            a[j] = d2
            j += 1
    return a


def sample_poly_cbd(byte_array, eta, q=3329):
    """
    Samples a pseudorandom polynomial from the distribution D_eta(R_q).
    :param byte_array: Byte array of size 64 * eta (input as a byte array).
    :param eta: The parameter eta that defines the range for the distribution.
    :param q: Modulus for the field (default is 3329).
    :return: Array of polynomial coefficients f ∈ ℤ_256.
    """
    expected_length = 64 * eta
    assert len(byte_array) == expected_length, f"The byte array must be of length {expected_length} (64 * eta)."

    bit_array = bytes_to_bits(byte_array)
    print(f'len(bit_array): {len(bit_array)}')
    f = [0] * 256
    for i in range(256):
        x = sum(bit_array[2 * i * eta + j] for j in range(eta))
        y = sum(bit_array[2 * i * eta + eta + j] for j in range(eta))
        f[i] = (x - y) % q
    return f
