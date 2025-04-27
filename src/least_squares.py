from manim import *
import random, math
import numpy as np

class LeastSquaresSurfaceFitting(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-1, 1, 0.5],
            y_range=[-1, 1, 0.5],
            z_range=[-0.2, 1, 0.5]
        )
        axes.set_opacity(0.3)
        axes.shift(IN * 2)
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)
        self.play(Create(axes), run_time=2)

        title = Text("Least-Squares Surface Fitting", font_size=48).to_corner(UL)
        formula = Text(
            "f(x,y)=a₁ x² + a₂ y² + a₃ xy + a₄ x + a₅ y + a₆",
            font_size=36
        ).to_corner(DL)
        self.add_fixed_in_frame_mobjects(title, formula)

        data = []
        dots = VGroup()
        for _ in range(100):
            theta = random.uniform(0, 2 * math.pi)
            r = math.sqrt(random.uniform(0, 1))
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            z_true = math.sqrt(max(0, 1 - x**2 - y**2))
            z = z_true + random.uniform(-0.05, 0.05)
            data.append((x, y, z))
            point = axes.c2p(x, y, z)
            dot = Dot3D(point=point + IN * 2, radius=0.03, color=RED)
            dot.shift(UP * 3)
            dots.add(dot)
        self.play(*[dot.animate.shift(DOWN * 3) for dot in dots], run_time=4)
        self.wait(0.5)

        X = np.array([[x**2, y**2, x*y, x, y, 1] for x,y,z in data])
        zs = np.array([z for x,y,z in data])
        p, *_ = np.linalg.lstsq(X, zs, rcond=None)

        self.move_camera(phi=60 * DEGREES, theta=-25 * DEGREES, run_time=2)

        surface = Surface(
            lambda u, v: axes.c2p(
                u, v,
                p[0]*u**2 + p[1]*v**2 + p[2]*u*v + p[3]*u + p[4]*v + p[5]
            ) + IN * 2,
            u_range=[-1, 1], v_range=[-1, 1], resolution=(32, 32)
        )
        surface.set_opacity(0)
        self.play(FadeIn(surface), run_time=2)
        self.play(surface.animate.set_opacity(0.7), run_time=2)

        label_surf = Text("Fitted Quadratic Surface", font_size=30).to_corner(DR)
        self.add_fixed_in_frame_mobjects(label_surf)
        self.wait(2)
