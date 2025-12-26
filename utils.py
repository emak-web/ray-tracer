from __future__ import annotations
from dataclasses import dataclass
import numbers
import math
import random


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
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def length_squared(self) -> numbers.Real:
        return self.x**2 + self.y**2 + self.z**2

    @staticmethod
    def random(min_v: numbers.Real = 0, max_v: numbers.Real = 1) -> Vec3:
        return Vec3(random.uniform(min_v, max_v), random.uniform(min_v, max_v), random.uniform(min_v, max_v))
    

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


def random_unit_vector() -> Vec3:
    while True:
        p = Vec3.random(-1, 1)
        lensq = p.length_squared()
        if 1e-160 < lensq <= 1:
            return p / math.sqrt(lensq)


def random_on_hemisphere(normal: Vec3) -> Vec3:
    on_unit_sphere = random_unit_vector()
    if dot(on_unit_sphere, normal) > 0:
        return on_unit_sphere
    else:
        return -on_unit_sphere


class Ray:
    def __init__(self, origin: Vec3, direction: Vec3):
        self.origin = origin
        self.direction = direction

    def at(self, t: numbers.Real) -> Vec3:
        return self.origin + t*self.direction


@dataclass
class Interval:
    min: numbers.Real = +math.inf
    max: numbers.Real = -math.inf
    
    def size(self) -> numbers.Real:
        return self.max - self.min

    def contains(self, x: numbers.Real) -> bool:
        return self.min <= x <= self.max

    def surrounds(self, x: numbers.Real) -> bool:
        return self.min < x < self.max

    def clamp(self, x: number.Real) -> numbers.Real:
        if x > self.max:
            return self.max
        if x < self.min:
            return self.min
        return x


Interval.empty = Interval(+math.inf, -math.inf)
Interval.universe = Interval(-math.inf, +math.inf)

