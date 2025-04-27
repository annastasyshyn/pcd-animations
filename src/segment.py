from manim import *
import random
import numpy as np

class PointSegmentation(Scene):
    def construct(self):
        random.seed(42)
        np.random.seed(42)

        distance_threshold = 0.5
        min_points = 5
        step = 0.2

        points = [np.array([random.uniform(-3, 3), random.uniform(-3, 3), 0]) for _ in range(50)]
        points_mobs = [Dot(point, color=WHITE) for point in points]
        self.play(*[FadeIn(dot) for dot in points_mobs])
        self.wait(2)

        assigned = set()
        colors = [RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, PINK, TEAL]

        color_idx = 0

        while len(assigned) < len(points):
            unassigned = [i for i in range(len(points)) if i not in assigned]
            if not unassigned:
                break
            idx = random.choice(unassigned)
            center = points[idx]

            radius = distance_threshold
            circle = None

            while True:
                nearby = [i for i, p in enumerate(points)
                          if np.linalg.norm(p - center) <= radius and i not in assigned]

                if circle:
                    self.remove(circle)
                circle = Circle(radius=radius, color=colors[color_idx % len(colors)])
                circle.move_to(center)
                self.add(circle)

                self.wait(0.7)

                if len(nearby) >= min_points:
                    for i in nearby:
                        points_mobs[i].set_color(colors[color_idx % len(colors)])
                        assigned.add(i)
                    self.play(FadeOut(circle))
                    color_idx += 1
                    break
                else:
                    radius += step

        self.wait(2)
