from core.utils.slh.wots import WOTS, Address

public_key_seed = b'\x00' * 32
address = Address(b'\x00' * 32)
wots = WOTS(public_key_seed, address)
private_key = b'\x00' * 32
public_key = wots.keygen(private_key)
message = b'\x00' * 32
signature = wots.sign(message, private_key)
print(f'public_key: {public_key}')
print(f'signature: {signature}')

