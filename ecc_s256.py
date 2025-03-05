from ecc import FieldElement, ECPoint

# Define constants that are used in Bitcoin for the secp256k1 curve
PRIME = 2**256 - 2**32 - 977
A = 0
B = 7
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


class S256Field(FieldElement):
    def __init__(self, num, prime=None):
        super().__init__(num=num, prime=PRIME)
    
    def __repr__(self):
        return '{:x}'.format(self.num).zfill(64)


class S256Point(ECPoint):
    def __init__(self, x, y, a=None, b=None):
        a, b = S256Field(A), S256Field(B)
        if type(x) == int:
            super().__init__(S256Field(x), S256Field(y), a, b)
        elif type(x) == S256Field:
            super().__init__(x, y, a, b)
        else:
            raise TypeError(f"Unrecognized type {type(x)}")
    
    def __repr__(self):
        if self.x is None and self.y is None:
            return 'S256Point(infinity)'
        return 'S256Point({}, {})'.format(self.x, self.y)