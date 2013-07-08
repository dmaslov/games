#!/usr/bin/env python

from Tkinter import *


class Stopwatch():

    def __init__(self):
        self.score_total = 0
        self.score_win = 0
        self.current_timer_position = 0
        self.break_point = 6000
        self.timer = None

    def format(self):
        total_seconds = self.current_timer_position // 10
        minutes = total_seconds // 60
        seconds = total_seconds - minutes * 60
        miliseconds = self.current_timer_position - total_seconds * 10

        if minutes < 10:
            minutes = '0%d' % minutes
        if seconds < 10:
            seconds = '0%d' % seconds

        return '%s:%s.%d' % (minutes, seconds, miliseconds)

    def start(self, event):
        if not self.timer:
            self.timer = True

    def stop(self, event):
        if self.timer:
            self.compare()
            self.score_total += 1
            self.timer = None

    def reset(self, event):
        self.score_total = self.score_win = self.current_timer_position = 0
        if self.timer:
            self.timer = None

    def compare(self):
        num = self.current_timer_position - (self.current_timer_position // 10) * 10
        if not num:
            self.score_win += 1

    def get_info(self):
        return {
            'timer': self.timer,
            'current_timer_position': self.current_timer_position,
            'break_point': self.break_point,
            'score_win': self.score_win,
            'score_total': self.score_total,
            'stopwatch': self.format()
        }

    def increment_timer(self):
        self.current_timer_position += 1

    def break_timer(self):
        self.current_timer_position = 0


def tick():
    stopwatch_vars = stopwatch.get_info()
    if stopwatch_vars['timer']:
        stopwatch.increment_timer()
    if stopwatch_vars['current_timer_position'] > stopwatch_vars['break_point']:
        stopwatch.break_timer()
    draw()
    root.after(100, tick)


def draw():
    stopwatch_vars = stopwatch.get_info()
    score = 'Win: %d | Total: %d' % (stopwatch_vars['score_win'], stopwatch_vars['score_total'])
    canvas.delete(ALL)
    canvas.create_text(150, 30, text=str(
        score), fill="gray", font=("Times", 22))
    canvas.create_text(150, 100, text=str(stopwatch_vars['stopwatch']), fill="white", font=("Times", 32))
    canvas.update()

stopwatch = Stopwatch()
root = Tk()
root.title('Stopwatch Game')
canvas = Canvas(root, width=300, height=200, bg="black")
start_button = Button(root, text="Start")
stop_button = Button(root, text="Stop")
reset_button = Button(root, text="Reset")
start_button.bind("<Button-1>", stopwatch.start)
stop_button.bind("<Button-1>", stopwatch.stop)
reset_button.bind("<Button-1>", stopwatch.reset)

canvas.focus_set()
canvas.pack(side=TOP)
start_button.pack(side=LEFT)
stop_button.pack(side=LEFT)
reset_button.pack(side=RIGHT)
root.after(100, tick)
root.mainloop()
