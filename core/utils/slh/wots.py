from core.utils.bits import int_to_bytes, bytes_to_int


class Address:
    def __init__(self, address = bytes(32)):
        """
        Initializes an Address object with a given address (Big Endian)
        layer_address: First 4 byte address of the layer
        tree_address: 12 byte address of the tree
        type: 4 byte address of the type
              0 - WOTS_HASH
              1 - WOTS_PK
              2 - TREE
              3 - FORS_TREE
              4 - FORS_ROOTS
              5 - WOTS_PRF
              6 - FORS_PRF
        Args:
            address: 32 byte address
        """
        if not len(address) == 32:  # Check if the address is 32 Words
            raise ValueError(f"Address should be 32 bytes. Not {len(address)}")

        self.address = address
        # Following word bytes are same for all types
        self._layer_address = address[:4]
        self._tree_address = address[4:16]
        self._type = address[16:20]

        # Depending on the type, the address will be different for the chain and tree
        self._key_pair = address[20:24]
        self._chain_address = address[20:28]
        self._tree_height = address[20:28]

        # Depending on the type, the address will be different for the hash and tree
        self._hash_address = address[28:]
        self._tree_index = address[28:]


    @property
    def layer_address(self):
        return self._layer_address

    @property
    def tree_address(self):
        return self._tree_address

    @property
    def type(self):
        return self._type

    @property
    def key_pair(self):
        return bytes_to_int(self.address[20:24], 4)

    @property
    def tree_index(self):
        return bytes_to_int(self.address[28:], 4)

    @layer_address.setter
    def layer_address(self, value):
        self._layer_address = int_to_bytes(value, 4)
        self.address = self._layer_address + self.address[4:]

    @tree_address.setter
    def tree_address(self, value):
        self._tree_address = int_to_bytes(value, 12)
        self.address = self.address[:4] + self._tree_address + self.address[16:]

    @type.setter
    def type(self, value):
        self._type = int_to_bytes(value, 4)
        self.address = self.address[:16] + self._type + int_to_bytes(0, 12)


def chain(byte_string, index, steps, public_key, address):
    temp = byte_string
    pass