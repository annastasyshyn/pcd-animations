from manim import *
import numpy as np
from sklearn.decomposition import PCA

class HemispherePointCloudScene(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        np.random.seed(42)

        num_points = 400
        noise_std = 0.02
        theta = np.random.uniform(0, 2 * np.pi, num_points)
        phi = np.random.uniform(0, np.pi / 2, num_points)
        x = np.cos(theta) * np.sin(phi) + np.random.normal(0, noise_std, num_points)
        y = np.sin(theta) * np.sin(phi) + np.random.normal(0, noise_std, num_points)
        z = np.cos(phi) + np.random.normal(0, noise_std, num_points)

        points = np.stack((x, y, z), axis=-1)

        patches = []
        colors = [BLUE, GREEN, RED, YELLOW]
        centers = [
            np.array([0.5, 0, 0.7]),
            np.array([-0.5, 0.5, 0.5]),
            np.array([-0.5, -0.5, 0.5]),
            np.array([0, 0, 1.0])
        ]

        for center in centers:
            distances = np.linalg.norm(points - center, axis=1)
            patches.append(distances)

        patches = np.stack(patches, axis=1)
        patch_indices = np.argmin(patches, axis=1)

        initial_color = GREY
        dots = VGroup()
        for i, point in enumerate(points):
            radius = 0.045 if patch_indices[i] == 0 else 0.03  # Make one cloud larger
            dot = Dot3D(point, radius=radius, color=initial_color)
            dots.add(dot)

        self.add(dots)

        self.move_camera(zoom=2, run_time=2)

        animations = []
        for i, dot in enumerate(dots):
            animations.append(dot.animate.set_color(colors[patch_indices[i]]))

        self.play(*animations, run_time=2)

        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        
        self.stop_ambient_camera_rotation()
        
        animations = []
        blue_dots = VGroup()
        
        for i, dot in enumerate(dots):
            if patch_indices[i] != 0:  # If not blue (patch 0)
                animations.append(dot.animate.set_opacity(0))
            else:
                blue_dots.add(dot)
        
        self.play(*animations, run_time=1.5)
        self.wait(1)

        blue_points = np.array([points[i] for i in range(len(points)) if patch_indices[i] == 0])

        pca = PCA(n_components=3)
        pca.fit(blue_points)

        normal_vector = pca.components_[2]

        normal_vector = normal_vector / np.linalg.norm(normal_vector)

        centroid = np.mean(blue_points, axis=0)

        plane_size = 1.5
        plane = Square(side_length=plane_size, color=BLUE_A)
        plane.set_fill(BLUE_A, opacity=0.3)
        plane.set_stroke(BLUE, opacity=0.7, width=1)
        
        x_axis = pca.components_[0]
        y_axis = pca.components_[1]

        rotation_matrix = np.column_stack([x_axis, y_axis, normal_vector])

        plane.move_to(centroid)

        plane.apply_matrix(rotation_matrix[:3, :3])
        
        self.play(FadeIn(plane), run_time=1.5)
        
        arrow_start = centroid
        arrow_end = centroid + normal_vector * 0.8
        normal_arrow = Arrow3D(
            arrow_start, arrow_end,
            color=YELLOW,
            thickness=0.03
        )
        
        self.play(Create(normal_arrow), run_time=1.5)
        
        scale = 0.7
        x_arrow = Arrow3D(
            centroid, centroid + x_axis * scale,
            color=RED,
            thickness=0.02
        )
        y_arrow = Arrow3D(
            centroid, centroid + y_axis * scale,
            color=GREEN,
            thickness=0.02
        )
        
        self.remove(normal_arrow)
        z_arrow = Arrow3D(
            centroid, centroid + normal_vector * scale,
            color=BLUE,
            thickness=0.02
        )
        
        self.play(
            Create(x_arrow),
            Create(y_arrow),
            Create(z_arrow),
            run_time=2
        )
        
        x_label = Text("x", font_size=24).set_color(RED)
        y_label = Text("y", font_size=24).set_color(GREEN)
        z_label = Text("z", font_size=24).set_color(BLUE)

        x_label.move_to(centroid + x_axis * (scale + 0.2))
        y_label.move_to(centroid + y_axis * (scale + 0.2))
        z_label.move_to(centroid + normal_vector * (scale + 0.2))
        
        self.add_fixed_in_frame_mobjects(x_label, y_label, z_label)
        self.play(
            Write(x_label),
            Write(y_label),
            Write(z_label),
            run_time=1.5
        )
        
        self.move_camera(phi=45 * DEGREES, theta=-30 * DEGREES, run_time=3)
        self.wait(3)
