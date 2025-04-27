from manim import *
import random
import numpy as np

class DenoisingMethods(Scene):
    def construct(self):
        # title = Text("How can point clouds be denoised?", font_size=72, color=WHITE)
        # self.play(Write(title))
        # self.play(title.animate.scale(0.5).to_edge(UP), run_time=3)
        # self.wait(1)
        # self.play(FadeOut(title), FadeOut(title), run_time=2)

        labels_y_position = DOWN * 3

        layer_sizes = [4, 5, 5, 2]
        nn_layers = VGroup()
        for i, size in enumerate(layer_sizes):
            layer = VGroup(*[Circle(radius=0.2, color=WHITE) for _ in range(size)])
            layer.arrange(DOWN, buff=0.5).shift(RIGHT * (i - 1.5) * 3)
            nn_layers.add(layer)
        nn_edges = VGroup(*[
            Line(start.get_center(), end.get_center(), color=GRAY)
            for layer1, layer2 in zip(nn_layers, nn_layers[1:])
            for start in layer1 for end in layer2
        ])
        nn_group = VGroup(nn_edges, nn_layers)
        nn_group.shift(UP * 1)
        nn_label = Text("Neural Networks", font_size=48, color=WHITE).move_to(labels_y_position)
        self.play(Create(nn_group), FadeIn(nn_label), run_time=4)
        self.wait(2)

        self.play(FadeOut(nn_group), FadeOut(nn_label), run_time=2)
        import networkx as nx
        G = nx.erdos_renyi_graph(8, 0.4)
        positions = {node: np.array([
            3 * np.cos(2 * np.pi * i / len(G.nodes())),
            3 * np.sin(2 * np.pi * i / len(G.nodes())), 0
        ]) for i, node in enumerate(G.nodes())}
        graph_nodes = VGroup(*[
            Dot(pos, radius=0.15, color=BLUE) for pos in positions.values()
        ])
        graph_edges = VGroup(*[
            Line(positions[u], positions[v], color=GRAY) for u, v in G.edges()
        ])
        graph_group = VGroup(graph_edges, graph_nodes)
        graph_group.shift(UP * 1)
        graph_label = Text("Graph-based Methods", font_size=48, color=WHITE).move_to(labels_y_position)
        self.play(Create(graph_group), FadeIn(graph_label), run_time=4)
        self.wait(2)

        self.play(FadeOut(graph_group), FadeOut(graph_label), run_time=2)

        plane = NumberPlane(
            x_range=[-4, 4, 1], y_range=[-3, 3, 1],
            background_line_style={"stroke_color": GRAY, "stroke_opacity": 0.3}
        ).shift(UP * 1)
        axes = VGroup(
            Arrow(plane.coords_to_point(-4, 0), plane.coords_to_point(4, 0), buff=0, color=WHITE),
            Arrow(plane.coords_to_point(0, -2.5), plane.coords_to_point(0, 2.5), buff=0, color=WHITE)
        )
        x_label = Text("X", font_size=24, color=WHITE).next_to(axes[0].get_end(), RIGHT)
        y_label = Text("Y", font_size=24, color=WHITE).next_to(axes[1].get_end(), UP)
        self.play(Create(plane), Create(axes), Write(x_label), Write(y_label), run_time=3)

        points = VGroup(*[
            Dot(
                plane.coords_to_point(
                    random.uniform(-3, 3), random.uniform(-0.5, 2)
                ), radius=0.05, color=LIGHT_GRAY
            ) for _ in range(50)
        ])
        self.play(LaggedStartMap(FadeIn, points, shift=DOWN), run_time=4)

        direction = np.array([np.cos(PI/6), np.sin(PI/6), 0])
        pca_line = DashedVMobject(
            Line(
                plane.coords_to_point(-4 * direction[0], -4 * direction[1]),
                plane.coords_to_point(4 * direction[0], 4 * direction[1])
            ), num_dashes=20, dashed_ratio=0.5, color=RED
        )
        arrow1 = Arrow(plane.coords_to_point(0, 0), plane.coords_to_point(3 * direction[0], 3 * direction[1]), buff=0, stroke_width=6, color=YELLOW)
        orth = np.array([-direction[1], direction[0], 0])
        arrow2 = Arrow(plane.coords_to_point(0, 0), plane.coords_to_point(2 * orth[0], 2 * orth[1]), buff=0, stroke_width=6, color=GREEN)
        label1 = Text("PC1", font_size=32, color=YELLOW).next_to(arrow1.get_end(), UR)
        label2 = Text("PC2", font_size=32, color=GREEN).next_to(arrow2.get_end(), UL)
        pca_group = VGroup(pca_line, arrow1, arrow2, label1, label2)
        self.play(Create(pca_line), run_time=3)
        self.play(Create(arrow1), Create(arrow2), run_time=2)
        self.play(FadeIn(label1), FadeIn(label2), run_time=1)

        # pca_title = Text("Principal Component Analysis", font_size=48, color=WHITE).move_to(labels_y_position)
        # self.play(FadeIn(pca_title), run_time=2)
        # self.wait(3)

        # self.play(
        #     FadeOut(plane), FadeOut(axes), FadeOut(x_label), FadeOut(y_label),
        #     FadeOut(points), FadeOut(pca_group), FadeOut(pca_title), run_time=3
        # )
        self.wait(1)
