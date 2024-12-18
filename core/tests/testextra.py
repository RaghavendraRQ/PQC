from core.algorithms.MLDSA import MLDSA

ml_dsa = MLDSA()
public_key, private_key = ml_dsa.keygen()
print(f'private_key: {private_key}')
print(f'public_key: {public_key}')
message = [1, 0, 1, 1, 0, 1, 0, 1]
signature = ml_dsa.sign(private_key, message, b'1234')
print(f'signature: {signature}')
print(ml_dsa.verify(public_key, message, signature, b''))

