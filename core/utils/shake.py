from Crypto.Hash import SHAKE128


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
