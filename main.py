from core.algorithms.MLKEM import MLKEM

print("Alice side")
ml_kem_alice = MLKEM()
encaps, decaps = ml_kem_alice.key_gen()
print(f'encaps: {encaps}')
print(f'decaps: {decaps}')

print('Bob side')
ml_kem_bob = MLKEM()
k, ci = ml_kem_bob.encapsulation(encaps)
print(f'K (Bob): {k.hex()}')
print(f'cipher: {ci}')

print('Alice side')
k_ = ml_kem_alice.decapsulation(decaps, ci)
print(f'K (Alice): {k_.hex()}')
