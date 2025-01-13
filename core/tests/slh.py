from core.utils.slh.wots import WOTS, Address
from core.utils.slh.xmss import XMSS

public_key_seed = b'\x00' * 32
address = Address(b'\x00' * 32)
private_key = b'\x00' * 32
message = b'\x00' * 32

# wots = WOTS(public_key_seed, address)
# public_key = wots.keygen(private_key)
# signature = wots.sign(message, private_key)
# print(f'public_key: {public_key}')
# print(f'signature: {signature}')
# public_key_derived = wots.public_key_from_sign(signature, message)

xmss = XMSS(public_key_seed, address)
index = 0
node = xmss.node(private_key, index, 0)
print(f'node: {node}')
signature = xmss.sign(message, private_key, index)
print(f'signature: {signature}')
public_key_derived = xmss.public_key_from_sign(index, signature, message)

print(f'public_key_derived: {public_key_derived}')



