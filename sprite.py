import turtle
import time

class AvatarController:
    def __init__(self, avatar_gif, cooldown_time):
        self.screen = turtle.Screen()
        self.screen.title("Turtle Avatar Control")
        self.screen.bgcolor("white")
        
        # Cooldown settings
        self.cooldown_time = cooldown_time
        self.last_call_time = 0

        # Load the GIF shape
        self.screen.addshape(avatar_gif)

        # Initialize avatar and arrow
        self.avatar = turtle.Turtle()
        self.avatar.shape(avatar_gif)
        self.avatar.penup()

        self.arrow = turtle.Turtle()
        self.arrow.shape("arrow")
        self.arrow.color("red")
        self.arrow.penup()

        self.avatar.setheading(90)
        self.arrow.setheading(90)
        self.cooldown_time = cooldown_time
        self.last_attack_time = 0
        self.bind_keys()

    def bind_keys(self):
        """Bind keys to movement and attack functions."""
        self.screen.listen()
        self.screen.onkeypress(self.move_forward, "w")
        self.screen.onkeypress(self.move_backward, "s")
        self.screen.onkeypress(self.turn_left, "a")
        self.screen.onkeypress(self.turn_right, "d")
        self.screen.onkeypress(self.attack, "e")

    def move_forward(self):
        """Move forward."""
        self.arrow.forward(20)
        self.avatar.goto(self.arrow.pos())

    def move_backward(self):
        """Move backward."""
        self.arrow.backward(20)
        self.avatar.goto(self.arrow.pos())

    def turn_left(self):
        """Turn left."""
        self.arrow.left(20)
        self.avatar.setheading(self.arrow.heading())

    def turn_right(self):
        """Turn right."""
        self.arrow.right(20)
        self.avatar.setheading(self.arrow.heading())


    def attack(self, callback=None):
        """Perform the attack action with an optional callback."""
        current_time = time.time()
        if current_time - self.last_attack_time >= self.cooldown_time:
            self.last_attack_time = current_time
            print("Avatar performed attack!")

            # Smooth forward animation
            for _ in range(10):  # Break the forward movement into 20 small steps
                self.avatar.forward(10)  # Move a small distance
                self.screen.update()  # Update the screen
                time.sleep(0.01)# Pause briefly for smooth animation

            # Smooth backward animation
            for _ in range(10):
                self.avatar.backward(10)  # Move a small distance
                self.screen.update()  # Update the screen
                time.sleep(0.01)
  # Pause briefly for smooth animation

            if callback:
                callback()
        else:
            print("Attack on cooldown!")
        self.avatar.setheading(self.arrow.heading())

    def blink(self, screen):
        """Make the avatar appear and disappear for a blinking effect."""
        for _ in range(3):  # Blink 3 times
            self.avatar.hideturtle()  # Hide the avatar
            screen.update()  # Refresh the screen
            time.sleep(0.25)  # Wait 0.25 seconds
            self.avatar.showturtle()  # Show the avatar again
            screen.update()  # Refresh the screen
            time.sleep(0.25)  # Wait 0.25 seconds

    def run(self):
        """Keep the screen running."""
        self.screen.mainloop()


# Main execution
if __name__ == "__main__":
    avatar_gif = "pics/hutao.gif"  # Path to your GIF
    cooldown_time = 3  # Cooldown period in seconds
    avatar_controller = AvatarController(avatar_gif, cooldown_time)
    avatar_controller.run()

