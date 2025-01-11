from enum import Enum

class SHAKE128_S:
    N = 16
    H = 63
    D = 7
    H_PRIME = 9
    A = 12
    K = 14
    LGW = 4
    M = 30
    W = 16
    PUBLIC_KEY_BYTES = 32
    SIGNATURE_BYTES = 7856

    LENGTH_1 = 32
    LENGTH_2 = 3
    LENGTH = 35

class SHAKE128_F:
    N = 16
    H = 66
    D = 22
    H_PRIME = 3
    A = 6
    K = 33
    LGW = 4
    M = 34
    W = 16
    PUBLIC_KEY_BYTES = 32
    SIGNATURE_BYTES = 17_088

    LENGTH_1 = 32
    LENGTH_2 = 3
    LENGTH = 35
