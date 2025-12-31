from utils import Color, Point3, Vec3
from materials import Metal, Lambertian, Dielectric
from hittable import HittableList, Sphere
from camera import Camera

import math
import random


def main():
    world = HittableList()

    ground_material = Lambertian(Color(0.5, 0.5, 0.5))
    world.add(Sphere(Point3(0, -1000, 0), 1000, ground_material))

    for a in range(-7, 7):
        for b in range(-7, 7):
            choose_mat = random.random()
            center = Point3(1.2*a + 0.9*random.random(), 0.2, 1.2*b + 0.9*random.random())

            if (center - Point3(4, 0.2, 0)).length() > 0.9:
                sphere_material = None

                if choose_mat < 0.8:
                    # diffuse
                    albedo = Color.random() * Color.random()
                    sphere_material = Lambertian(albedo)
                elif choose_mat < 0.95:
                    # metal
                    albedo = Color.random(0.5, 1)
                    fuzz = random.uniform(0, 0.5)
                    sphere_material = Metal(albedo, fuzz)
                else:
                    # glass
                    sphere_material = Dielectric(1.5)

                world.add(Sphere(center, 0.2, sphere_material))

    material1 = Dielectric(1.5)
    world.add(Sphere(Point3(0, 1, 0), 1, material1))
                
    material2 = Lambertian(Color(0.4, 0.2, 0.1))
    world.add(Sphere(Point3(-4, 1, 0), 1, material2))

    material3 = Metal(Color(0.7, 0.6, 0.5), 0)
    world.add(Sphere(Point3(4, 1, 0), 1, material3))

    cam = Camera()
    cam.aspect_ration = 16 / 9
    cam.image_width = 1200
    cam.samples_per_pixel = 100
    cam.max_depth = 50
    
    cam.vfov = 20
    cam.lookfrom = Point3(13, 2, 3)
    cam.lookat = Point3(0, 0, 0)
    cam.vup = Vec3(0, 1, 0)

    cam.defocus_angle = 0.6
    cam.focus_dist = 10

    im = cam.render(world)

    im.save("output.png")
    im.show()


if __name__ == "__main__":
    main()
