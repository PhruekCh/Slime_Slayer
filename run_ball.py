from sprite import AvatarController
import animated
import ball
import my_event
import turtle
import random
import heapq
import math
import time


class BouncingSimulator:
    def __init__(self, num_balls, initial_speed, avatar_gif, cooldown_time):
        self.num_balls = num_balls
        self.ball_list = []
        self.t = 0.0
        self.pq = []
        self.HZ = 4
        self.collision_count = 0
        self.collision_cooldown = 4
        self.last_collision_time = 0
        self.avatar_radius = 80
        self.is_paused = False
        self.avatar_lives = 3
        self.current_level = 1

        self.start_time = time.time()

        # Screen setup
        self.screen = turtle.Screen()
        self.screen.bgpic("pics/tgc.gif")
        self.screen.tracer(0)
        self.canvas_width = turtle.screensize()[0]
        self.canvas_height = turtle.screensize()[1]
        self.screen.addshape("pics/red_heart.gif")
        self.screen.addshape("pics/black_heart.gif")

        # Initialize the avatar controller
        self.avatar = AvatarController(avatar_gif, cooldown_time)

        self.hearts = []
        for i in range(3):  # Display 3 hearts
            heart = turtle.Turtle()
            heart.penup()
            heart.shape("pics/red_heart.gif")
            heart.goto(self.canvas_width // 2 - 100 *
                       (i + 1), self.canvas_height // 2 + 180)
            self.hearts.append(heart)

        self.update_level_text(self.current_level)
        self.initialize_balls(num_balls, initial_speed)

        # Create balls

    def initialize_balls(self, ball_count=5, initial_speed=0.7):
        """Helper function to initialize balls with given count and speed."""
        ball_radius = 0.05 * self.canvas_width
        self.ball_list = []
        for i in range(ball_count):
            x = random.uniform(-self.canvas_width / 2 +
                               ball_radius, self.canvas_width / 2 - ball_radius)
            y = random.uniform(-self.canvas_height / 2 +
                               ball_radius, self.canvas_height / 2 - ball_radius)
            angle = random.uniform(0, 360)
            vx = initial_speed * math.cos(math.radians(angle))
            vy = initial_speed * math.sin(math.radians(angle))
            gif_path = random.choice(
                ["pics/slime_blue.gif", "pics/slime_red.gif", "pics/slime_green.gif", "pics/slime_purple.gif"])
            self.ball_list.append(
                ball.Ball(ball_radius, x, y, vx, vy, None, len(self.ball_list), gif_path))

    def remove_balls(self):
        """Remove balls within the radius of the avatar when 'E' is pressed."""
        avatar_x, avatar_y = self.avatar.avatar.pos()
        avatar_heading = self.avatar.avatar.heading()
        balls_to_remove = [ball for ball in self.ball_list
                           if self.detect_attack(ball, avatar_x, avatar_y, avatar_heading, attack_range=100, attack_width=100)]

        for ball in balls_to_remove:
            frames = [f"pics/smoke/frame_{i+1}.gif" for i in range(16)]
            animation = animated.Animated(self.screen, frames, ball.x, ball.y)
            animation.play_animation(delay=0.05, loop=False)

            ball.turtle.hideturtle()  # Hide the ball
            self.ball_list.remove(ball)  # Remove from ball list
            print(f"Removed ball at ({ball.x}, {ball.y})")

        # Clear events related to removed balls
            self.clear_removed_ball_events(balls_to_remove)

        # Synchronize updates
        self.screen.update()

        # Check if all balls have been removed
        self.check_game_over()

    def clear_removed_ball_events(self, removed_balls):
        """Remove events related to removed balls from the priority queue."""
        self.pq = [
            event for event in self.pq if event.a not in removed_balls and event.b not in removed_balls]
        heapq.heapify(self.pq)

    def detect_attack(self, ball, x, y, direction, attack_range=100, attack_width=100):
        direction_rad = math.radians(direction)
        # Compute the vector in the direction the avatar is facing
        dx = ball.x - x
        dy = ball.y - y

        # Rotate the ball's position relative to the avatar's heading
        rotated_x = dx * math.cos(-direction_rad) - \
            dy * math.sin(-direction_rad)
        rotated_y = dx * math.sin(-direction_rad) + \
            dy * math.cos(-direction_rad)
        return 0 < rotated_x < attack_range and abs(rotated_y) < attack_width / 2

    def detect_collision(self, ball):
        """Detect collision between the avatar and a ball."""
        avatar_x, avatar_y = self.avatar.avatar.pos()
        distance = math.sqrt((ball.x - avatar_x) ** 2 +
                             (ball.y - avatar_y) ** 2)
        return distance < (ball.size + 20)

    def handle_collision(self, ball):
        """Handle collision with cooldown logic."""
        current_time = time.time()

        if current_time - self.start_time < 3:
            return

        if current_time - self.last_collision_time >= self.collision_cooldown and self.avatar_lives > 0:
            self.collision_count += 1
            self.last_collision_time = current_time
            self.avatar_lives -= 1
            self.hearts[self.avatar_lives].shape(
                "pics/black_heart.gif")  # Update heart display
            print(f"Collision detected! Lives remaining: {self.avatar_lives}")
            print(f"Collision detected! Total collisions: {\
                  self.collision_count}")
            self.avatar.blink(self.screen)

    def __predict(self, a_ball):
        """Predict collision events for a ball."""
        if a_ball is None:
            return
        # Ball-to-ball collisions
        for i in range(len(self.ball_list)):
            dt = a_ball.time_to_hit(self.ball_list[i])
            heapq.heappush(self.pq, my_event.Event(
                self.t + dt, a_ball, self.ball_list[i]))
        # Ball-to-wall collisions
        dtX = a_ball.time_to_hit_vertical_wall()
        dtY = a_ball.time_to_hit_horizontal_wall()
        heapq.heappush(self.pq, my_event.Event(self.t + dtX, a_ball, None))
        heapq.heappush(self.pq, my_event.Event(self.t + dtY, None, a_ball))

    def __redraw(self):
        """Redraw all elements."""
        turtle.clear()
        self.__draw_border()
        for ball in self.ball_list:
            ball.draw()
        turtle.update()
        heapq.heappush(self.pq, my_event.Event(
            self.t + 1.0 / self.HZ, None, None))

    def __draw_border(self):
        turtle.penup()
        turtle.hideturtle()
        turtle.goto(-self.canvas_width, -self.canvas_height)
        turtle.pensize(10)
        turtle.pendown()
        turtle.color((0, 0, 0))
        for i in range(2):
            turtle.forward(2*self.canvas_width)
            turtle.left(90)
            turtle.forward(2*self.canvas_height)
            turtle.left(90)

    def check_game_over(self):
        """Check if all balls have been removed and display a message if so."""
        if self.avatar_lives <= 0:
            print("Out of lives. Pausing game.")  # Debug message
            self.pause_game("L")
        elif len(self.ball_list) == 0 and not self.is_paused:  # Ensure single transition
            print("All balls removed. Pausing game.")  # Debug message
            self.prepare_next_level()
            self.pause_game("W")

    def pause_game(self, settle):
        """Pause the game and allow only the restart input."""
        print("Game paused.")  # Debug message
        self.is_paused = True
        if settle == "L":
            self.display_message("You're out of lives! Press 'R' to Restart.")
        elif settle == "W":
            self.display_message(
                "You won! Press 'R' to Restart, 'N' to go to Next Level")

    def restart_game(self):
        """Restart the game by resetting the simulation, only if paused."""
        print(f"Restart attempt. Is paused: {self.is_paused}")  # Debug message
        if self.is_paused:
            print("Restarting the game...")  # Debug message
            self.is_paused = False
            self.screen.clear()
            self.__init__(self.num_balls, 1.2, "pics/hutao.gif",
                          3)  # Reinitialize the simulator
            heapq.heappush(self.pq, my_event.Event(
                0, None, None))  # Add an initial event
            self.run()
        else:
            print("Restart ignored: Game is not paused.")  # Debug message

    def prepare_next_level(self):
        """Prepare the game for the next level by resetting balls and events."""
        self.ball_list = []
        self.pq = []
        self.collision_count = 0
        self.avatar_lives = 3

        # Reset hearts
        for heart in self.hearts:
            heart.shape("pics/red_heart.gif")

        self.update_level_text(self.current_level)  # Update the level display
        heapq.heappush(self.pq, my_event.Event(
            0, None, None))  # Add an initial event
        print(f"Level {self.current_level} prepared!")

    def start_next_level(self):
        """Start a new instance of the simulator for the next level."""
        if self.is_paused:
            # Debug message
            print(f"Starting Level {self.current_level + 1}...")
            self.is_paused = False  # Unpause

            # Clear the screen and reset
            self.screen.clearscreen()

            # Update level count
            new_level = self.current_level + 1

            # Create new instance with updated attributes
            new_ball_count = 5 + (self.current_level // 2) + self.current_level
            initial_speed = 1.2 + (0.1 * self.current_level * 2)
            new_simulator = BouncingSimulator(
                num_balls=new_ball_count,
                initial_speed=initial_speed,
                avatar_gif="pics/hutao.gif",
                cooldown_time=3
            )

            # Update level text
            new_simulator.current_level = new_level
            new_simulator.update_level_text(new_level)

            # Run the new instance
            new_simulator.run()

    def update_level_text(self, level_number):
        """Update the displayed level text."""
        if hasattr(self, 'level_text'):
            self.level_text.clear()  # Clear the previous level text
        else:
            self.level_text = turtle.Turtle()
            self.level_text.penup()
            self.level_text.hideturtle()
            self.level_text.color("black")
            # Position at the bottom
            self.level_text.goto(0, self.canvas_height // 2 + 110)

        self.level_text.write(f"Level {level_number}", align="center", font=(
            "Times New Roman", 24, "bold"))
        print("Grace period active. invincible for 3 seconds.")

    def on_key_press(self, action):
        """Execute an action only if the game is not paused."""
        if not self.is_paused:
            action()
        else:
            print("Game is paused. Press 'R' to restart.")

    def display_message(self, message):
        """Display a message in the center of the screen."""
        turtle.penup()
        turtle.hideturtle()
        turtle.goto(0, 0)  # Center of the screen
        turtle.write(message, align="center", font=(
            "Times New Roman", 24, "bold"))

    def run(self):
        """Main simulation loop."""
        for ball in self.ball_list:
            self.__predict(ball)

        heapq.heappush(self.pq, my_event.Event(0, None, None))

        # Bind key
        self.screen.listen()
        self.screen.onkeypress(lambda: self.on_key_press(
            lambda: self.avatar.attack(self.remove_balls)), "e")
        # Bind 'R' for restart during pause
        self.screen.onkeypress(self.restart_game, "r")
        # Bind 'N' to go to the next level
        self.screen.onkeypress(self.start_next_level, "n")

        while True:
            if self.is_paused:
                self.screen.update()
                continue  # Skip simulation updates if the game is paused

            e = heapq.heappop(self.pq)
            if not e.is_valid():
                continue

            ball_a = e.a
            ball_b = e.b

            # Update ball positions
            for ball in self.ball_list:
                ball.move(e.time - self.t)

                # Detect collisions with the avatar
                if self.detect_collision(ball):
                    self.handle_collision(ball)

            self.t = e.time

            # Handle collisions
            if ball_a and ball_b:
                ball_a.bounce_off(ball_b)
            elif ball_a:
                ball_a.bounce_off_vertical_wall()
            elif ball_b:
                ball_b.bounce_off_horizontal_wall()
            else:
                self.__redraw()

            self.__predict(ball_a)
            self.__predict(ball_b)
            self.check_game_over()

        turtle.done()


# Main execution
if __name__ == "__main__":
    num_balls = 5
    initial_speed = 1.2  # Adjust speed
    avatar_gif = "pics/hutao.gif"  # Path to avatar sprite
    cooldown_time = 3  # Cooldown for avatar attack
    simulator = BouncingSimulator(
        num_balls, initial_speed, avatar_gif, cooldown_time)
    simulator.run()
