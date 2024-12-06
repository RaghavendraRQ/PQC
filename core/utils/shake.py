from Crypto.Hash import SHAKE128, SHAKE256, SHA3_512, SHA3_256
import core.constants as const


def shake128(strings, byte_lengths):
    """
    Performs a sequence of absorbing and squeezing operations using SHAKE128.
    :param strings: List of byte arrays (str1, ..., strm).
    :param byte_lengths: List of positive integers (b1, ..., bl) indicating output byte lengths.
    :return: Concatenated output of the squeezing operations.
    """
    # Initialize context
    shake = SHAKE128.new()

    # Absorb each byte array into the context
    for string in strings:
        shake.update(string)

    # Squeeze outputs of specified lengths
    outputs = []
    for b in byte_lengths:
        outputs.append(shake.read(b))  # Read b bytes

    # Concatenate outputs
    return b''.join(outputs)


def sha3_512(ctx):
    sha3 = SHA3_512.new(ctx)
    hashed = sha3.digest()
    return hashed[:32], hashed[32:]


def sha3_256(ctx):
    sha3 = SHA3_256.new(ctx)
    return sha3.digest()


def prf(byte_string, b, eta=None):
    shake256 = SHAKE256.new(byte_string)
    shake256.update(b)
    return shake256.read(64 * (eta or const.ETA))


def shake256(ctx):
    shake256 = SHAKE256.new(ctx)
    return shake256.read(32)
