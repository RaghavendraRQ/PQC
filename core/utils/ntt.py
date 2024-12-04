from core.constants import ZETA_VALUES, ZETA_DOUBLE_VALUES, N, Q


def ntt(f, q=Q, zeta_values=ZETA_VALUES):
    """
    Computes the NTT of a given polynomial f.
    :param f: Array of polynomial coefficients in Z_q (length 256).
    :param q: Modulus for the field (default is 3329).
    :param zeta_values: Precomputed zeta values for bit-reversed ordering (length 256).
    :return: Array of NTT coefficients f_hat in Z_q.
    """
    f_cap = f.copy()
    i = 1
    length = 128
    while length >= 2:
        for start in range(0, 256, 2 * length):
            zeta = zeta_values[i]
            i += 1
            for j in range(start, start + length):
                t = (zeta * f_cap[j + length]) % q
                f_cap[j + length] = (f_cap[j] - t) % q
                f_cap[j] = (f_cap[j] + t) % q
        length //= 2
    return f_cap


def ntt_inverse(f_cap, q=Q, zeta_values=ZETA_VALUES):
    """
            Computes the inverse NTT (NTT_Inverse) of a given NTT representation f_cap.
            :param f_cap: Array of NTT coefficients in Z_q (length 256).
            :param q: Modulus for the field (default is 3329).
            :param zeta_values: Precomputed zeta values for bit-reversed ordering (length 256).
            :return: Array of polynomial coefficients f in Z_q.
            """
    f = f_cap.copy()
    i = 127  # Start with the last zeta value for inverse NTT
    length = 2
    while length <= 128:
        for start in range(0, 256, 2 * length):
            zeta = zeta_values[i]
            i -= 1
            for j in range(start, start + length):
                t = f[j]  # Save the value of f[j]
                f[j] = (t + f[j + length]) % q  # f[j] = f[j] + f[j + length]
                f[j + length] = (zeta * (f[j + length] - t)) % q  # f[j+length] = zeta * (f[j+length] - t)
        length *= 2
    scale_factor = 3303
    f = [(x * scale_factor) % q for x in f]
    return f


def base_case_multiply(a0, a1, b0, b1, zeta):
    c0 = (a0 * b0 + a1 * b1 * zeta) % Q
    c1 = (a0 * b1 + a1 * b0) % Q
    return c0, c1


def multiply_ntt(f_cap, g_cap):
    h_cap = [0] * 256
    for i in range(128):
        h_cap[2 * i], h_cap[2 * i + 1] = base_case_multiply(f_cap[2 * i], f_cap[2 * i + 1],
                                                            g_cap[2 * i], g_cap[2 * i + 1], ZETA_DOUBLE_VALUES[i])
    return h_cap

