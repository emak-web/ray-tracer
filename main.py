from utils import Color, Point3, Metal, Lambertian
from hittable import HittableList, Sphere
from camera import Camera
from PIL import Image


def main():
    world = HittableList()
    world.add(Sphere(Point3(-1, 0, -1), 0.5, Metal(Color(0.8, 0.8, 0.8))))
    world.add(Sphere(Point3(1, 0, -1), 0.5, Metal(Color(0.8, 0.6, 0.2))))
    world.add(Sphere(Point3(0, 0, -1.2), 0.5, Lambertian(Color(0.1, 0.2, 0.5))))
    world.add(Sphere(Point3(0, -100.5, -1), 100, Lambertian(Color(0.8, 0.8, 0.0))))

    cam = Camera()
    cam.aspect_ration = 16 / 9
    cam.image_width = 600
    cam.samples_per_pixel = 10

    im = cam.render(world)

    im.save("output.png")
    im.show()


if __name__ == "__main__":
    main()
