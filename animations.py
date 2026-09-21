from manim import *
from PIL import Image
import numpy as np
import os

class AshWalking(Scene):
    SPRITE_DIR = "sprites/ash/"
    STEP_DISTANCE = 0.25
    STEP_TIME = 0.15

    def construct(self):
        ash = self.create_ash()
        path = [("down", 1.6), ("right", 1.7)] # FULL PATH HERE

        self.walk_path(ash, path)
        self.wait(5)

    def sprite_path(self, filename):
        return os.path.join(self.SPRITE_DIR, filename)

    def get_sprite_size(self, filename):
        image = Image.open(self.sprite_path(filename))
        return image.size

    def get_max_sprite_size(self):
        filenames = [
            "face_down_standing.png",
            "face_down_walk_1.png",
            "face_down_walk_2.png",
            "face_up_standing.png",
            "face_up_walk_1.png",
            "face_up_walk_2.png",
            "face_left_standing.png",
            "face_left_walk.png",
            "face_right_standing.png",
            "face_right_walk.png",
        ]
        sizes = [
            self.get_sprite_size(filename)
            for filename in filenames
        ]
        max_width = max(width for width, height in sizes)
        max_height = max(height for width, height in sizes)

        return max_width, max_height

    def load_padded_sprite(self, filename):
        image = Image.open(self.sprite_path(filename)).convert("RGBA")
        width, height = image.size
        max_width, max_height = self.get_max_sprite_size()
        canvas = Image.new("RGBA", (max_width, max_height), (0, 0, 0, 0))

        x = (max_width - width) // 2
        y = (max_height - height) // 2
        canvas.alpha_composite(image, (x, y))

        return np.array(canvas)

    def create_sprite(self, filename):
        image = self.load_padded_sprite(filename)
        return ImageMobject(image)

    def create_ash(self):
        ash = self.create_sprite("face_down_standing.png")
        ash.move_to(ORIGIN)
        return ash

    def get_walk_frames(self, direction):
        frames = {
            "up": ["face_up_walk_1.png", "face_up_walk_2.png"],
            "down": ["face_down_walk_1.png", "face_down_walk_2.png"],
            "left": ["face_left_standing.png", "face_left_walk.png"],
            "right": ["face_right_standing.png", "face_right_walk.png"]
        }

        return [self.create_sprite(filename) for filename in frames[direction]]

    def get_standing_sprite(self, direction):
        standing = {
            "up": "face_up_standing.png",
            "down": "face_down_standing.png",
            "left": "face_left_standing.png",
            "right": "face_right_standing.png"
        }

        return self.create_sprite(standing[direction])

    def walk(self, ash, direction, distance):
        frames = self.get_walk_frames(direction)
        movement = {
            "up": UP,
            "down": DOWN,
            "left": LEFT,
            "right": RIGHT
        }[direction]
        steps = round(distance / self.STEP_DISTANCE)

        for i in range(steps):
            frame = frames[i % 2]
            frame.move_to(ash.get_center())
            ash.become(frame)
            self.play(ash.animate.shift(movement * self.STEP_DISTANCE), run_time=self.STEP_TIME, rate_func=linear)

        standing = self.get_standing_sprite(direction)
        standing.move_to(ash.get_center())

        ash.become(standing)

    def walk_path(self, ash, path):
        for direction, distance in path:
            self.walk(ash, direction, distance)

class ShowGrid(Scene):
    GRID_SIZE = 4.9

    def construct(self):
        values = [
            [50, 65, 80],
            [95, "empty", 105],
            [120, 135, 150]
        ]
		numbers = self.create_numbers(values)
        grid = self.create_grid()

        self.play(Create(grid))
        self.play(*[Write(number) for number in numbers])
        self.wait(5)

    def create_grid(self):
        grid = VGroup()
        outer_square = Square(side_length=self.GRID_SIZE)
        grid.add(outer_square)

        cell_size = self.GRID_SIZE / 3
        for i in range(1, 3):
            offset = -self.GRID_SIZE / 2 + i * cell_size
            vertical_line = Line(start=[offset, -self.GRID_SIZE / 2, 0], end=[offset, self.GRID_SIZE / 2, 0])
            horizontal_line = Line(start=[-self.GRID_SIZE / 2, offset, 0], end=[self.GRID_SIZE / 2, offset, 0])
            grid.add(vertical_line, horizontal_line)

        return grid

    def create_numbers(self, values):
        numbers = VGroup()
        cell_size = self.GRID_SIZE / 3

        for row, row_values in enumerate(values):
            for col, value in enumerate(row_values):
                if value == "empty":
                    continue

                x = (-self.GRID_SIZE / 2 + (col + 0.5) * cell_size)
                y = (self.GRID_SIZE / 2 - (row + 0.5) * cell_size)
                number = Text(str(value), font_size=36)
                number.move_to([x, y, 0])
                numbers.add(number)

        return numbers

class MoveCursor(Scene):
    def construct(self):
        cursor = ImageMobject("sprites/cursor.png")
        cursor.scale(0.05)        
        cursor.move_to(RIGHT * 6 + UP * 3)
        
        self.add(cursor)
        self.play(cursor.animate.move_to(ORIGIN + 0.35 * DOWN + 0.15 * RIGHT), run_time=2, rate_func=smooth)
        self.wait(5)

class DrawSquare(Scene):
    def construct(self):
        square = Square(color=PURE_MAGENTA, stroke_width=20)

        self.play(Create(square))
        self.wait(5)

class ThunderboltAttack(Scene):
    def construct(self):
        bolt = ImageMobject("sprites/thunder_bolt.png")
        bolt.height = 2

        top_y = config.frame_height / 2 + 0.2
        bolt_y = top_y - bolt.height / 2
        start_x = -config.frame_width / 2 - bolt.width / 2
        bolt.move_to([start_x, bolt_y, 0])

        self.add(bolt)
        end_x = config.frame_width / 2 + bolt.width / 2
        self.play(bolt.animate.move_to([end_x, bolt_y, 0]), run_time=3, rate_func=linear)

class FishingAnimation(Scene):
    def construct(self):
        rod = ImageMobject("sprites/fishing_rod.png")
        rod.set_height(5.5)
        rod.move_to([0, -2.5, 0], aligned_edge=DOWN)
        pivot = rod.get_bottom()
        angle = 35 * DEGREES
        rod.rotate(-angle, about_point=pivot)

        self.add(rod)
        for swing in range(4):
            self.play(Rotate(rod, angle=2 * angle, about_point=pivot, rate_func=smooth), run_time=3)
            self.play(Rotate(rod, angle=-2 * angle, about_point=pivot, rate_func=smooth), run_time=3)
        self.wait(5)
