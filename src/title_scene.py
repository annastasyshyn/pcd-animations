from manim import *

class TitleScene(Scene):
    def construct(self):
        title = Text("Point Cloud Denoising", font_size=72)
        
        subtitle = Text("Linear Algebra Semester Project", font_size=36)
        subtitle.next_to(title, DOWN, buff=0.5)
        
        authors = Text("Oleh Basystyi, Maksym Zhuk, Anna Stasyshyn", font_size=24)
        authors.next_to(subtitle, DOWN, buff=0.5)
        
        text_group = VGroup(title, subtitle, authors)
        
        text_group.move_to(ORIGIN)
        
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)
        self.play(Write(subtitle), run_time=1)
        self.wait(0.5)
        self.play(Write(authors), run_time=1)
        
        self.wait(3)