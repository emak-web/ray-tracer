from __future__ import annotations
from math import sqrt
import numbers


class Vec3:
    def __init__(self, x: numbers.Real = 0.0, y: numbers.Real = 0.0, z: numbers.Real = 0.0):
        self.x, self.y, self.z = x, y, z
        
    def __repr__(self) -> str:
        return f'Vec3({self.x}, {self.y}, {self.z})'
    
    def __add__(self, vector: Vec3) -> Vec3:
        return Vec3(self.x+vector.x, self.y+vector.y, self.z+vector.z)
    
    def __sub__(self, vector: Vec3) -> Vec3:
        return Vec3(self.x-vector.x, self.y-vector.y, self.z-vector.z)
    
    def __neg__(self) -> Vec3:
        return Vec3(-self.x, -self.y, -self.z)

    def __mul__(self, other: numbers.Real | Vec3) -> Vec3:
        if isinstance(other, numbers.Real):
            return Vec3(self.x*other, self.y*other, self.z*other)
        
        return Vec3(self.x*other.x, self.y*other.y, self.z*other.z)
    
    def __rmul__(self, other: numbers.Real | Vec3) -> Vec3:
        return self.__mul__(other)

    def __truediv__(self, scalar: numbers.Real) -> Vec3:
        return Vec3(self.x/scalar, self.y/scalar, self.z/scalar)

    def length(self) -> numbers.Real:
        return sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def length_squared(self) -> numbers.Real:
        return self.x**2 + self.y**2 + self.z**2


class Point3(Vec3):
    pass

class Color(Vec3):
    pass


def dot(u: Vec3, v: Vec3) -> numbers.Real:
    return u.x*v.x + u.y*v.y + u.z*v.z


def cross(u: Vec3, v: Vec3) -> Vec3:
    return Vec3(
        u.y*v.z - v.y*u.z,
        u.z*v.x - v.z*u.x,
        u.x*v.y - v.x*u.y,
    )


def unit_vector(u: Vec3) -> Vec3:
    return u / u.length()


class Ray:
    def __init__(self, origin: Vec3, direction: Vec3):
        self.origin = origin
        self.direction = direction

    def at(self, t: numbers.Real) -> Vec3:
        return self.origin + t*self.direction
    