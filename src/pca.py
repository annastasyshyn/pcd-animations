from manim import *
import numpy as np


class PCAPowerIteration(Scene):
    def construct(self):
        np.random.seed(0)
        mean = np.array([0, 0])
        cov = np.array([[3, 2], [2, 2]])  # correlated features
        n_points = 300
        samples = np.random.multivariate_normal(mean, cov, n_points)

        axes = Axes(
            x_range=[-8, 8, 2],
            y_range=[-8, 8, 2],
            x_length=7,
            y_length=7,
            tips=False,
        ).shift(DOWN * 0.5)

        dots = VGroup(
            *[Dot(axes.coords_to_point(x, y), radius=0.04, color=BLUE) for x, y in samples]
        )

        self.play(Create(axes, run_time=1), FadeIn(dots, lag_ratio=0.01, run_time=1))
        self.wait(0.5)

        def power_iteration(mat, v0, steps=6):
            v = v0 / np.linalg.norm(v0)
            vectors = [v.copy()]
            for _ in range(steps):
                v = mat @ v
                v = v / np.linalg.norm(v)
                vectors.append(v.copy())
            return vectors

        cov_matrix = np.cov(samples, rowvar=False)
        v0 = np.random.randn(2)
        vecs_pc1 = power_iteration(cov_matrix, v0, steps=6)


        arrows = VGroup()
        labels = VGroup()
        
        for i, v in enumerate(vecs_pc1[1:]):
            arrow = Arrow(
                start=axes.coords_to_point(0, 0),
                end=axes.coords_to_point(*(3 * v)),
                buff=0,
                color=YELLOW,
                stroke_width=8,
            )
            
            offset = RIGHT if v[0] > 0 else LEFT
            label = MathTex(f"v_{{{i+1}}}").scale(0.7).next_to(arrow.get_end(), offset)
            
            arrows.add(arrow)
            labels.add(label)

        self.play(GrowArrow(arrows[0]), FadeIn(labels[0]))
        self.wait(0.3)
        
        current_arrow = arrows[0].copy()
        current_label = labels[0].copy()
        self.add(current_arrow, current_label)
        self.remove(arrows[0], labels[0])
        
        for i in range(1, len(arrows)):
            next_arrow = arrows[i].copy()
            next_label = labels[i].copy()
            
            self.play(
                Transform(current_arrow, next_arrow),
                FadeOut(current_label),
                FadeIn(next_label),
                run_time=0.8
            )
            
            current_label = next_label
            self.wait(0.1)
            
        pc1_arrow = current_arrow
        pc1_vector = vecs_pc1[-1]


        self.play(pc1_arrow.animate.set_color(RED))
        pc1_label = Text("PC1", font_size=28, color=RED).next_to(pc1_arrow.get_end(), UP)
        self.play(FadeOut(current_label), FadeIn(pc1_label))
        self.wait(0.5)

        eigval1 = float(pc1_vector.T @ cov_matrix @ pc1_vector)
        deflated = cov_matrix - eigval1 * np.outer(pc1_vector, pc1_vector)
        v0_2 = np.random.randn(2)
        vecs_pc2 = power_iteration(deflated, v0_2, steps=6)

        arrows_pc2 = VGroup()
        labels_pc2 = VGroup()
        
        for i, v in enumerate(vecs_pc2[1:]):
            arrow = Arrow(
                start=axes.coords_to_point(0, 0),
                end=axes.coords_to_point(*(3 * v)),
                buff=0,
                color=TEAL,
                stroke_width=8,
            )
            
            offset = LEFT if v[0] > 0 else RIGHT
            label = MathTex(f"w_{{{i+1}}}").scale(0.7).next_to(arrow.get_end(), offset)
            
            arrows_pc2.add(arrow)
            labels_pc2.add(label)

        self.play(GrowArrow(arrows_pc2[0]), FadeIn(labels_pc2[0]))
        
        current_arrow_pc2 = arrows_pc2[0].copy()
        current_label_pc2 = labels_pc2[0].copy()
        self.add(current_arrow_pc2, current_label_pc2)
        self.remove(arrows_pc2[0], labels_pc2[0])
        
        for i in range(1, len(arrows_pc2)):
            next_arrow = arrows_pc2[i].copy()
            next_label = labels_pc2[i].copy()
            
            self.play(
                Transform(current_arrow_pc2, next_arrow),
                FadeOut(current_label_pc2),
                FadeIn(next_label),
                run_time=0.6
            )
            
            current_label_pc2 = next_label
            
        pc2_arrow = current_arrow_pc2
        
        self.play(pc2_arrow.animate.set_color(GREEN))
        pc2_label = Text("PC2", font_size=28, color=GREEN).next_to(pc2_arrow.get_end(), DOWN)
        self.play(FadeOut(current_label_pc2), FadeIn(pc2_label))
        self.wait(2)
