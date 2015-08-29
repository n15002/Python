#!/usr/bin/python3
from tkinter import *
import bounce
import random
import time

# 定数
WIDTH = 500
HEIGHT = 600
FPS = 60
BALL_SPEED = 5
PADDLE_SPEED = 3
BALL_MOVE_XY = (WIDTH * 0.5, HEIGHT * 0.5)
PADDLE_MOVE_XY = (WIDTH * 0.5, HEIGHT * 0.1)
BLOCKS_MOVE_XY = (WIDTH * 0.1, HEIGHT * 0.7)
COLORS = ('cyan', 'green', 'gold', 'dark orange', 'magenta',)
REVERSE = True
LIFE = 3

class reverse_Ball(bounce.Ball):
    def __init__(self, canvas, paddle, blocks, speed, color, xy,):
        super().__init__(canvas, paddle, blocks, speed, color, xy)
        self.hit_top = False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)

        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x *= -1
        if pos[3] <= 0:
            self.hit_top = True
        if pos[2] >= WIDTH:
            self.x *= -1
        if pos[3] >= HEIGHT:
            self.y *= -1
        if self.hit_paddle(pos):
            self.y *= -1

        (target, collision_type) = self.hit_block(pos)
        if target is not None:
            target.delete()
            del self.blocks[self.blocks.index(target)]
            if (collision_type & 1) != 0:
                self.y *= -1
            if (collision_type & 2) != 0:
                self.x *= -1

    def hit_paddle(self, pos):
            paddle_pos = self.canvas.coords(self.paddle.id)
            if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
                if pos[1] <= paddle_pos[3] and pos[1] >= paddle_pos[1]:
                    return True
            return False

class reverse_Paddle(bounce.Paddle):
    def __init__(self, canvas, speed, color, xy):
        super().__init__(canvas, speed, color, xy)


class reverse_Block(bounce.Block):
    def __init__(self, canvas, x, y, color):
        self.canvas = canvas
        self.pos_x = x
        self.pos_y = y
        self.id = canvas.create_rectangle(0, 0, 50, 20, fill=color)
        self.canvas.move(self.id, (WIDTH * 0.1) + self.pos_x * 50,
                         (HEIGHT * 0.9) + self.pos_y * -20)


if __name__ == '__main__':
    tk = Tk()
    Canvas(tk, width=WIDTH, height=HEIGHT)
    tk.title('ブロック崩し')
    tk.resizable(0, 0)
    tk.wm_attributes("-topmost", 1)
    canvas = Canvas(tk, width=WIDTH, height=HEIGHT, bd=0, highlightthickness=0)
    canvas.pack()
    tk.update()

    blocks = []
    if REVERSE:
        for y in range(4):
            for x in range(8):
                blocks.append(reverse_Block(canvas, x, y, random.choice(COLORS)))
        paddle = bounce.Paddle(canvas, PADDLE_SPEED, 'blue', PADDLE_MOVE_XY)
        ball = reverse_Ball(canvas, paddle, blocks, BALL_SPEED, 'red', BALL_MOVE_XY)
    else:
        for y in range(5):
            for x in range(8):
                blocks.append(bounce.Block(canvas, x, y, random.choice(COLORS)))
        paddle = bounce.Paddle(canvas, PADDLE_SPEED, 'blue', PADDLE_MOVE_XY)
        ball = bounce.Ball(canvas, paddle, blocks, BALL_SPEED, 'red', BALL_MOVE_XY)

    while True:
        ball.draw()
        paddle.draw()
        if ball.hit_top or ball.hit_bottom:
            sys.exit()
        tk.update_idletasks()
        tk.update()
        time.sleep(1 / FPS)
