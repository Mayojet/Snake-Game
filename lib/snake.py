import pygame
from pygame.math import Vector2


class Snake:
    def __init__(self, size_per_cell, cell_num):
        self.size_per_cell = size_per_cell
        self.cell_num = cell_num
        self.body = [
            Vector2(12, 10),
            Vector2(12, 11),
            Vector2(12, 12),
        ]  # default body length = 3
        self.direction = Vector2(0, -1)
        self.tail_last_block = Vector2(12, 13)
        self.grow = False
        self.in_portal = False
        self.exit_portal_pos = None

        self.head_up = pygame.image.load(
            'resources/head_up.png').convert_alpha()
        self.head_down = pygame.image.load(
            'resources/head_down.png').convert_alpha()
        self.head_right = pygame.image.load(
            'resources/head_right.png').convert_alpha()
        self.head_left = pygame.image.load(
            'resources/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load(
            'resources/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load(
            'resources/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load(
            'resources/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load(
            'resources/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load(
            'resources/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load(
            'resources/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load(
            'resources/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load(
            'resources/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load(
            'resources/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load(
            'resources/body_bl.png').convert_alpha()

    def draw_snake(self, screen):
        components = self.draw_snake_util()
        for (asset, loc) in components:
            screen.blit(asset, loc)

    def get_rect(self, block):
        cell_size = self.size_per_cell
        x_pos = int(block.x * cell_size)
        y_pos = int(block.y * cell_size)
        return pygame.Rect(x_pos, y_pos, cell_size, cell_size)

    def draw_snake_util(self):
        """
        Returns a list of snake assets and locations based on 
        the current snake state 
        """
        components = []

        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            block_rect = self.get_rect(block)

            if index == 0:
                asset = self.head
            elif index == len(self.body) - 1:
                asset = self.tail
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                pb_x = previous_block.x
                pb_y = previous_block.y
                nb_x = next_block.x
                nb_y = next_block.y

                if pb_x == nb_x:
                    asset = self.body_vertical
                elif pb_y == nb_y:
                    asset = self.body_horizontal
                else:
                    if pb_x == -1 and nb_y == -1 or pb_y == -1 and nb_x == -1:
                        asset = self.body_tl
                    elif pb_x == -1 and nb_y == 1 or pb_y == 1 and nb_x == -1:
                        asset = self.body_bl
                    elif pb_x == 1 and nb_y == -1 or pb_y == -1 and nb_x == 1:
                        asset = self.body_tr
                    elif pb_x == 1 and nb_y == 1 or pb_y == 1 and nb_x == 1:
                        asset = self.body_br

            components.append((asset, block_rect))

        return components

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down
        else:
            if self.direction == Vector2(-1, 0):
                self.head = self.head_left
            elif self.direction == Vector2(1, 0):
                self.head = self.head_right
            elif self.direction == Vector2(0, -1):
                self.head = self.head_up
            else:
                self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down
        else:
            if self.direction == Vector2(-1, 0):
                self.tail = self.head_left
            elif self.direction == Vector2(1, 0):
                self.tail = self.head_right
            elif self.direction == Vector2(0, -1):
                self.tail = self.head_up
            else:
                self.tail = self.head_down

    def grow_snake(self):
        self.grow = True

    def enter_portal(self, exit_portal):
        self.in_portal = True
        self.exit_portal_pos = exit_portal.pos

    def move_snake(self):
        self.tail_last_block = self.body[-1]

        if self.grow == True:
            self.grow = False
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
        elif self.in_portal == True:
            self.in_portal = False
            body_copy = self.body[:-1]
            body_copy.insert(0, self.exit_portal_pos)
            self.body = body_copy[:]
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def get_tail_pos(self):
        return self.body[-1]

    def snake_collision(self, blocks):
        # check collision with self
        for i in range(len(self.body)):
            for j in range(len(self.body)):
                if i != j:
                    if self.body[i] == self.body[j]:
                        return True

        # check collision with edge of map
        for seg in self.body:
            if seg[0] < 0 or seg[1] < 0:
                return True
            if seg[0] >= self.cell_num or seg[1] >= self.cell_num:
                return True
        
        # check collision with blocks:
        for seg in self.body:
            for blk in blocks:
                if seg == blk.pos:
                    return True

        return False
