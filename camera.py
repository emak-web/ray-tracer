from PIL import Image
from utils import Color, Ray, Point3, Vec3, unit_vector, random_on_hemisphere, random_unit_vector, linear_to_gamma
from hittable import Hittable, HittableList, Sphere, Interval
import math
import random
import numbers


class Camera:
    def __init__(self):
        self.aspect_ration = 16 / 9
        self.image_width = 400
        self.samples_per_pixel = 10
        self.max_depth = 10

    def initalize(self):
        self.image_height = int(self.image_width/self.aspect_ration)
        self.image_height = self.image_height if self.image_height > 1 else 1

        self.pixel_samples_scale = 1 / self.samples_per_pixel

        self.focal_length = 1
        self.viewport_height = 2
        self.viewport_width = self.viewport_height*self.image_width/self.image_height
        self.camera_center = Point3(0, 0, 0)

        self.viewport_u = Vec3(self.viewport_width, 0, 0)
        self.viewport_v = Vec3(0, -self.viewport_height, 0)

        self.pixel_delta_u = self.viewport_u / self.image_width
        self.pixel_delta_v = self.viewport_v / self.image_height

        self.viewport_upper_left = self.camera_center - Vec3(0, 0, self.focal_length) - self.viewport_u/2 - self.viewport_v/2
        self.pixel00_loc = self.viewport_upper_left + 0.5 * (self.pixel_delta_u + self.pixel_delta_v)

    def render(self, world: Hittable):
        self.initalize()
        im = Image.new("RGB", (self.image_width, self.image_height))

        pixels = im.load()

        for y in range(self.image_height):
            print(f'{y}/{self.image_height-1}')
            for x in range(self.image_width):
                pixel_color = Color(0, 0, 0)
                for sample in range(self.samples_per_pixel):
                    r = self.get_ray(x, y)
                    pixel_color += self.ray_color(r, self.max_depth, world)

                
                intensity = Interval(0.000, 0.999)
                pixel_color *= self.pixel_samples_scale
                r, g, b = linear_to_gamma(pixel_color.x), linear_to_gamma(pixel_color.y), linear_to_gamma(pixel_color.z)
                pixels[x, y] = (int(255.999*intensity.clamp(r)), int(255.999*intensity.clamp(g)), int(255.999*intensity.clamp(b)))

        return im

    def ray_color(self, r: Ray, depth: int, world: Hittable) -> Color:
        if depth <= 0:
            return Color(0, 0, 0)

        rec = world.hit(r, Interval(0.001, math.inf))
        if rec is not None:
            # return 0.5 * (rec.normal + Color(1,1,1))
            # direction = random_on_hemisphere(rec.normal)
            # direction = rec.normal + random_unit_vector()
            attenuation, scattered = rec.mat.scatter(r, rec)
            return attenuation * self.ray_color(scattered, depth-1, world)
            
            # return Color(0, 0, 0)
        
        unit_direction = unit_vector(r.direction)
        a = 0.5 * (unit_direction.y+1)
        return (1 - a) * Color(1, 1, 1) + a * Color(0.5, 0.7, 1)

    def get_ray(self, i, j):
        offset = self.sample_square()
        pixel_center = self.pixel00_loc + (i + offset.x)*self.pixel_delta_u + (j + offset.y)*self.pixel_delta_v
        ray_direction = pixel_center - self.camera_center

        return Ray(self.camera_center, ray_direction)

    def sample_square(self):
        return Vec3(random.random() - 0.5, random.random() - 0.5, 0)

