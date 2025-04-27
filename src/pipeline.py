from manim import *
import numpy as np

class HemispherePointCloudScene(ThreeDScene):
    def construct(self):
        np.random.seed(42)
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        num_points = 400
        noise_std = 0.02
        theta = np.random.uniform(0, 2 * np.pi, num_points)
        phi = np.random.uniform(0, np.pi / 2, num_points)
        x = np.cos(theta) * np.sin(phi) + np.random.normal(0, noise_std, num_points)
        y = np.sin(theta) * np.sin(phi) + np.random.normal(0, noise_std, num_points)
        z = np.cos(phi) + np.random.normal(0, noise_std, num_points)

        points = np.stack((x, y, z), axis=-1)

        dots = VGroup(*[
            Dot3D(point, radius=0.03, color=BLUE)
            for point in points
        ])

        self.play(FadeIn(dots, lag_ratio=0.01, run_time=2))
        
        self.wait(3)
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=2, run_time=2)

