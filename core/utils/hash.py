from Crypto.Hash import SHAKE128, SHAKE256, SHA3_512, SHA3_256


def shake128(ctx, byte_lengths):
    """
    Performs a sequence of absorbing and squeezing operations using SHAKE128.

    Args:
        ctx:  List of byte arrays.
        byte_lengths: List of positive integers (b1, ..., bl) indicating output byte lengths.

    Returns:
        Concatenated output of the squeezing operations
    """

    shake = SHAKE128.new()
    for string in ctx:
        shake.update(string)
    outputs = []
    for b in byte_lengths:
        outputs.append(shake.read(b))
    return b''.join(outputs)


def sha3_512(ctx):
    """
    Generates sha3 512 hash for the given context
    Args:
        ctx: a byte string or byte array

    Returns:
        Tuple: first 32 hashed bytes and remaining
    """
    sha3 = SHA3_512.new(ctx)
    hashed = sha3.digest()
    return hashed[:32], hashed[32:]


def sha3_256(ctx):
    """
    Generates a sha3_256 hash for the given context
    Args:
        ctx: A byte string or array

    Returns:
        bytes: Hashed values of the ctx
    """
    sha3 = SHA3_256.new(ctx)
    return sha3.digest()


def prf(ctx, b, eta):
    """
    Generates a shake_256 hash. (use only in KPKE)
    Args:
        ctx: byte string or array
        b: next bytes
        eta: A Constant value which is used to read the data

    Returns:
        bytes: Hashed values of byte string and b with length 64 * ETA
    """
    shake_256 = SHAKE256.new(ctx)
    shake_256.update(b)
    return shake_256.read(64 * eta)


def shake256(ctx):
    """
    Generates a shake256 hash for the given context
    Args:
        ctx: a byte string

    Returns:
        bytes: Hashed value for the given context
    """
    shake_256 = SHAKE256.new(ctx)
    return shake_256.read(32)
