from manim import *
from time import sleep
from copy import deepcopy
import numpy as np
import math


class Mola(Scene):
    def construct(self):
        '''lattice = self.init_lattice() ## Assistance Lattice

        b1 = self.linha_vertical(-7) ## Scene Bound
        b2 = self.linha_vertical(7) ## Scene Bound
        self.add(b1, b2, *lattice)'''
        titulo = Text('Movimento Harmônico Simples') ## Titulo
        abr = Text('MHS') ## Titilo v2
        abrt = Text('MHS').scale(1)  ## Titulo v3
        abrt.shift(UP*3.5)
        self.play(Write(titulo))
        self.wait(1)
        self.play(Transform(titulo, abr))
        self.wait(1.1)

        road = Line(start=7*LEFT+3*DOWN, end=7*RIGHT+3*DOWN, stroke_width=5) ## Base
        wall = Line(start=4*LEFT+3*DOWN, end=4*LEFT+UP, stroke_width=10) ## Parede
        self.play(Create(road), Create(wall), Transform(titulo, abrt))

        block = Block(mass=1, side_length=1, fill_color=GREEN, fill_opacity=0.7, stroke_color=GREEN_A, z_index=-1).next_to(road, UP, buff=0)
        self.play(Create(block))
        ## Molas
        mola = always_redraw(lambda: DashedLine(start=wall.get_x()*RIGHT + (block.get_y()-0.25)*UP,
                                                end=block.get_x()*RIGHT + block.get_y()*UP + block.side_length*0.5*LEFT + 0.25*DOWN,
                                                stroke_color=GRAY, stroke_width=5))
        mola2 = always_redraw(lambda: DashedLine(start=wall.get_x()*RIGHT + (block.get_y()+0.25)*UP,
                                                end=block.get_x()*RIGHT + block.get_y()*UP + block.side_length*0.5*LEFT + 0.25*UP,
                                                stroke_color=GRAY, stroke_width=5))
        K : float = 0.5   # Spring Constant

        self.play(Create(mola), Create(mola2))
        self.wait(1)

        t = MathTex(r"F = -k \bigtriangleup x")  ## F = -kx
        t.next_to(titulo, DOWN)
        self.play(Write(t))

        dist = always_redraw(lambda: Distance(height=0.25, start=(block.get_y()+0.75)*UP,
                                              end=(block.get_y()+0.75)*UP+block.get_x()*RIGHT))
        dist_label = always_redraw(lambda: MathTex(rf"\bigtriangleup x = {round(block.get_x(), 2)}").scale(0.5).next_to(dist, UP))
        force_vec = always_redraw(lambda: Vector([-K*block.get_x(), 0], color=DARK_BLUE).shift((block.get_y()+0.1)*UP + block.get_x()*RIGHT))


        self.wait(1)
        self.play(Create(dist), Create(force_vec), Write(dist_label))
        self.wait(1)
        self.play(block.animate.shift(RIGHT*2), run_time=1.5)

        time = ValueTracker(0)
        vel_vec = always_redraw(lambda: Vector([-2*0.5**0.5*np.sin(0.5**0.5 * time.get_value()), 0], color=GOLD).shift((block.get_y()-0.1)*UP + block.get_x()*RIGHT))
        self.add(vel_vec)
        x_of_t = lambda box: box.set_x(2*np.cos(time.get_value()*(K/block.mass)**0.5))
        xoft = lambda t: 2*np.cos(t*(K/block.mass)**0.5)
        block.add_updater(update_function=x_of_t)
        P = math.pi * 8 ** 0.5
        self.play(time.animate.set_value(2*P), rate_func=rate_functions.linear, run_time=P)
        time.set_value(0)
        physics = VGroup()
        physics.add(block, mola, mola2, wall, road, dist, dist_label)
        self.play(physics.animate.shift(UP*5), Unwrite(titulo), Unwrite(t))
        ax_cnfg = {}
        axes = Axes(x_range=[0, 20, 1], y_range=[-2.5, 2.5, 0.5], x_length=10, y_length=5, tips=True,
                    axis_config={'include_numbers': True}).shift(DOWN)
        labels = axes.get_axis_labels('t', MathTex(r'\bigtriangleup x'))
        plot = always_redraw(lambda: axes.plot(function=xoft, x_range=[0, time.get_value()], color=BLUE))
        dot = always_redraw(lambda: Dot(color=BLUE, point=[axes.c2p(time.get_value(), xoft(time.get_value()))]))
        self.play(Create(axes), Create(dot), Write(labels))
        self.wait()
        self.add(plot)
        self.play(time.animate.set_value(2*P), rate_func=rate_functions.linear, run_time=P)
        self.play(*[Uncreate(x) for x in [block, mola, mola2, wall, road, dist, force_vec, axes, plot, dot]], Unwrite(dist_label), Unwrite(labels))
        self.wait()

    @staticmethod
    def linha_vertical(x: float):
        return Line(start=5*DOWN + x*RIGHT, end=5*UP + x*RIGHT)

    @staticmethod
    def linha_horizontal(y: float):
        return Line(start=x*UP + 10*RIGHT, end=x*UP + 10*LEFT)

    @staticmethod
    def init_lattice():
        xl = [x for x in range(-7, 8)]
        yl = [y for y in range(-5, 6)]
        lattice = list()

        for c1 in xl:
            for c2 in yl:
                lattice.append(Dot(point=c1*RIGHT+c2*UP, radius=0.02))

        return lattice



class Distance(Line):
    def __init__(self, height=0.5, **kwargs):
        super().__init__(**kwargs)

        startL = super().get_start()
        endL = super().get_end()

        left_bound = Line(start=startL+0.5*height*DOWN, end=startL+0.5*height*UP)
        right_bound= Line(start=endL+0.5*height*DOWN, end=endL+0.5*height*UP)

        self.add(left_bound, right_bound)


class Block(Square):
    def __init__(self, mass: int, **kwargs):
        super().__init__(**kwargs)
        self.mass = mass


