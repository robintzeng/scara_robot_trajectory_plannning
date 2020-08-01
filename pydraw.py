import pygame as pg
import math
from pygame.math import Vector2


class Button(object):
    def __init__(self, rect, command, **kwargs):
        self.rect = pg.Rect(rect)
        self.command = command
        self.clicked = False
        self.hovered = False
        self.hover_text = None
        self.clicked_text = None
        self.process_kwargs(kwargs)
        self.render_text()

    def process_kwargs(self, kwargs):
        settings = {
            "color": pg.Color('navy'),
            "text": None,
            "font": None,  # pg.font.Font(None,16),
            "call_on_release": True,
            "hover_color": None,
            "clicked_color": None,
            "font_color": pg.Color("white"),
            "hover_font_color": None,
            "clicked_font_color": None,
            "click_sound": None,
            "hover_sound": None,
            'border_color': pg.Color('black'),
            'border_hover_color': pg.Color('yellow'),
            'disabled': False,
            'disabled_color': pg.Color('grey'),
            'radius': 3,
        }
        for kwarg in kwargs:
            if kwarg in settings:
                settings[kwarg] = kwargs[kwarg]
            else:
                raise AttributeError("{} has no keyword: {}".format(
                    self.__class__.__name__, kwarg))
        self.__dict__.update(settings)

    def render_text(self):
        if self.text:
            if self.hover_font_color:
                color = self.hover_font_color
                self.hover_text = self.font.render(self.text, True, color)
            if self.clicked_font_color:
                color = self.clicked_font_color
                self.clicked_text = self.font.render(self.text, True, color)
            self.text = self.font.render(self.text, True, self.font_color)

    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.on_release(event)

    def on_click(self, event):
        if self.rect.collidepoint(event.pos):
            self.clicked = True
            if not self.call_on_release:
                self.function()

    def on_release(self, event):
        if self.clicked and self.call_on_release:
            # if user is still within button rect upon mouse release
            if self.rect.collidepoint(pg.mouse.get_pos()):
                self.command()
        self.clicked = False

    def check_hover(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            if not self.hovered:
                self.hovered = True
                if self.hover_sound:
                    self.hover_sound.play()
        else:
            self.hovered = False

    def draw(self, surface):
        color = self.color
        text = self.text
        border = self.border_color
        self.check_hover()
        if not self.disabled:
            if self.clicked and self.clicked_color:
                color = self.clicked_color
                if self.clicked_font_color:
                    text = self.clicked_text
            elif self.hovered and self.hover_color:
                color = self.hover_color
                if self.hover_font_color:
                    text = self.hover_text
            if self.hovered and not self.clicked:
                border = self.border_hover_color
        else:
            color = self.disabled_color

        # if not self.rounded:
        #    surface.fill(border,self.rect)
        #    surface.fill(color,self.rect.inflate(-4,-4))
        # else:
        if self.radius:
            rad = self.radius
        else:
            rad = 0
        self.round_rect(surface, self.rect, border, rad, 1, color)
        if self.text:
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)

    def round_rect(self, surface, rect, color, rad=20, border=0, inside=(0, 0, 0, 0)):
        rect = pg.Rect(rect)
        zeroed_rect = rect.copy()
        zeroed_rect.topleft = 0, 0
        image = pg.Surface(rect.size).convert_alpha()
        image.fill((0, 0, 0, 0))
        self._render_region(image, zeroed_rect, color, rad)
        if border:
            zeroed_rect.inflate_ip(-2*border, -2*border)
            self._render_region(image, zeroed_rect, inside, rad)
        surface.blit(image, rect)

    def _render_region(self, image, rect, color, rad):
        corners = rect.inflate(-2*rad, -2*rad)
        for attribute in ("topleft", "topright", "bottomleft", "bottomright"):
            pg.draw.circle(image, color, getattr(corners, attribute), rad)
        image.fill(color, rect.inflate(-2*rad, 0))
        image.fill(color, rect.inflate(0, -2*rad))

    def update(self):
        # for completeness
        pass


class Point:
    # constructed using a normal tupple
    def __init__(self, point_t=(0, 0)):
        self.x = float(point_t[0])
        self.y = float(point_t[1])
    # define all useful operators

    def __add__(self, other):
        return Point((self.x + other.x, self.y + other.y))

    def __sub__(self, other):
        return Point((self.x - other.x, self.y - other.y))

    def __mul__(self, scalar):
        return Point((self.x*scalar, self.y*scalar))

    def __truediv__(self, scalar):
        return Point((self.x/scalar, self.y/scalar))

    def __len__(self):
        return int(math.sqrt(self.x**2 + self.y**2))
    # get back values in original tuple format

    def get(self):
        return (self.x, self.y)


def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=10):
    origin = Point(start_pos)
    target = Point(end_pos)
    displacement = target - origin

    length = len(displacement)
    # slope = Point((displacement.x/length, displacement.y/length))
    slope = displacement / float(length)

    for index in range(0, int(length/dash_length), 2):
        start = origin + (slope * index * dash_length)
        end = origin + (slope * (index + 1) * dash_length)
        pg.draw.line(surf, color, start.get(), end.get(), width)


def draw_xy_coordinate(surf, color, screen_width, screen_height, gap):
    pg.draw.line(surf, color, (0, screen_height/2),
                 (screen_width, screen_height/2), 1)

    pg.draw.line(surf, color, (screen_width/2, 0),
                 (screen_width/2, screen_height), 1)

    for i in range(int(screen_height/2), screen_height, gap):
        draw_dashed_line(surf, color, (0, i),
                         (screen_width, i), width=1, dash_length=5)

    for i in range(int(screen_height/2), 0, -gap):
        draw_dashed_line(surf, color, (0, i),
                         (screen_width, i), width=1, dash_length=5)

    for i in range(int(screen_width/2), screen_width, gap):
        draw_dashed_line(surf, color, (i, 0),
                         (i, screen_height), width=1, dash_length=5)

    for i in range(int(screen_width/2), 0, -gap):
        draw_dashed_line(surf, color, (i, 0),
                         (i, screen_height), width=1, dash_length=5)


class Entity(pg.sprite.Sprite):

    def __init__(self, pos, width, height, angle, offset):
        super().__init__()
        # self.image = pg.Surface((width, height), pg.SRCALPHA)
        # pg.draw.rect(self.image, pg.Color(
        #    'dodgerblue1'), [0, 0, width, height], 0)
        self.image = pg.image.load("link.png")
        self.image = pg.transform.scale(self.image, (width, height))
        # A reference to the original image to preserve the quality.
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)  # The original center position/pivot point.

        # We shift the sprite 50 px to the right.
        self.offset = Vector2(offset, 0)
        self.angle = angle
        self.endpoint = self.pos+self.offset.rotate(self.angle)*2

    def update(self):
        self.rotate()

    def rotate(self):
        """Rotate the image of the sprite around a pivot point."""
        # Rotate the image.
        self.image = pg.transform.rotozoom(self.orig_image, -self.angle, 1)
        # Rotate the offset vector.
        offset_rotated = self.offset.rotate(self.angle)
        # Create a new rect with the center of the sprite + the offset.
        self.rect = self.image.get_rect(center=self.pos+offset_rotated)
        self.endpoint = self.pos+self.offset.rotate(self.angle)*2


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((600, 400))
    screen_rect = screen.get_rect()
    done = False

    def print_on_press():
        print('button pressed')

    settings = {
        "clicked_font_color": (0, 0, 0),
        "hover_font_color": (205, 195, 100),
        'font': pg.font.Font(None, 16),
        'font_color': (255, 255, 255),
        'border_color': (0, 0, 0),
    }

    btn = Button(rect=(10, 10, 105, 25), command=print_on_press,
                 text='Press Me', **settings)

    while not done:
        mouse = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            btn.get_event(event)
        btn.draw(screen)
        draw_dashed_line(screen, pg.Color('red'), (0, 0),
                         (600, 400), dash_length=5)
        pg.display.update()
