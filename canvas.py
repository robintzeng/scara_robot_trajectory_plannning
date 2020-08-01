import pygame as pg
from pydraw import *
from enum import Enum
import numpy as np

screen_width = 640
screen_height = 480
clock = pg.time.Clock()
first_time = True


def setting():
    global btn0, btn1, screen, canvas, first_time

    def btn0_cmd():
        canvas.fill(pg.Color("white"))
        print("Clean")

    def btn1_cmd():
        global first_time
        first_time = True
        print("Rerun")

    btn0_settings = {
        "clicked_font_color": (0, 0, 0),
        "hover_font_color": (0, 0, 128),
        'font': pg.font.Font(None, 16),
        'font_color': (255, 255, 255),
        'border_color': (0, 0, 0),
    }

    btn0 = Button(rect=(10, 10, 120, 60), command=btn0_cmd,
                  text='Clear Trajectory', **btn0_settings)

    btn1_settings = {
        "color": pg.Color('red'),
        "clicked_font_color": (0, 0, 0),
        "hover_font_color": (0, 0, 128),
        'font': pg.font.Font(None, 16),
        'font_color': (255, 255, 255),
        'border_color': (0, 0, 0),
    }

    btn1 = Button(rect=(180, 10, 120, 60), command=btn1_cmd,
                  text='Rerun', **btn1_settings)

    screen = pg.display.set_mode((screen_width, screen_height))
    canvas = pg.Surface(screen.get_size())
    canvas = canvas.convert()

    screen.fill(pg.Color("white"))
    canvas.fill(pg.Color("white"))


def manual_mode():
    global btn0, btn1, screen, canvas
    l0 = 100
    l1 = 100

    setting()

    # *1.1 for beauty
    link0 = Entity((screen_width/2, screen_height/2),
                   int(l0), 1, 59.9184, int(l0/2))
    link1 = Entity((link0.endpoint), int(l1), 1, -420.3016, int(l1/2))

    all_sprites = pg.sprite.Group(link0, link1)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            btn0.get_event(event)
        keys = pg.key.get_pressed()

        if keys[pg.K_d]:
            link0.pos.x += 5
        elif keys[pg.K_a]:
            link0.pos.x -= 5

        elif keys[pg.K_w]:
            link0.angle += 2

        elif keys[pg.K_q]:
            link0.angle -= 2

        elif keys[pg.K_r]:
            link1.angle += 2

        elif keys[pg.K_e]:
            link1.angle -= 2

        link0.update()
        link1.pos = link0.endpoint
        mutiUpdate(link0, link1)


def auto_mode(buffer, l0, l1):
    global btn0, btn1, screen, canvas, screen_width, screen_height, first_time
    setting()

    # *1.1 for beauty

    link0 = Entity((screen_width/2, screen_height/2),
                   int(1.1*l0), 30, -buffer[0][0], int(l0/2))

    link1 = Entity((link0.endpoint), int(1.1*l1), 30,
                   -(buffer[0][0]+buffer[0][1])-360, int(l1/2))

    while True:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            btn0.get_event(event)
            btn1.get_event(event)

        keys = pg.key.get_pressed()

        if keys[pg.K_d]:
            link0.pos.x += 5
        elif keys[pg.K_a]:
            link0.pos.x -= 5

        elif keys[pg.K_w]:
            link0.angle += 2

        elif keys[pg.K_q]:
            link0.angle -= 2

        elif keys[pg.K_r]:
            link1.angle += 2

        elif keys[pg.K_e]:
            link1.angle -= 2
        link0.update()
        link1.pos = link0.endpoint

        if(first_time == True):

            for buf in buffer:
                link0.angle = -buf[0]
                link0.update()
                link1.pos = link0.endpoint
                link1.angle = -(buf[0]+buf[1])-360
                mutiUpdate(link0, link1)
            first_time = False

        buf = buffer[len(buffer)-1]
        mutiUpdate(link0, link1)


def mutiUpdate(link0, link1):
    global screen_width, screen_height, clock, btn0, btn1, screen, canvas

    all_sprites = pg.sprite.Group(link0, link1)
    all_sprites.update()

    pg.draw.circle(canvas, pg.Color('black'), [
        int(i) for i in link1.endpoint], 3)

    screen.blit(canvas, (0, 0))

    draw_xy_coordinate(screen, (100, 200, 255),
                       screen_width, screen_height, 50)

    all_sprites.draw(screen)
    btn0.draw(screen)
    btn1.draw(screen)

    pg.draw.circle(screen, pg.Color('orange'), [
        int(i) for i in link0.pos], 3)

    pg.draw.circle(screen, pg.Color('orange'), [
        int(i) for i in link0.endpoint], 3)

    pg.draw.circle(screen, pg.Color('orange'), [
        int(i) for i in link1.endpoint], 3)

    pg.display.flip()
    pg.display.update()
    clock.tick(30)


if __name__ == '__main__':
    pg.init()
    manual_mode()
    pg.quit()
