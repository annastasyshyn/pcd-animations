from manim import *
import numpy as np

class PointCloud3DScene(ThreeDScene):
    def construct(self):
        num_points = 200
        points = np.random.uniform(-3, 3, (num_points, 3))

        dots = VGroup(*[
            Dot3D(
                point=np.array([x, y, z]),
                radius=0.05,
                color=BLUE
            ) for x, y, z in points
        ])

        self.add(dots)

        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)

        self.wait(1)

        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[-4, 4, 1],
            axis_config={
                "stroke_width": 2,
                "stroke_color": WHITE
            }
        )

        self.play(Create(axes), run_time=2)

        labels = VGroup(
            axes.get_x_axis_label("x"),
            axes.get_y_axis_label("y"),
            axes.get_z_axis_label("z")
        )
        self.play(Write(labels))

        self.begin_3dillusion_camera_rotation(rate=0.1)
        self.wait(4)
        self.stop_3dillusion_camera_rotation()
