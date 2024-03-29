from math import sqrt


class Vector:
    """
    2D vector.
    """
    __slots__ = ["x", "y"]

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def copy(self) -> "Vector":
        """Copies the vector"""
        return Vector(self.x, self.y)

    def sqnorm(self):
        """Squared norm, useful for comparisons, faster than the norm."""
        return self.x * self.x + self.y * self.y

    def norm(self):
        """Euclidean norm of the vector."""
        return sqrt(self.sqnorm())

    def normalized(self):
        norm = self.norm()
        return self / norm

    def dot_product(self, other: "Vector") -> float:
        return self.x * other.x + self.y * other.y

    def cross_product(self, other: "Vector") -> float:
        return self.x * other.y - self.y * other.x

    def orthogonal(self):
        return Vector(-self.y, self.x)

    def __iter__(self):
        return iter((self.x, self.y))

    def __add__(self, vec):
        return Vector(self.x + vec.x, self.y + vec.y)

    def __iadd__(self, vec):
        self.x += vec.x
        self.y += vec.y
        return self

    def __sub__(self, vec):
        return Vector(self.x - vec.x, self.y - vec.y)

    def __isub__(self, vec):
        self.x -= vec.x
        self.y -= vec.y

    def __mul__(self, k):
        return Vector(self.x * k, self.y * k)

    def __imul__(self, k):
        self.x *= k
        self.y *= k

    def __truediv__(self, k):
        return Vector(self.x / k, self.y / k)

    def __itruediv__(self, k):
        self.x /= k
        self.y /= k

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __abs__(self):
        return Vector(abs(self.x), abs(self.y))

    def __eq__(self, other):
        return isinstance(other, Vector) and other.x == self.x and other.y == self.y

    def __hash__(self):
        return 31*hash(self.x) + hash(self.y)

    def __str__(self) -> str:
        return f"({self.x},{self.y})"

    def __repr__(self) -> str:
        return f"Vector({self.x},{self.y})"
