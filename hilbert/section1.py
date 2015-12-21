from mobject import Mobject, Point
from mobject.tex_mobject import \
    TexMobject, TextMobject, Brace
from mobject.image_mobject import \
    ImageMobject, MobjectFromRegion

from scene import Scene

from animation import Animation
from animation.transform import \
    Transform, CounterclockwiseTransform, ApplyMethod,\
    GrowFromCenter, ClockwiseTransform
from animation.simple_animations import \
    ShowCreation, ShimmerIn, FadeOut, FadeIn
from animation.meta_animations import \
    DelayByOrder, TransformAnimations
from animation.playground import Vibrate

from topics.geometry import \
    Line, Dot, Arrow, Grid, Square, Point
from topics.characters import ThoughtBubble
from topics.number_line import UnitInterval
from topics.three_dimensions import Stars

from region import region_from_polygon_vertices

import displayer as disp

from hilbert.curves import \
    TransformOverIncreasingOrders, FlowSnake


from helpers import *



def get_grid():
    return Grid(64, 64)

def get_freq_line():
    return UnitInterval().shift(2*DOWN) ##Change?


class AboutSpaceFillingCurves(TransformOverIncreasingOrders):
    @staticmethod
    def args_to_string():
        return ""

    @staticmethod
    def string_to_args(arg_str):
        return ()

    def construct(self):
        self.bubble = ThoughtBubble().ingest_sub_mobjects()
        self.bubble.scale(1.5)

        TransformOverIncreasingOrders.construct(self, FlowSnake, 7)
        self.play(Transform(self.curve, self.bubble))
        self.show_infinite_objects()
        self.pose_question()
        self.dither()

    def show_infinite_objects(self):
        sigma, summand, equals, result = TexMobject([
            "\\sum_{n = 1}^{\\infty}",
            "\\dfrac{1}{n^2}",
            "=",
            "\\dfrac{\pi^2}{6}"
        ]).split()
        alt_summand = TexMobject("n").replace(summand)
        alt_result = TexMobject("-\\dfrac{1}{12}").replace(result)

        rationals, other_equals, naturals = TexMobject([
            "|\\mathds{Q}|",
            "=",
            "|\\mathds{N}|"
        ]).scale(2).split()
        infinity = TexMobject("\\infty").scale(2)
        local_mobjects = filter(
            lambda m : isinstance(m, Mobject),
            locals().values(),
        )
        for mob in local_mobjects:    
            mob.sort_points(np.linalg.norm)

        self.play(ShimmerIn(infinity))
        self.dither()
        self.play(
            ShimmerIn(summand),
            ShimmerIn(equals),
            ShimmerIn(result),
            DelayByOrder(Transform(infinity, sigma))
        )
        self.dither()
        self.play(
            Transform(summand, alt_summand),
            Transform(result, alt_result),
        )
        self.dither()
        self.remove(infinity)
        self.play(*[
            CounterclockwiseTransform(
                Mobject(summand, equals, result, sigma),
                Mobject(rationals, other_equals, naturals)
            )
        ])
        self.dither()
        self.clear()
        self.add(self.bubble)

    def pose_question(self):
        infinity, rightarrow, N = TexMobject([
            "\\infty", "\\rightarrow", "N"
        ]).scale(2).split()
        question_mark = TextMobject("?").scale(2)

        self.add(question_mark)
        self.dither()
        self.play(*[
            ShimmerIn(mob)
            for mob in infinity, rightarrow, N
        ] + [
            ApplyMethod(question_mark.next_to, rightarrow, UP),
        ])
        self.dither()




class PostponePhilosophizing(Scene):
    def construct(self):
        abstract, arrow, concrete = TextMobject([
            "Abstract", " $\\rightarrow$ ", "Concrete"
        ]).scale(2).split()

        self.add(abstract, arrow, concrete)
        self.dither()
        self.play(*[
            ApplyMethod(
                word1.replace, word2,
                interpolation_function = path_along_arc(np.pi/2)
            )
            for word1, word2 in it.permutations([abstract, concrete])
        ])
        self.dither()

class WriteSomeSoftware(Scene):
    pass #Done viea screen capture, written here for organization



class ImageToSound(Scene):
    def construct(self):
        string = Vibrate(color = BLUE_D, run_time = 5)
        picture = ImageMobject("lion", invert = False)
        picture.scale(0.8)
        picture_copy = picture.copy()
        picture.sort_points(np.linalg.norm)
        string.mobject.sort_points(lambda p : -np.linalg.norm(p))

        self.add(picture)
        self.dither()
        self.play(Transform(
            picture, string.mobject,
            run_time = 3,
            alpha_func = rush_into
        ))
        self.remove(picture)
        self.play(string)

        for mob in picture_copy, string.mobject:
            mob.sort_points(lambda p : np.linalg.norm(p)%1)

        self.play(Transform(
            string.mobject, picture_copy,
            run_time = 5,
            alpha_func = rush_from
        ))


class ImageDataIsTwoDimensional(Scene):
    def construct(self):
        image = ImageMobject("lion", invert = False)
        image.scale(0.5)
        image.shift(2*LEFT)

        self.add(image)
        for vect, num in zip([DOWN, RIGHT], [1, 2]):
            brace = Brace(image, vect)
            words_mob = TextMobject("Dimension %d"%num)
            words_mob.next_to(image, vect, buff = 1)
            self.play(
                Transform(Point(brace.get_center()), brace),
                ShimmerIn(words_mob), 
                run_time = 2
            )
        self.dither()


class SoundDataIsOneDimensional(Scene):
    def construct(self):
        overtones = 5
        floor = 2*DOWN
        main_string = Vibrate(color = BLUE_D)
        component_strings = [
            Vibrate(
                num_periods = k+1,
                overtones = 1,
                color = color,
                center = 2*DOWN + UP*k
            )
            for k, color in zip(
                range(overtones),
                Color(BLUE_E).range_to(WHITE, overtones)
            )
        ]
        dots = [
            Dot(
                string.mobject.get_center(),
                color = string.mobject.get_color()
            )
            for string in component_strings
        ]

        freq_line = get_freq_line()
        freq_line.shift(floor)
        freq_line.sort_points(np.linalg.norm)
        brace = Brace(freq_line, UP)
        words = TextMobject("Range of frequency values")
        words.next_to(brace, UP)


        self.play(*[
            TransformAnimations(
                main_string.copy(),
                string,
                run_time = 5
            )
            for string in component_strings
        ])
        self.clear()
        self.play(*[
            TransformAnimations(
                string,
                Animation(dot)
            )
            for string, dot in zip(component_strings, dots)
        ])
        self.clear()
        self.play(
            ShowCreation(freq_line),
            GrowFromCenter(brace),
            ShimmerIn(words),
            *[
                Transform(
                    dot,
                    dot.copy().scale(2).rotate(-np.pi/2).shift(floor),
                    interpolation_function = path_along_arc(np.pi/3)
                )
                for dot in dots
            ]
        )
        self.dither(0.5)

class GridOfPixels(Scene):
    def construct(self):
        low_res = ImageMobject("low_resolution_lion", invert = False)
        high_res = ImageMobject("Lion", invert = False)
        grid = get_grid()
        for mob in low_res, high_res:
            mob.replace(grid, stretch = True)
        for mob in low_res, high_res, grid:
            mob.sort_points(np.linalg.norm)
        side_brace = Brace(grid, LEFT)
        top_brace = Brace(grid, UP)
        top_words = TextMobject("256 Px", size = "\\normal")
        side_words = top_words.copy().rotate(np.pi/2)
        top_words.next_to(top_brace, UP)
        side_words.next_to(side_brace, LEFT)

        self.add(high_res)
        self.dither()
        self.play(DelayByOrder(Transform(high_res, low_res)))
        self.dither()
        self.play(DelayByOrder(Transform(high_res, grid)))
        self.clear()
        self.add(grid)
        self.play(
            GrowFromCenter(top_brace),
            GrowFromCenter(side_brace),
            ShimmerIn(top_words),
            ShimmerIn(side_words)
        )
        self.dither()


class ShowFrequencySpace(Scene):
    def construct(self):
        freq_line = get_freq_line()

        self.add(freq_line)
        self.dither()
        for tex, vect in zip(["20 Hz", "20{,}000 Hz"], [LEFT, RIGHT]):
            tex_mob = TextMobject(tex)
            tex_mob.to_edge(vect)
            tex_mob.shift(UP)
            arrow = Arrow(tex_mob, freq_line.get_edge_center(vect))
            self.play(
                ShimmerIn(tex_mob),
                ShowCreation(arrow)
            )
        self.dither()



class AssociatePixelWithFrequency(Scene):
    def construct(self):
        big_grid_dim = 20.
        small_grid_dim = 6.
        big_grid = Grid(64, 64, height = big_grid_dim, width = big_grid_dim)
        big_grid.to_corner(UP+RIGHT, buff = 2)
        small_grid = big_grid.copy()
        small_grid.scale(small_grid_dim/big_grid_dim)
        small_grid.center()
        pixel = MobjectFromRegion(
            region_from_polygon_vertices(*0.2*np.array([
                RIGHT+DOWN,
                RIGHT+UP,
                LEFT+UP,
                LEFT+DOWN
            ]))
        )
        pixel.set_color(WHITE)
        pixel_width = big_grid.width/big_grid.columns
        pixel.scale_to_fit_width(pixel_width)
        pixel.to_corner(UP+RIGHT, buff = 2)
        pixel.shift(5*pixel_width*(2*LEFT+DOWN))

        freq_line = get_freq_line()
        dot = Dot()
        dot.shift(freq_line.get_center() + 2*RIGHT)
        string = Line(LEFT, RIGHT, color = GREEN)
        arrow = Arrow(
            dot, string.get_center(),
            color = YELLOW_C
        )
        vibration_config = {
            "overtones"      : 1,
            "spatial_period" : 2,
        }
        vibration, loud_vibration, quiet_vibration = [
            Vibrate(string.copy(), amplitude = a, **vibration_config)
            for a in [0.5, 1., 0.25]
        ]

        self.add(small_grid)
        self.dither()
        self.play(
            Transform(small_grid, big_grid)
        )
        self.play(FadeIn(pixel))
        self.dither()
        self.play(
            FadeOut(small_grid),            
            ShowCreation(freq_line)
        )
        self.remove(small_grid)
        self.play(
            Transform(pixel, dot),
        )
        self.dither()
        self.play(ShowCreation(arrow))
        self.play(loud_vibration)
        self.play(
            TransformAnimations(loud_vibration, quiet_vibration),            
            ApplyMethod(dot.fade, 0.1)
        )
        self.clear()
        self.add(freq_line, dot, arrow)
        self.play(quiet_vibration)


class ListenToAllPixels(Scene):
    def construct(self):
        grid = get_grid()
        grid.sort_points(np.linalg.norm)        
        freq_line = get_freq_line()
        freq_line.sort_points(lambda p : p[0])
        red, blue = Color(RED), Color(BLUE)
        freq_line.gradient_highlight(red, blue)

        colors = [
            Color(rgb = interpolate(
                np.array(red.rgb),
                np.array(blue.rgb),
                alpha
            ))
            for alpha in np.arange(4)/3.
        ]
        string = Line(3*LEFT, 3*RIGHT, color = colors[1])
        vibration = Vibrate(string)
        vibration_copy = vibration.copy()
        vibration_copy.mobject.point_thickness = 1
        sub_vibrations = [
            Vibrate(
                string.copy().shift((n-1)*UP).highlight(colors[n]),
                overtones = 1,
                spatial_period = 6./(n+1),
                temporal_period = 1./(n+1),
                amplitude = 0.5/(n+1)
            )
            for n in range(4)
        ]
        words = TexMobject("&\\vdots \\\\ \\text{thousands }& \\text{of frequencies} \\\\ &\\vdots")
        words.to_edge(UP, buff = 0.1)

        self.add(grid)
        self.dither()
        self.play(DelayByOrder(ApplyMethod(
            grid.gradient_highlight, red, blue
        )))
        self.play(Transform(grid, freq_line))
        self.dither()
        self.play(
            ShimmerIn(
                words,
                alpha_func = squish_alpha_func(smooth, 0, 0.2)
            ),
            *sub_vibrations,
            run_time = 5
        )
        self.play(
            *[
                TransformAnimations(
                    sub_vib, vibration
                )
                for sub_vib in sub_vibrations
            ]+[FadeOut(words)]
        )
        self.clear()
        self.add(freq_line)
        self.play(vibration)


class LayAsideSpeculation(Scene):
    def construct(self):
        words = TextMobject("Would this actually work?")
        grid = get_grid()
        grid.scale_to_fit_width(6)
        grid.to_edge(LEFT)
        freq_line = get_freq_line()
        freq_line.scale_to_fit_width(6)
        freq_line.center().to_edge(RIGHT)
        mapping = Mobject(
            grid, freq_line, Arrow(grid, freq_line)
        )
        mapping.ingest_sub_mobjects()
        lower_left = Point().to_corner(DOWN+LEFT, buff = 0)
        lower_right = Point().to_corner(DOWN+RIGHT, buff = 0)

        self.add(words)
        self.dither()
        self.play(
            Transform(words, lower_right),
            Transform(lower_left, mapping)
        )
        self.dither()


class RandomMapping(Scene):
    def construct(self):
        grid = get_grid()
        grid.scale_to_fit_width(6)
        grid.to_edge(LEFT)
        freq_line = get_freq_line()
        freq_line.scale_to_fit_width(6)
        freq_line.center().to_edge(RIGHT)
        # for mob in grid, freq_line:
        #     indices = np.arange(mob.get_num_points())
        #     random.shuffle(indices)
        #     mob.points = mob.points[indices]
        stars = Stars(point_thickness = grid.point_thickness)

        self.add(grid)
        targets = [stars, freq_line]
        alphas = [not_quite_there(rush_into), rush_from]
        for target, alpha_func in zip(targets, alphas):
            self.play(Transform(
                grid, target,
                run_time = 3,
                alpha_func = alpha_func,
                interpolation_function = path_along_arc(-np.pi/2)
            ))
        self.dither()
        


class LeverageExistingIntuitions(Scene):
    def construct(self):
        self.add(TextMobject("Leverage existing intuitions"))
        self.dither()

















