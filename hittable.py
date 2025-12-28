from dataclasses import dataclass
from abc import ABC, abstractmethod
import numbers

from utils import Point3, Vec3, Ray, dot, Interval, Material
from math import sqrt


@dataclass
class HitRecord:
    p: Point3
    normal: Vec3
    mat: Material
    t: numbers.Real
    front_face: bool = True

    def set_face_normal(self, r: Ray, outward_normal: Vec3):
        self.front_face = dot(r.direction, outward_normal) < 0
        self.normal = outward_normal if self.front_face else -outward_normal


class Hittable(ABC):
    @abstractmethod
    def hit(self, r: Ray, t_min: numbers.Real, t_max: numbers.Real):
        pass
        

class Sphere(Hittable):
    def __init__(self, center: Point3, radius: numbers.Real, mat: Material):
        self.center = center
        self.radius = radius
        self.mat = mat
    
    def hit(self, r: Ray, ray_t: Interval) -> HitRecord:
        oc = self.center - r.origin
        a = r.direction.length_squared()
        h = dot(r.direction, oc)
        c = oc.length_squared() - self.radius*self.radius
        d = h*h - a*c

        if d < 0:
            return None
        
        sqrtd = sqrt(d)
        root = (h - sqrtd) / a
        
        if not ray_t.surrounds(root):
            root = (h + sqrtd) / a
            if not ray_t.surrounds(root):
                return None

        rec = HitRecord(r.at(root), (r.at(root) - self.center) / self.radius, self.mat, root)
        outward_normal = (rec.p - self.center) / self.radius
        rec.set_face_normal(r, outward_normal)

        return rec
    

class HittableList(Hittable):
    def __init__(self, *objects: Hittable):
        self.objects = [i for i in objects]

    def clear(self):
        self.objects = []

    def add(self, object: Hittable):
        self.objects.append(object)
        
    def hit(self, r: Ray, ray_t: Interval) -> HitRecord:
        rec = None
        closest_so_far = ray_t.max

        for object in self.objects:
            temp_rec = object.hit(r, Interval(ray_t.min, closest_so_far))
            if temp_rec is not None:
                rec = temp_rec
                closest_so_far = temp_rec.t
        
        return rec
    
