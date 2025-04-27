from manim import *

import numpy as np

class FFT2DAnimation(Scene):
    def construct(self):
        grid_size = 5
        input_data = np.random.rand(grid_size, grid_size)
        
        input_matrix = self.create_matrix(input_data, title="Input Grid")
        self.play(FadeIn(input_matrix))
        self.wait(2)
        
        row_fft_data = np.fft.fft(input_data, axis=1)
        row_fft_matrix = self.create_matrix(np.abs(row_fft_data), title="After Row-wise FFT")
        self.play(Transform(input_matrix, row_fft_matrix))
        self.wait(2)

        col_fft_data = np.fft.fft(row_fft_data, axis=0)
        final_fft_matrix = self.create_matrix(np.abs(col_fft_data), title="Final 2D FFT Output")
        self.play(Transform(input_matrix, final_fft_matrix))
        self.wait(3)
        
    def create_matrix(self, data, title=""):
        mobject_matrix = Matrix(
            [[f"{val:.2f}" for val in row] for row in data],
            h_buff=0.8,
            v_buff=0.6
        )
        title_text = Text(title).scale(0.7).next_to(mobject_matrix, UP)
        group = VGroup(title_text, mobject_matrix).arrange(DOWN)
        return group
