from PIL import Image
from utils import Color, Ray, Point3, Vec3, unit_vector
from hittable import Hittable, HittableList, Sphere, Interval
import math


def ray_color(r: Ray, world: Hittable):
    rec = world.hit(r, Interval(0, math.inf))
    if rec is not None:
        return 0.5 * (rec.normal + Color(1,1,1))
    
    unit_direction = unit_vector(r.direction)
    a = 0.5 * (unit_direction.y+1)
    return (1 - a) * Color(1, 1, 1) + a * Color(0.5, 0.7, 1)


def main():
    aspect_ration = 16 / 9
    image_width = 400
    image_height = int(image_width/aspect_ration)
    image_height = image_height if image_height > 1 else 1

    world = HittableList()
    world.add(Sphere(Point3(0, 0, -1), 0.5))
    world.add(Sphere(Point3(0, -100.5, -1), 100))

    # world.add(Sphere(Point3(-0.5, 0, -1), 0.5))
    # world.add(Sphere(Point3(0.3, 0, -1), 0.5))
    # world.add(Sphere(Point3(0, 0.5, -1), 0.5))
    # world.add(Sphere(Point3(0, 0, -0.3), 0.2))

    focal_length = 1
    viewport_height = 2
    viewport_width = viewport_height*image_width/image_height
    camera_center = Point3(0, 0, 0)

    viewport_u = Vec3(viewport_width, 0, 0)
    viewport_v = Vec3(0, -viewport_height, 0)

    pixel_delta_u = viewport_u / image_width
    pixel_delta_v = viewport_v / image_height

    viewport_upper_left = camera_center - Vec3(0, 0, focal_length) - viewport_u/2 - viewport_v/2
    pixel00_loc = viewport_upper_left + 0.5 * (pixel_delta_u + pixel_delta_v)

    im = Image.new("RGB", (image_width, image_height))

    pixels = im.load()

    for y in range(image_height):
        print(f'{y}/{image_height-1}')
        for x in range(image_width):
            pixel_center = pixel00_loc + x*pixel_delta_u + y*pixel_delta_v
            ray_direction = pixel_center - camera_center
            r = Ray(camera_center, ray_direction)
            c = ray_color(r, world)
            pixels[x, y] = (int(255.999*c.x), int(255.999*c.y), int(255.999*c.z))

    im.show()
    im.save("output.png")


if __name__ == "__main__":
    main()
