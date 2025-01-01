import math


def mod_symmetric(m, a):
    """
    Compute the symmetric modulo operation.

    Args:
        m (int): The integer input.
        a (int): The positive integer modulus.

    Returns:
        int: The result of m (± mod a) in the symmetric range −⌈a/2⌉ < m′ ≤ ⌊a/2⌋.
    """
    if a <= 0:
        raise ValueError("The modulus 'a' must be a positive integer.")

    m_standard = m % a

    half_a = a / 2  # Floating-point value for precise ceiling and floor handling
    upper_bound = math.floor(half_a)  # ⌊a/2⌋

    if m_standard > upper_bound:
        return m_standard - a
    return m_standard


def power2_round(r, Q, D):
    """
    Round a number to the nearest multiple of 2^D in the ring Z_Q.
    Args:
        r: An Integer
        Q: Modulus
        D: Drop bits

    Returns:
        Tuple[int, int]: The tuple of the rounded number and the dropped bits.
    """

    r1 = r % Q
    r0 = mod_symmetric(r1, 2 ** D)
    return (r1 - r0) // (2 ** D), r0


def decompose(r, Q, GAMMA_2):
    """
    Decompose a number into the sum of a multiple of GAMMA_2 and a small number.
    Args:
        r: An Integer
        Q: Modulus
        GAMMA_2: Low Order Rounding Range

    Returns:
        Tuple[int, int]: The tuple of the multiple of GAMMA_2 and the small number.
    """
    # assert r < Q, "r should be less than Q"

    r1 = r % Q
    r0 = mod_symmetric(r1, 2 * GAMMA_2)
    if r1 - r0 == Q - 1:
        return 0, r0 - 1
    r1 = (r1 - r0) // (2 * GAMMA_2)
    return r1, r0


def high_bits(r, Q, GAMMA_2):
    """
    Extract the high bits of a number.
    Args:
        r: An Integer
        Q: Modulus
        GAMMA_2: Low Order Rounding Range

    Returns:
        int: The high bits of the number
    """
    # assert r < Q, "r should be less than Q"

    r1, r0 = decompose(r, Q, GAMMA_2)
    return r1


def low_bits(r, Q, GAMMA_2):
    """
    Extract the low bits of a number.
    Args:
        r: An Integer
        Q: Modulus
        GAMMA_2: Low Order Rounding Range

    Returns:
        int: The low bits of the number
    """

    r1, r0 = decompose(r, Q, GAMMA_2)
    return r0


def make_hint(z, r, Q, GAMMA_2):
    """
    Computes hint by indicating whether adding z to r alter the high bits of r.

    Args:
        z: An Integer
        r: An Integer
        Q: Modulus
        GAMMA_2: Low Order Rounding Range

    Returns:
        bool: True if adding z to r alters the high bits of r, False otherwise.
    """
    assert r < Q, "r should be less than Q"
    assert z < Q, "z should be less than Q"

    r1 = high_bits(r, Q, GAMMA_2)
    v1 = high_bits(r + z, Q, GAMMA_2)
    return 1 if r1 != v1 else 0


def use_hint(h, r, Q, GAMMA_2):
    """
    Apply a hint to a number.

    Args:
        h: A Boolean hint
        r: An Integer
        Q: Modulus
        GAMMA_2: Low Order Rounding Range

    Returns:
        int: The number after applying the hint.
    """
    assert r < Q, "r should be less than Q"

    m = (Q - 1) // (2 * GAMMA_2)
    r1, r0 = decompose(r, Q, GAMMA_2)
    if h == 1 and r0 > 0:
        return (r1 + 1) % m
    elif h == 1 and r0 <= 0:
        return (r1 - 1) % m
    return r1
