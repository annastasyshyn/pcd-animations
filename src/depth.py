from manim import *
import numpy as np

class DepthSensorSphere(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)

        sphere = Sphere(radius=2, color=BLUE).set_opacity(0.5)
        sensor_point = np.array([5, 0, 0])
        sensor = Dot3D(point=sensor_point, color=RED)

        self.add(sphere, sensor)

        horizontal_steps = 40
        vertical_layers = 8
        horizontal_range = (-PI/3, PI/3)
        vertical_range = (-PI/6, PI/6)

        for phi in np.linspace(*vertical_range, vertical_layers):
            rays_layer = VGroup()
            points_layer = VGroup()

            for theta in np.linspace(*horizontal_range, horizontal_steps):
                x = 2 * np.cos(phi) * np.cos(theta)
                y = 2 * np.cos(phi) * np.sin(theta)
                z = 2 * np.sin(phi)
                P = np.array([x, y, z])

                ray = Line3D(start=sensor_point, end=P, stroke_width=1)
                hit = Dot3D(point=P, color=GREEN, radius=0.05)

                rays_layer.add(ray)
                points_layer.add(hit)

            self.play(Create(rays_layer), run_time=1)
            self.play(FadeIn(points_layer), run_time=0.5)
            self.play(FadeOut(rays_layer), run_time=0.5)

        self.wait(2)
