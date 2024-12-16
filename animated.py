import turtle
import time


class Animated:
    def __init__(self, screen, frames, x=0, y=0):
        """Initialize the Animated object."""
        self.screen = screen  # Reuse the passed screen instance
        self.frames = frames
        self.turtle = turtle.Turtle()
        self.turtle.penup()
        self.turtle.goto(x, y)
        self.turtle.hideturtle()  # Initially hide the turtle
        self.current_frame = 0
        self.is_running = False

        # Register frames with the screen
        for frame in frames:
            self.screen.addshape(frame)

    def play_animation(self, delay=0.05, loop=False):
        """Start the animation."""
        self.is_running = True
        self.loop = loop
        self.delay = delay
        self.turtle.showturtle()
        print("Starting animation at:", self.turtle.pos())  # Debugging point
        self.animate()

    def animate(self):
        """Perform one step of the animation."""
        if not self.is_running:
            return

        # Set the turtle shape to the current frame
        self.turtle.shape(self.frames[self.current_frame])

        # Advance to the next frame
        self.current_frame += 1

        # Check if the animation is done
        if self.current_frame >= len(self.frames):
            if self.loop:
                self.current_frame = 0  # Loop back to the first frame
            else:
                self.is_running = False
                self.turtle.hideturtle()  # Cleanup: Hide the turtle
                return

        # Schedule the next frame
        self.screen.ontimer(self.animate, int(self.delay * 1000))
