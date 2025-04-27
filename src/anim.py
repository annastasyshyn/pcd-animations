from __future__ import annotations
from manim import *
import numpy as np
import random

def sample_sphere_points(n: int = 1000, radius: float = 2.0) -> np.ndarray:
    phi = np.arccos(1.0 - 2.0 * np.random.rand(n))
    theta = TAU * np.random.rand(n)
    x = radius * np.sin(phi) * np.cos(theta)
    y = radius * np.sin(phi) * np.sin(theta)
    z = radius * np.cos(phi)
    return np.column_stack([x, y, z])


def make_point_cloud(points: np.ndarray, radius: float = 0.03, colour=YELLOW) -> VGroup:
    return VGroup(*[Dot3D(p, radius=radius, color=colour) for p in points])

class ReconstructionScene(ThreeDScene):

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)

        # Ground‑truth sphere
        sphere = Sphere(radius=2, resolution=(24, 48), fill_opacity=0.15, stroke_opacity=0.4)
        self.add(sphere)

        # Place several cameras (blue cubes)
        cam_icons = VGroup()
        n_cams = 6
        for k in range(n_cams):
            ang = TAU * k / n_cams
            pos = 4 * np.array([np.cos(ang), np.sin(ang), 0.6])
            cam = Cube(side_length=0.35, fill_color=BLUE_E, fill_opacity=0.9, stroke_width=0).move_to(pos)
            cam.rotate(-ang + PI / 2, axis=OUT)
            cam_icons.add(cam)
        self.play(LaggedStartMap(FadeIn, cam_icons, lag_ratio=0.15))
        self.wait(0.2)

        rays = VGroup()
        # main_cam = cam_icons[0]
        # key_pts = sample_sphere_points(5)  # simulate detected key‑points
        # for p in key_pts:
        #     rays.add(DashedLine(main_cam.get_center(), p, dash_length=0.06))
        for other_cam in cam_icons[1:]:
            for p in sample_sphere_points(5):
                rays.add(DashedLine(other_cam.get_center(), p, dash_length=0.06))
            # rays.add(DashedLine(other_cam.get_center(), ORIGIN, dash_length=0.12))
        self.play(LaggedStartMap(Create, rays, lag_ratio=0.02, run_time=3))
        self.wait(0.3)

        dots = make_point_cloud(sample_sphere_points(1200))
        self.play(LaggedStartMap(GrowFromCenter, dots, lag_ratio=0.005, run_time=3))
        self.wait(2)

class NoiseScene(ThreeDScene):

    def construct(self):
        # self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)

        # title = Text("Noisy vs. Clean Point Cloud", font_size=48)
        # self.play(Write(title))
        # self.play(title.animate.to_edge(UP))

        clean_pts = sample_sphere_points(1000)
        clean_cloud = make_point_cloud(clean_pts, colour=GREEN)
        fresh_cloud = clean_cloud.copy()
        self.add(clean_cloud)
        self.wait(1)

        noisy_pts = clean_pts + 0.3 * (np.random.rand(*clean_pts.shape) - 0.5)
        very_noisy_pts = clean_pts + 0.8 * (np.random.rand(*clean_pts.shape) - 0.5)
        noisy_cloud = make_point_cloud(noisy_pts, colour=RED)
        very_noisy_cloud = make_point_cloud(very_noisy_pts, colour=RED)

        self.play(Transform(clean_cloud, noisy_cloud, run_time=3))
        self.wait(2)
        self.play(Transform(clean_cloud, very_noisy_cloud, run_time=3))
        self.wait(3)
        self.play(Transform(clean_cloud, fresh_cloud, run_time=3))
        self.play(FadeOut(clean_cloud))
        self.wait()

class FFTScene(Scene):

    GRID_N = 16

    def construct(self):
        title = Text("FFT Denoising Pipeline", font_size=48)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        grid = self._colour_grid(noisy=True)
        self.play(FadeIn(grid))
        self.wait(0.4)

        brace = Brace(grid, DOWN)
        lbl = Text("Split into patches", font_size=32)
        self.play(GrowFromCenter(brace), Write(lbl.next_to(brace, DOWN)))
        self.wait(0.6)
        self.play(FadeOut(brace), FadeOut(lbl))

        freq_grid = self._colour_grid(noisy=False, freq=True)
        fft_lbl = Text("2D FFT", font_size=32).next_to(grid, RIGHT)
        self.play(Transform(grid, freq_grid), Write(fft_lbl))
        self.wait(0.6)

        mask = self._low_pass_mask()
        self.play(FadeIn(mask))
        self.wait(0.6)

        clean_grid = self._colour_grid(noisy=False)
        self.play(FadeOut(mask), Transform(grid, clean_grid), FadeOut(fft_lbl))
        self.wait(2)

    def _colour_grid(self, noisy: bool, freq: bool = False):
        N = self.GRID_N
        squares = VGroup()
        for i in range(N):
            for j in range(N):
                x, y = i - N / 2, j - N / 2
                r = np.hypot(x, y)
                val = np.cos(r / 2)
                if noisy:
                    val += 0.4 * random.uniform(-1, 1)
                if freq:
                    val = np.exp(-0.08 * r ** 2)
                colour = color_gradient([BLUE, GREEN, YELLOW, RED], 32)[int((val + 1) * 15.5)]
                sq = Square(0.4, fill_color=colour, fill_opacity=0.95, stroke_width=0)
                sq.move_to(np.array([(i - N / 2) * 0.4, (j - N / 2) * 0.4, 0]))
                squares.add(sq)
        return squares

    def _low_pass_mask(self):
        N = self.GRID_N
        R = 3
        mask = VGroup()
        for i in range(N):
            for j in range(N):
                if np.hypot(i - N / 2, j - N / 2) > R:
                    sq = Square(0.4, fill_color=BLACK, fill_opacity=0.8, stroke_width=0)
                    sq.move_to(np.array([(i - N / 2) * 0.4, (j - N / 2) * 0.4, 0]))
                    mask.add(sq)
        return mask

class LeastSquaresScene(ThreeDScene):

    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)

        title = Text("Least Squares Patch Fit", font_size=48)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # Select only a small patch of the sphere (simulate local window)
        all_pts = sample_sphere_points(1200)
        patch = all_pts[(all_pts[:, 2] > 0.5) & (all_pts[:, 0] > 0)]  # quarter‑hemisphere patch
        patch[:, 2] += 0.4 * (np.random.rand(len(patch)) - 0.5)       # add noise
        cloud = make_point_cloud(patch, colour=RED)
        self.add(cloud)
        self.wait(0.4)

        X, Y = patch[:, 0], patch[:, 1]
        A = np.column_stack([X**2, Y**2, X * Y, X, Y, np.ones_like(X)])
        coeffs, *_ = np.linalg.lstsq(A, patch[:, 2], rcond=None)

        def quad(u, v):
            a1, a2, a3, a4, a5, a6 = coeffs
            return np.array([u, v, a1*u**2 + a2*v**2 + a3*u*v + a4*u + a5*v + a6])

        surf = Surface(lambda u, v: quad(u, v), u_range=[0, 1.6], v_range=[0, 1.6],
                       resolution=(24, 24), fill_color=GREEN, fill_opacity=0.6,
                       stroke_width=0.5, stroke_color=GREEN_D)
        self.play(Create(surf, run_time=3))
        self.wait(0.4)

        dists = np.abs(patch[:, 2] - (A @ coeffs))
        thr = np.percentile(dists, 70)
        good = patch[dists < thr]
        bad  = patch[dists >= thr]
        good_cloud = make_point_cloud(good, colour=YELLOW)
        bad_cloud  = make_point_cloud(bad, colour=RED)
        self.play(Transform(cloud, bad_cloud))
        self.play(FadeOut(cloud), FadeIn(good_cloud))
        self.wait(2)
