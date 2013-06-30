#!/usr/bin/env python

from Tkinter import *
import random

field = None
paddle1 = None
paddle2 = None
score1 = None
score2 = None
ball = None


class Ball():

    def __init__(self, right):
        self.x = 0
        self.y = 0
        self.position = []
        self.velocity = []
        self.speed = 1
        self.right = right
        self.SPEED_UP_COEF = 0.15
        self.RADIUS = 20
        self.field_width = field.get_width()
        self.field_height = field.get_height()
        self.paddle_width = paddle1.get_width()
        self.paddle_half_height = paddle1.get_half_height()
        self.set_position()

    def set_position(self):
        self.x = random.randrange(120, 240)
        self.y = random.randrange(60, 180)
        if self.right:
            self.x = - self.x
            self.y = - self.y
        self.position = [self.field_width / 2, self.field_height / 2]
        self.velocity = [self.x / 50, self.y / 50]
        self.speed = 1

    def draw(self):
        paddle1_position = paddle1.get_position()
        paddle2_position = paddle2.get_position()

        self.position[0] -= self.velocity[0] * self.speed
        self.position[1] += self.velocity[1] * self.speed

        if self.position[0] >= self.field_width - self.paddle_width - self.RADIUS:
            if self.position[1] <= paddle2_position + self.paddle_half_height and self.position[1] >= paddle2_position - self.paddle_half_height:
                self.speed = self.speed + self.SPEED_UP_COEF
                self.velocity[0] = - self.velocity[0]
            else:
                score1.update()
                self.right = False
                self.set_position()

        if self.position[0] <= self.paddle_width + self.RADIUS:
            if self.position[1] <= paddle1_position + self.paddle_half_height and self.position[1] >= paddle1_position - self.paddle_half_height:
                self.speed = self.speed + self.SPEED_UP_COEF
                self.velocity[0] = - self.velocity[0]
            else:
                score2.update()
                self.right = True
                self.set_position()

        if self.position[1] <= self.RADIUS or self.position[1] >= (self.field_height - 1) - self.RADIUS:
            self.velocity[1] = - self.velocity[1]

        # draw ball
        canvas.create_oval(
            (self.position[0] - self.RADIUS, self.position[1] + self.RADIUS,
             self.position[0] + self.RADIUS, self.position[1] - self.RADIUS), fill="white")


class Paddle():

    def __init__(self, right):
        self.WIDTH = 18
        self.HEIGHT = 100
        self.HALF_WIDTH = self.WIDTH / 2
        self.HALF_HEIGHT = self.HEIGHT / 2
        self.right = right
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
        self.velocity = 0
        self.speed = 10
        self.center = field.get_height() / 2
        self.field_width = field.get_width()
        self.field_height = field.get_height()

    def get_width(self):
        return self.WIDTH

    def get_position(self):
        return self.center

    def get_half_height(self):
        return self.HALF_HEIGHT

    def draw(self):
        self.center += self.velocity

        if self.center <= self.HALF_HEIGHT:
            self.center = self.HALF_HEIGHT
        elif self.center >= self.field_height - self.HALF_HEIGHT:
            self.center = self.field_height - self.HALF_HEIGHT

        if self.right:
            self.x0 = self.field_width - self.HALF_WIDTH
            self.y0 = self.center - self.HALF_HEIGHT
            self.x1 = self.field_width - self.HALF_WIDTH
            self.y1 = self.center + self.HALF_HEIGHT
        else:
            self.x0 = self.HALF_WIDTH
            self.y0 = self.center - self.HALF_HEIGHT
            self.x1 = self.HALF_WIDTH
            self.y1 = self.center + self.HALF_HEIGHT

        canvas.create_line(
            self.x0, self.y0, self.x1, self.y1, fill="white", width=self.WIDTH)

    def keyup_handled(self):
        self.velocity = 0

    def keydown_handler(self, key):
        if key in ['w', 'Up'] and self.center - self.HALF_HEIGHT >= 0:
            self.velocity -= self.speed
        if key in ['s', 'Down'] and self.center + self.HALF_HEIGHT <= self.field_height:
            self.velocity += self.speed


class Field():

    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 600
        self.PADDLE_WIDTH = 18

    def get_height(self):
        return self.HEIGHT

    def get_width(self):
        return self.WIDTH

    def draw(self):
        canvas.create_line(
            self.WIDTH / 2, 0, self.WIDTH / 2, self.HEIGHT, fill="white")
        canvas.create_line(
            self.PADDLE_WIDTH, 0, self.PADDLE_WIDTH, self.HEIGHT, fill="white")
        canvas.create_line(self.WIDTH - self.PADDLE_WIDTH, 0,
                           self.WIDTH - self.PADDLE_WIDTH, self.HEIGHT, fill="white")


class Score():

    def __init__(self, right):
        self.total = 0
        self.field_width = field.get_width()
        if right:
            self.x = self.field_width - (self.field_width / 4)
        else:
            self.x = self.field_width / 4

        self.y = 50

    def update(self):
        self.total += 1

    def draw(self):

        canvas.create_text(self.x, self.y, text=str(
            self.total), fill="white", font=("Helvetica", 32))


def new_game(event):
    global field, paddle1, paddle2, score1, score2, ball

    field = Field()
    paddle1 = Paddle(False)
    paddle2 = Paddle(True)
    score1 = Score(False)
    score2 = Score(True)
    ball = Ball(random.choice([True, False]))


def keydown(event):
    global paddle1, paddle2

    if event.keysym in ['Up', 'Down']:
        paddle2.keydown_handler(event.keysym)
    elif event.keysym in ['w', 's']:
        paddle1.keydown_handler(event.keysym)


def keyup(event):
    global paddle1, paddle2

    if event.keysym in ['Up', 'Down']:
        paddle2.keyup_handled()
    elif event.keysym in ['w', 's']:
        paddle1.keyup_handled()


def update():
    canvas.after(1000 / 60, update)
    canvas.delete(ALL)
    field.draw()
    paddle1.draw()
    paddle2.draw()
    score1.draw()
    score2.draw()
    ball.draw()
    canvas.update()


root = Tk()
root.title('Pong')
new_game(None)
canvas = Canvas(root, width=800, height=600, bg="black")
button = Button(root, text="New game")
canvas.bind("<Key>", keydown)
canvas.bind("<KeyRelease>", keyup)
button.bind("<Button-1>", new_game)
canvas.focus_set()
canvas.pack()
button.pack()
canvas.after(1000 / 60, update)
root.mainloop()
