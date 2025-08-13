from manim import *  # noqa: F403

class CreateCircleAndText(Scene):
    def construct(self):
        # Create a circle
        circle = Circle()
        
        # Create some text
        text = Text("Hello, Visium")

        # Show the circle appearing
        self.play(Create(circle))
        
        # Show the text being written
        self.play(Write(text))

        # Wait for 2 seconds
        self.wait(2)