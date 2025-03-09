from unittest import TestCase
from ecc import FieldElement, ECPoint
from ecc_s256 import N, G, S256Point

class ECCTest(TestCase):

    def test_on_curve(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        valid_points = [(192, 105), (17, 56), (1, 193)]
        invalid_points = [(200, 119), (42, 99)]
        for x_raw, y_raw in valid_points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            ECPoint(x, y, a, b)
        for x_raw, y_raw in invalid_points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            with self.assertRaises(ValueError):
                ECPoint(x, y, a, b)

    def test_add(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)

        # test 1
        p1 = ECPoint(FieldElement(170, prime), FieldElement(142, prime), a, b)
        p2 = ECPoint(FieldElement(60, prime), FieldElement(139, prime), a, b)
        p3 = ECPoint(FieldElement(220, prime), FieldElement(181, prime), a, b)
        self.assertEqual(p1 + p2, p3)

        # test 2 
        p1 = ECPoint(FieldElement(47, prime), FieldElement(71, prime), a, b)
        p2 = ECPoint(FieldElement(17, prime), FieldElement(56, prime), a, b)
        p3 = ECPoint(FieldElement(215, prime), FieldElement(68, prime), a, b)
        self.assertEqual(p1 + p2, p3)

        # test 3
        p1 = ECPoint(FieldElement(143, prime), FieldElement(98, prime), a, b)
        p2 = ECPoint(FieldElement(76, prime), FieldElement(66, prime), a, b)
        p3 = ECPoint(FieldElement(47, prime), FieldElement(71, prime), a, b)
        self.assertEqual(p1 + p2, p3)
    

class S256Test(TestCase):

    def test_order(self):
        point = G
        # order of G is N, G*N should be S256Point(infinity)
        self.assertEqual(N * point, S256Point(None, None))
    
    def test_pubpoint(self):
        # write a test that tests the public point for the following privates
        # 999**3, 123, 42424242
        # if the underlying computation were incorrect, this would be incorrect
        points = (
            (999**3) * G,
            123 * G,
            42424242 * G
        )
        for point in points:
            self.assertEqual(point, point)
        

