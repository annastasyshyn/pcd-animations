from manim import *
import numpy as np

class DenoiseHemispherePointCloud(ThreeDScene):
    def generate_noisy_hemisphere(self, num_points=200):
        points = []
        for _ in range(num_points):
            theta = np.random.uniform(0, 2 * np.pi)
            phi = np.random.uniform(0, np.pi / 2)
            r = 1 + np.random.normal(0, 0.1)

            x = r * np.sin(phi) * np.cos(theta)
            y = r * np.sin(phi) * np.sin(theta)
            z = r * np.cos(phi)

            points.append(np.array([x, y, z]))
        return points

    def generate_clean_hemisphere(self, noisy_points):
        clean_points = []
        for p in noisy_points:
            norm = np.linalg.norm(p)
            if norm == 0:
                clean_points.append(p)
                continue
            clean_p = p / norm
            if clean_p[2] < 0:
                clean_p[2] *= -1
            clean_points.append(clean_p)
        return clean_points

    def construct(self):
        axes = ThreeDAxes()
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        noisy_points = self.generate_noisy_hemisphere(num_points=200)
        clean_points = self.generate_clean_hemisphere(noisy_points)

        noisy_dots = VGroup(*[
            Dot3D(point, radius=0.03, color=BLUE) for point in noisy_points
        ])
        clean_dots = VGroup(*[
            Dot3D(point, radius=0.03, color=GREEN) for point in clean_points
        ])

        self.add(axes)
        self.add(noisy_dots)
        self.wait(2)

        self.play(
            Transform(noisy_dots, clean_dots),
            run_time=3
        )
        self.wait(2)
