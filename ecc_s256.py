from ecc import FieldElement, ECPoint

# Define constants that are used in Bitcoin for the secp256k1 curve
PRIME = 2**256 - 2**32 - 977
A = 0
B = 7



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
        # if x is None, then this represents the point at infinity (edge case)
        else:
            super().__init__(x, y, a, b)
    
    def __repr__(self):
        if self.x is None or self.y is None:
            return 'S256Point(infinity)'
        return 'S256Point({}, {}, {}, {})'.format(self.x, self.y, self.a, self.b)

    # since we know the order of the group, we mod by the order
    def __mul__(self, coefficient):
        coef = coefficient % N
        return super().__mul__(coef)
    
    def __rmul__(self, coefficient):
        return self * coefficient
    


N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G = S256Point(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
            0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)