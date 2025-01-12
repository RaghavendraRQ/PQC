"""
eXtended Merkle Signature Scheme (XMSS) implementation.

XMSS extends the Winternitz one-time signature scheme with a binary tree of height h. The tree is used to sign multiple
messages. The tree is built from the WOTS+ one-time signature scheme. The WOTS+ one-time signature scheme is a
modification of the Winternitz one-time signature scheme that allows for chaining of WOTS+ instances.
This chaining is used to sign the root of the binary tree.
"""
from core.utils.slh.wots import WOTS, Address
from core.utils.hash import slh_H


class XMSS:
    """
    XMSS Signature data format
    h - height of the binary tree
    len - length of the message
    n - number of WOTS+ instances in the tree

    ++-------------++
    || Signature   ||
    ++-------------++
    ||  Auth[0]    ||
    ++-------------++
    ||  ...        ||
    ++-------------++
    ||  Auth[h-1]  ||

    Each Auth[i] is an n-byte value
    """

    def __init__(self, public_key_seed, address):
        """
        Initializes a XMSS object with the given public key seed and address
        Args:
            public_key_seed:    32 byte public key seed
            address:            Address object

        Returns:
            XMSS object
        """
        self.public_key_seed = public_key_seed
        self.address = address
        self.wots = WOTS(public_key_seed, address)

    def node(self, private_key_seed, node_index, node_height):
        """
        Generates a node for the given node index and height
        Args:
            private_key_seed:   32 byte private key seed
            node_index:         index of the node
            node_height:        height of the node

        Returns:
            n - byte root node
        """
        if node_height == 0:
            self.address.type, self.address.key_pair = 0, node_index
            self.wots = WOTS(self.public_key_seed, self.address)
            return self.wots.keygen(private_key_seed)
        else:
            left_node = self.node(private_key_seed, 2 * node_index, node_height - 1)
            right_node = self.node(private_key_seed, 2 * node_index + 1, node_height - 1)

            self.address.type, self.address.key_pair = 2, node_index
            self.address.tree_height = node_height
            return slh_H(self.public_key_seed, self.address.address, left_node + right_node)


    def sign(self, message, private_key_seed, index):
        """
        Generates a signature for the given message using the private key seed and index
        Args:
            message:            32 byte message
            private_key_seed:   32 byte private key seed
            index:              index of the message

        Returns:
            XMSS signature
        """
        signature = [b'' for _ in range(self.address.h + 1)]
        auth = [b'' for _ in range(self.address.h)]
        for i in range(self.address.h):
            auth[i] = self.node(private_key_seed, index >> i, i)

        signature[0] = self.wots.sign(message, private_key_seed)
        for i in range(self.address.h):
            signature[i + 1] = auth[i]

        return b''.join(signature)