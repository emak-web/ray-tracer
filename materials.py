from __future__ import annotations
from utils import Vec3, Ray, Color, dot, unit_vector
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from hittable import HitRecord
from abc import ABC, abstractmethod

import numbers
import random
import math


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


def reflect(v: Vec3, n: Vec3) -> Vec3:
    return v - 2*dot(v, n)*n


def refract(uv: Vec3, n: Vec3, etai_over_etat: numbers.Real) -> Vec3:
    cos_theta = min(dot(-uv, n), 1)
    r_out_perp = etai_over_etat * (uv + cos_theta*n)
    r_out_parallel = -math.sqrt(1 - r_out_perp.length_squared()) * n
    return r_out_perp + r_out_parallel


class Material(ABC):
    @abstractmethod
    def scatter(self, r_in: Ray, rec: HitRecord) -> bool:
        return None


class Lambertian(Material):
    def __init__(self, albedo: Color):
        self.albedo = albedo

    def scatter(self, r_in: Ray, rec: HitRecord) -> bool:
        scatter_direction = rec.normal + random_unit_vector()

        if scatter_direction.near_zero():
            scatter_direction = rec.normal
        
        scattered = Ray(rec.p, scatter_direction)
        return self.albedo, scattered


class Metal(Material):
    def __init__(self, albedo: Color, fuzz: numbers.Real = 1):
        self.albedo = albedo
        self.fuzz = fuzz

    def scatter(self, r_in: Ray, rec: HitRecord) -> bool:
        attenuation = self.albedo
        reflected = reflect(r_in.direction, rec.normal)
        reflected = unit_vector(reflected) + (self.fuzz * random_unit_vector())
        scattered = Ray(rec.p, reflected)
        return attenuation, scattered


class Dielectric(Material):
    def __init__(self, refraction_index: numbers.Real):
        self.refraction_index = refraction_index

    def scatter(self, r_in: Ray, rec: HitRecord) -> bool:
        attenuation = Color(1, 1, 1)
        ri = (1 / self.refraction_index) if rec.front_face else self.refraction_index
        unit_direction = unit_vector(r_in.direction)
        cos_theta = min(dot(-unit_direction, rec.normal), 1)
        sin_theta = math.sqrt(1 - cos_theta**2)

        cannot_refract = ri * sin_theta > 1
        direction = None

        if cannot_refract or self.reflectance(cos_theta, ri) > random.random():
            direction = reflect(unit_direction, rec.normal)
        else:
            direction = refract(unit_direction, rec.normal, ri)

        scattered = Ray(rec.p, direction)
        return attenuation, scattered

    def reflectance(self, cosine: numbers.Real, refractive_index: numbers.Real):
        r0 = (1 - refractive_index) / (1 + refractive_index)
        r0 *= r0
        return r0 + (1-r0)*pow((1 - cosine), 5)
