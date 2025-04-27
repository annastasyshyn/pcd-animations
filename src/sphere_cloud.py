from manim import *
import numpy as np

class SpherePointCloud(ThreeDScene):
    def create_point_cloud(self, n_points=2000, radius=1.0):
        points = []
        for _ in range(n_points):
            u = np.random.rand()
            v = np.random.rand()
            theta = 2 * np.pi * u
            phi = np.arccos(2 * v - 1)
            x = radius * np.sin(phi) * np.cos(theta)
            y = radius * np.sin(phi) * np.sin(theta)
            z = radius * np.cos(phi)
            points.append(np.array([x, y, z]))
        return points

    def construct(self):
        num_points = 2000
        sphere_radius = 2.0

        final_positions = self.create_point_cloud(num_points, radius=sphere_radius)
        initial_positions = [np.random.uniform(-6, 6, 3) for _ in range(num_points)]

        dots = VGroup(*[
            Dot3D(point=initial_positions[i], radius=0.03, color=BLUE)
            for i in range(num_points)
        ])
        self.add(dots)

        self.play(*[
            dot.animate.move_to(final_positions[i])
            for i, dot in enumerate(dots)
        ], run_time=4)

        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, run_time=1.5)

        self.play(Rotate(dots, angle=2 * PI, axis=UP), run_time=4)
        self.wait()
