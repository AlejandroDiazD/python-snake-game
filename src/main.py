import turtle
import random
import time

class Snake():

    def __init__(self) -> None:
        self.screen_w = 600
        self.screen_h = 600

        self.threshold = 20

        self.delay = 0.1
        self.score = 0
        self.high_score = 0

        self.screen = turtle.Screen()
        self.head   = turtle.Turtle()
        self.food   = turtle.Turtle()
        self.scoreboard = turtle.Turtle()
        self.segments = []

        self.config()

    def config(self):
        # Screen
        self.screen.title("Python Snake game")
        self.screen.bgcolor("black")
        self.screen.setup(width=self.screen_w, height=self.screen_h)
        self.screen.tracer(0)

        # Keyboard controls
        self.screen.listen()
        self.screen.onkey(self.go_up, "w")
        self.screen.onkey(self.go_down, "s")
        self.screen.onkey(self.go_left, "a")
        self.screen.onkey(self.go_right, "d")

        # Snake head
        self.head.speed(0)
        self.head.shape("square")
        self.head.color("white")
        self.head.penup()
        self.head.goto(0, 0)
        self.head.direction = "stop"

        # Snake food
        self.food.speed(0)
        self.food.shape("circle")
        self.food.color("red")
        self.food.penup()
        self.food.goto(0, 100)

        # Scoreboard
        self.scoreboard.speed(0)
        self.scoreboard.shape("square")
        self.scoreboard.color("white")
        self.scoreboard.penup()
        self.scoreboard.hideturtle()
        self.scoreboard.goto(0, 260)
        self.scoreboard.write("Score: 0  High Score: 0", 
                              align="center", font=("Courier", 24, "normal"))

    # Movements
    def go_up(self):
        if self.head.direction != "down":
            self.head.direction = "up"

    def go_down(self):
        if self.head.direction != "up":
            self.head.direction = "down"

    def go_left(self):
        if self.head.direction != "right":
            self.head.direction = "left"

    def go_right(self):
        if self.head.direction != "left":
            self.head.direction = "right"

    def move_head(self):
        if self.head.direction == "up":
            y = self.head.ycor()
            self.head.sety(y + 20)

        elif self.head.direction == "down":
            y = self.head.ycor()
            self.head.sety(y - 20)

        elif self.head.direction == "left":
            x = self.head.xcor()
            self.head.setx(x - 20)

        elif self.head.direction == "right":
            x = self.head.xcor()
            self.head.setx(x + 20)

    def move_body(self):
        # Move from end of the body inversely
        for index in range(len(self.segments) - 1, 0, -1):
            x = self.segments[index - 1].xcor()
            y = self.segments[index - 1].ycor()
            self.segments[index].goto(x, y)

        # Move segment 0 to head position
        if len(self.segments) > 0:
            x = self.head.xcor()
            y = self.head.ycor()
            self.segments[0].goto(x, y)

    # Game actions
    def is_edge_collision(self):
        """
        Check if snake has a collision with screen edge.

        Args:
            head
            screen_w
            screen_h
            threshold: Minimum distance between elements to consider a collision.

        Returns:
            True if there is a collision, False if not.
        """
        if (self.head.xcor() >  (self.screen_w/2-self.threshold/2)  or 
            self.head.xcor() < -(self.screen_w/2-self.threshold/2)  or 
            self.head.ycor() >  (self.screen_h/2-self.threshold/2)  or 
            self.head.ycor() < -(self.screen_h/2-self.threshold/2)):
            return True
        else:
            return False

    def is_food_collision(self):
        """
        Check if snake head has a collision with food.

        Args:
            head
            food
            threshold: Minimum distance between elements to consider a collision.

        Returns:
            True if there is a collision, False if not.
        """
        if self.head.distance(self.food) < self.threshold:
            return True
        else:
            return False

    def is_snake_collision(self):
        """
        Check if snake head has a collision with any of its body segments.

        Args:
            head
            segments
            threshold: Minimum distance between elements to consider a collision.

        Returns: 
            True if there is a collision, False if not.
        """
        for segment in self.segments:
            if segment.distance(self.head) < self.threshold:
                return True
        return False

    def food_collision(self):
        # Relocate food
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        self.food.goto(x, y)

        # Add a snake body segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("grey")
        new_segment.penup()
        self.segments.append(new_segment)

        # Increase score
        self.score += 10
        if self.score > self.high_score:
            self.high_score = self.score
        self.scoreboard.clear()
        self.scoreboard.write("Score: {}  High Score: {}".
                        format(self.score, self.high_score), align="center", 
                        font=("Courier", 24, "normal"))

    def game_over(self):
        time.sleep(1)
        self.head.goto(0, 0)
        self.head.direction = "stop"

        # Hide segments
        for segment in self.segments:
            segment.goto(1000, 1000)

        # Reset segments list
        self.segments.clear()

        # Reset scoreboard
        self.score = 0
        self.scoreboard.clear()
        self.scoreboard.write("Score: {}  High Score: {}".
                        format(self.score, self.high_score), align="center", 
                        font=("Courier", 24, "normal"))

def main():
    snake = Snake()

    while True:
        snake.screen.update()

        if snake.is_snake_collision():
            snake.game_over()

        elif snake.is_edge_collision():
            snake.game_over()

        elif snake.is_food_collision():
            snake.food_collision()
            snake.move_body()
            snake.move_head()

        else:
            snake.move_body()
            snake.move_head()

        time.sleep(snake.delay)

if __name__ == "__main__":
    main()