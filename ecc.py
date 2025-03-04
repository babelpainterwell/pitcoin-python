class FieldElement:

    def __init__(self, num, prime):
        if num >= prime or num < 0:
            error = f"Num {num} not in field range 0 to {prime-1}"
            raise ValueError(error)
        self.num = num
        self.prime = prime
    
    def __repr__(self):
        return f"FieldElement_{self.prime}({self.num})"

    def __eq__(self, other):
        if other is None:
            return False 
        return self.num == other.num and self.prime == other.prime

    def __ne__(self, other):
        return not (self == other)
    
    def __add__(self, other):
        if self.prime != other.prime:
            raise TypeError("Cannot add two numbers in different Fields")
        num = (self.num + other.num) % self.prime 
        return self.__class__(num, self.prime)

    def __sub__(self, other):
        if self.prime != other.prime:
            raise TypeError("Cannot subtract two numbers in different Fields")
        num = (self.num - other.num) % self.prime
        return self.__class__(num, self.prime)

    def __mul__(self, other):
        if isinstance(other, FieldElement):
            if self.prime != other.prime:
                raise TypeError("Cannot multiply two numbers in different Fields")
            num = (self.num * other.num) % self.prime
            return self.__class__(num, self.prime)
        elif isinstance(other, int):
            num = (self.num * other) % self.prime
            return self.__class__(num, self.prime)
        else:
            raise TypeError(f"Cannot multiply FieldElement with {type(other)}")
    
    def __rmul__(self, coefficient):
        return self.__mul__(coefficient)

    # Leverage Fermat's Little Theorem to reduce the number of operations
    # the exponent could be negative
    def __pow__(self, exponent):
        # shrink the exponent
        n = exponent % (self.prime - 1)
        # n = exponent 
        # while n < 0:
        #     n += self.prime - 1 
        num = pow(self.num, n, self.prime)
        return self.__class__(num, self.prime)

    def __truediv__(self, other):
        if self.prime != other.prime:
            raise TypeError("Cannot divide two numbers in different Fields")
        # a ** (-1) = a ** (p - 2) % p since a ** (-1) * a = 1 = a ** (p - 1) due to Fermat's Little Theorem
        num = self.num * pow(other.num, self.prime - 2, self.prime) % self.prime
        return self.__class__(num, self.prime)



class ECPoint:
    def __init__(self, x, y, a, b):
        self.x = x
        self.y = y 
        self.a = a
        self.b = b 
        # use None to signify the point at infinity
        if self.x is None and self.y is None:
            return
        if self.y ** 2 != self.x ** 3 + a * x + b:
            raise ValueError(f"({x}, {y}) is not on the curve")
    
    def __repr__(self):
        if self.x is None or self.y is None:
            return "ECPoint(infinity)"
        return f"ECPoint({self.x}, {self.y}) on y^2 = x^3 + {self.a}x + {self.b}"
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.a == other.a and self.b == other.b

    def __ne__(self, other):
        return not (self == other)

    def __add__(self, other):
        if self.a != other.a or self.b != other.b:
            raise TypeError(f"Points {self}, {other} are not on the same curve")
        # Case 0.0: self is the point at infinity, return other
        if self.x is None:
            return other
        # Case 0.1: other is the point at infinity, return self
        if other.x is None:
            return self
        # Case 1: self.x == other.x, self.y != other.y
        if self.x == other.x and self.y != other.y:
            return self.__class__(None, None, self.a, self.b)
        # Case 2: self.x != other.x
        if self.x != other.x:
            s = (other.y - self.y) / (other.x - self.x)
            x = s ** 2 - self.x - other.x
            y = s * (self.x - x) - self.y
            return self.__class__(x, y, self.a, self.b)
        # Case 3: self == other
        if self == other:
            # if self.y == 0: # example uses self.u == 0 * self.x
            # for future FieldElement operation use, apply self.x to indicate a field operation
            if self.y == self.x * 0:
                return self.__class__(None, None, self.a, self.b)
            else:
                s = (3 * self.x ** 2 + self.a) / (2 * self.y)
                x = s ** 2 - 2 * self.x
                y = s * (self.x - x) - self.y
                return self.__class__(x, y, self.a, self.b)
    
    def __mul__(self, coefficient):
        # apply binary expansion 
        coef = coefficient 
        current = self 
        result = self.__class__(None, None, self.a, self.b)
        while coef:
            if coef & 1:
                result += current 
            current += current 
            coef >>= 1 
        return result

    def __rmul__(self, coefficient):
        return self.__mul__(coefficient)

            



    
    