from utils import Color, Point3
from materials import Metal, Lambertian, Dielectric
from hittable import HittableList, Sphere
from camera import Camera

from PIL import Image


def main():
    material_left = Dielectric(1.5)
    material_bubble = Dielectric(1/1.5)
    material_right = Metal(Color(0.8, 0.6, 0.2), 1)
    material_center = Lambertian(Color(0.1, 0.2, 0.5))
    material_ground = Lambertian(Color(0.8, 0.8, 0.0))
    
    world = HittableList()
    world.add(Sphere(Point3(-1, 0, -1), 0.5, material_left))
    world.add(Sphere(Point3(-1, 0, -1), 0.4, material_bubble))
    world.add(Sphere(Point3(1, 0, -1), 0.5, material_right))
    world.add(Sphere(Point3(0, 0, -1.2), 0.5, material_center))
    world.add(Sphere(Point3(0, -100.5, -1), 100, material_ground))

    cam = Camera()
    cam.aspect_ration = 16 / 9
    cam.image_width = 400
    cam.samples_per_pixel = 100
    cam.max_depth = 50

    im = cam.render(world)

    im.save("output.png")
    im.show()


if __name__ == "__main__":
    main()
