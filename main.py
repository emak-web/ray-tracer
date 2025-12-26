from utils import Color, Ray, Point3, Vec3, unit_vector, random_unit_vector
from hittable import Hittable, HittableList, Sphere, Interval
from camera import Camera
from PIL import Image


def main():
    world = HittableList()
    world.add(Sphere(Point3(0, 0, -1), 0.5))
    world.add(Sphere(Point3(0, -100.5, -1), 100))

    cam = Camera()
    cam.aspect_ration = 16 / 9
    cam.image_width = 600
    cam.samples_per_pixel = 10

    im = cam.render(world)

    im.save("output.png")
    im.show()


if __name__ == "__main__":
    main()
