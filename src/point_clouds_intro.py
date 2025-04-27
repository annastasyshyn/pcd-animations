from manim import *

class PointCloudsIntroScene(Scene):
    def construct(self):
        title = Text("Data, tests and metrics", font_size=56)
        title.move_to(ORIGIN)
        
        self.play(FadeIn(title), run_time=1)
        self.wait(1)
        
        # self.play(
        #     title.animate.scale(0.6).shift(UP * 3),
        #     run_time=1.5
        # )
        # self.wait(0.5)
        
        self.play(FadeOut(title), run_time=1)
        self.wait(1)