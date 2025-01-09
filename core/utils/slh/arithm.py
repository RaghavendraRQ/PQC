def precomputed_len():
    return 3


def gen_len(security_parameter, bits_per_hash):
    w = 2 ** bits_per_hash
    length_1 = (8 * security_parameter + bits_per_hash - 1) // bits_per_hash
    max_check_sum = length_1 * (w - 1)

    length_2 = 1
    capacity = w
    while capacity <= max_check_sum:
        length_2 += 1
        capacity *= w

    return length_2


def base_2b(byte_string, bit_length, output_length):
    _in, bits, total = 0, 0, 0
    output = [0] * output_length
    for out in range(output_length):
        while bits < bit_length:
            bits += 8
            total = total << 8 | byte_string[_in]
            _in += 1
        bits -= bit_length
        output[out] = (total >> bits) % (1 << bit_length)
    return output



