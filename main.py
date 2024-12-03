from core.utils.sampleNtt import sample_ntt, sample_poly_cbd
seed = b"This is a 32-byte seed used for NT"


# Call SampleNTT with the seed and modulus q
ntt_coefficients = sample_ntt(seed)
eta = 2
seed = b"This is a 64-byte seed used for CBD but it is not a multiple s22" * eta
polynomial = sample_poly_cbd(seed, eta)
