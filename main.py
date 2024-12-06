from core.algorithms.ML_KEM import ML_KEM

ml_kem = ML_KEM()

encaps, decaps = ml_kem.key_gen()
k, c = ml_kem.encapsulation(encaps)
k_ = ml_kem.decapsulation(decaps, c)

print(f'k: {k}')
print(f'K_: {k_}')
