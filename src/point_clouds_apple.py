from manim import *
import numpy as np

class ApplePointCloud(Scene):
    def create_point_cloud(self, n_points=5000):
        def apple(u, v):
            x = 0.5 * np.sin(u) * (1 + 0.2 * np.cos(v)) * (1 + 0.1 * np.cos(2 * u))
            y = 0.5 * np.cos(u) * (1 + 0.2 * np.cos(v)) * (1 + 0.1 * np.cos(2 * u))
            z = 0.5 * np.sin(v) + 0.1 * np.cos(3 * u)
            return np.array([x, y, z])
        
        points = []
        for _ in range(n_points):
            u = np.random.uniform(0, 2 * np.pi)
            v = np.random.uniform(-np.pi / 2, np.pi / 2)
            pt = apple(u, v)
            points.append(pt)
        return points

    def construct(self):
        num_points = 2000
        final_positions = self.create_point_cloud(num_points)
        initial_positions = [np.random.uniform(-6, 6, 3) for _ in range(num_points)]

        dots = VGroup(*[
            Dot3D(point=initial_positions[i], radius=0.03, color=RED)
            for i in range(num_points)
        ])
        self.add(dots)

        self.play(*[
            dot.animate.move_to(final_positions[i])
            for i, dot in enumerate(dots)
        ], run_time=4)

        self.play(Rotate(dots, angle=2 * PI, axis=UP), run_time=4)
        self.wait()
