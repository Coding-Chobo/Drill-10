from pico2d import *
from state_machine import *
from ball import Ball
import random
import game_world
import game_framework


class Flight:
    @staticmethod
    def enter(bird, e):
        global RUN_SPEED_PPS 
        PIXEL_PER_METER = (10.0 / 0.3)
        RUN_SPEED_KMPH = 20.0  # Km / Hour
        RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
        RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
        RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    @staticmethod
    def exit(bird, e):
        if space_down(e):
            bird.fire_ball()


    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 14
        bird.x += bird.dir * RUN_SPEED_PPS * game_framework.frame_time
        if bird.x > 1550 and bird.dir == 1:
            bird.dir = -1
        elif bird.x < 50 and bird.dir == -1:
            bird.dir = 1

    @staticmethod
    def draw(bird):
        if bird.dir == 1:
            bird.image.clip_draw((int(bird.frame)%5) * 183, (2-(int(bird.frame)//5)) * 168, 183, 168, bird.x, bird.y,50,50)            
        else:
            bird.image.clip_composite_draw((int(bird.frame)%5) * 183, (2-(int(bird.frame)//5))  * 168, 183, 168,0,'h', bird.x, bird.y,50,50)





class Bird:

    def __init__(self):
        self.x, self.y = 100 + random.randint(0,100), 300 + random.randint(0,100)
        self.dir = 1
        self.frame = 0
        self.image = load_image('bird_animation.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Flight)
        self.state_machine.set_transitions(
            {
                Flight: {}
            }
        )
        global TIME_PER_ACTION,FRAMES_PER_ACTION,ACTION_PER_TIME
        TIME_PER_ACTION = 0.5
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 8

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        pass

    def draw(self):
        self.state_machine.draw()
