from lib.snake import Snake
from lib.bot import Bot
from lib.item import Apple, Portal, Block
from pygame.math import Vector2

import pygame
import sys
import random

# global variables
SIZE_PER_CELL = 40
NUM_CELLS = 20
FONT_SIZE = 25
EVENT_CYCLE = 150  # ms
STARTING_SNAKE_LENGTH = 3
SPAWN_PORTAL_PROB = 1
BLOCK_NUM = 4

# styling options
BACKGROUND_COLOR = (163, 214, 28)
GRASS_COLOR = (158, 207, 31)
MENU_BROWN_BLOCK_COLOR = (139, 69, 19)
SCORE_TEXT_COLOR = (0, 0, 0)
SCORE_BOX_BG_COLOR = (167, 209, 61)
SCORE_BOX_OUTLINE_COLOR = (0, 0, 0)
SCORE_BOX_OUTLINE_WIDTH = 3

#timer styling
TIMER_TEXT_COLOR = (100, 58, 207)
TIMER_BOX_BG_COLOR = (167, 209, 61)
TIMER_BOX_OUTLINE_COLOR = (0, 0, 0)
TIMER_BOX_OUTLINE_WIDTH = 3
TIME_TIME = 0

SCORE_COORDINATES = (SIZE_PER_CELL * (NUM_CELLS - 1), SIZE_PER_CELL)
TIMER_COORDINATES = (SIZE_PER_CELL * (NUM_CELLS // 2), SIZE_PER_CELL)

# Screen dimensions
WIDTH, HEIGHT = SIZE_PER_CELL * NUM_CELLS, SIZE_PER_CELL * NUM_CELLS
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


class Game():
    def __init__(self, options, event_cycle=150) -> None:
        global EVENT_CYCLE
        EVENT_CYCLE = event_cycle

        pygame.init()
        self.screen = pygame.display.set_mode(
            (NUM_CELLS * SIZE_PER_CELL, NUM_CELLS * SIZE_PER_CELL))
        self.screen.fill(BACKGROUND_COLOR)
        self.clock = pygame.time.Clock()
        pygame.time.set_timer(pygame.USEREVENT, EVENT_CYCLE)
        self.font = pygame.font.Font('resources/font.ttf', FONT_SIZE)
        self.bot = Bot(NUM_CELLS)

        self.enable_portal = options.get("portal", True)
        self.enable_block = options.get("block", True)
        self.enable_bot = options.get("bot", False)
        self.recv_input = False

    def game_start(self):
        font = pygame.font.Font(None, 36)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.main_menu(font)
            self.reset_game()
            self.game_loop()
            self.game_over_menu(font)

    def one_iter(self):
        self.reset_game()
        self.game_loop()
        return self.score

    def reset_game(self):
        self.score = 0
        self.time = 0
        self.snake = Snake(SIZE_PER_CELL, NUM_CELLS)
        self.apple = Apple(SIZE_PER_CELL, NUM_CELLS)

        if self.enable_portal:
            self.portal_1 = Portal(SIZE_PER_CELL, NUM_CELLS)
            self.portal_2 = Portal(SIZE_PER_CELL, NUM_CELLS)
            self.portal_3 = Portal(SIZE_PER_CELL, NUM_CELLS)
            self.portal_4 = Portal(SIZE_PER_CELL, NUM_CELLS)

        self.blocks = []
        if self.enable_block:
            self.init_blocks()

        self.has_portal = False
        self.has_block = False
        self.portal_enterable = False

    def init_blocks(self):
        for _ in range(BLOCK_NUM):
            self.blocks.append(Block(SIZE_PER_CELL, NUM_CELLS))
        items_pos = [self.apple.pos]
        for blk in self.blocks:
            blk.randomize(self.snake.body, items_pos)
            items_pos.append(blk.pos)

    def game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.USEREVENT:
                    self.update()
                    self.snake_interaction()

                if self.check_collision():
                    return

                if self.enable_bot == False:
                    self.movement(event)
                else:
                    if self.bot_exit(event) == True:
                        return
                    bot_choice = self.bot.get_move(
                        self.snake.body, self.snake.direction, self.snake.tail_last_block, self.apple.pos, self.blocks)
                    self.bot_movement(bot_choice)
            self.time += 1
            self.draw_elements()
            pygame.display.update()
            self.clock.tick(EVENT_CYCLE)

    def movement(self, event):
        if self.recv_input:
            return

        if event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_UP or key == pygame.K_w:
                if self.snake.direction.y != 1:
                    self.snake.direction = Vector2(0, -1)
                    self.recv_input = True
            if key == pygame.K_RIGHT or key == pygame.K_d:
                if self.snake.direction.x != -1:
                    self.snake.direction = Vector2(1, 0)
                    self.recv_input = True
            if key == pygame.K_DOWN or key == pygame.K_s:
                if self.snake.direction.y != -1:
                    self.snake.direction = Vector2(0, 1)
                    self.recv_input = True
            if key == pygame.K_LEFT or key == pygame.K_a:
                if self.snake.direction.x != 1:
                    self.snake.direction = Vector2(-1, 0)
                    self.recv_input = True

    def bot_exit(self, event):
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_q:
                return True
        return False

    def bot_movement(self, bot_choice):
        if bot_choice == 0:
            if self.snake.direction.y != 1:
                self.snake.direction = Vector2(0, -1)
        if bot_choice == 3:
            if self.snake.direction.x != -1:
                self.snake.direction = Vector2(1, 0)
        if bot_choice == 2:
            if self.snake.direction.y != -1:
                self.snake.direction = Vector2(0, 1)
        if bot_choice == 1:
            if self.snake.direction.x != 1:
                self.snake.direction = Vector2(-1, 0)

    def check_enter_portal(self):
        if not self.portal_enterable:
            return
        if self.portal_1.pos == self.snake.body[0]:
            self.snake.enter_portal(self.portal_2)
            self.portal_enterable = False
            return
        elif self.portal_2.pos == self.snake.body[0]:
            self.snake.enter_portal(self.portal_1)
            self.portal_enterable = False
            return
        elif self.portal_3.pos == self.snake.body[0]:
            self.snake.enter_portal(self.portal_4)
            self.portal_enterable = False
            return
        elif self.portal_4.pos == self.snake.body[0]:
            self.snake.enter_portal(self.portal_3)
            self.portal_enterable = False
            return

    def check_snake_exit_portal(self):
        tail_at_portal = (self.snake.get_tail_pos() == self.portal_1.pos or
                          self.snake.get_tail_pos() == self.portal_2.pos or
                          self.snake.get_tail_pos() == self.portal_3.pos or
                          self.snake.get_tail_pos() == self.portal_4.pos)

        if self.has_portal and tail_at_portal:
            self.has_portal = False

    def check_eat_apple(self):
        if self.apple.pos == self.snake.body[0]:  # check for eating apple
            self.apple.randomize(self.snake.body)
            self.snake.grow_snake()
            self.score += 1
            items_pos = [self.apple.pos]

            # portal spawning logic after eating an apple
            if self.enable_portal:
                random_num = random.uniform(0, 1)
                if self.has_portal == False and random_num <= SPAWN_PORTAL_PROB and self.check_snake_not_on_portal():
                    self.has_portal = True
                    self.portal_enterable = True
                    self.portal_1.randomize(self.snake.body, items_pos)
                    items_pos.append(self.portal_1.pos)
                    self.portal_2.randomize(self.snake.body, items_pos)
                    items_pos.append(self.portal_2.pos)
                    self.portal_3.randomize(self.snake.body, items_pos)
                    items_pos.append(self.portal_3.pos)
                    self.portal_4.randomize(self.snake.body, items_pos)
                    items_pos.append(self.portal_4.pos)
                else:
                    items_pos.append(self.portal_1.pos)
                    items_pos.append(self.portal_2.pos)
                    items_pos.append(self.portal_3.pos)
                    items_pos.append(self.portal_4.pos)

            # random obstacle spawning logic after eating an apple
            if self.enable_block:
                self.has_block = True
                for blk in self.blocks:
                    blk.randomize(self.snake.body, items_pos)
                    items_pos.append(blk.pos)

    def check_snake_not_on_portal(self):
        for body_blk in self.snake.body:
            if body_blk == self.portal_1.pos or body_blk == self.portal_2.pos:
                return False

        return True

    def snake_interaction(self):
        if self.enable_portal:
            self.check_snake_exit_portal()
        self.check_eat_apple()
        if self.enable_portal:
            self.check_enter_portal()

    def check_collision(self):
        if self.has_block == False:
            return self.snake.snake_collision([])

        return self.snake.snake_collision(self.blocks)

    def draw_grass(self):
        for row in range(NUM_CELLS):
            for col in range(NUM_CELLS):
                if row % 2 == 0 and col % 2 == 0:
                    grass_blk = pygame.Rect(
                        row * SIZE_PER_CELL, col * SIZE_PER_CELL, SIZE_PER_CELL, SIZE_PER_CELL)
                    pygame.draw.rect(self.screen, GRASS_COLOR, grass_blk)
                elif row % 2 != 0 and col % 2 != 0:
                    grass_blk = pygame.Rect(
                        row * SIZE_PER_CELL, col * SIZE_PER_CELL, SIZE_PER_CELL, SIZE_PER_CELL)
                    pygame.draw.rect(self.screen, GRASS_COLOR, grass_blk)

    def draw_menu_block(self):
        for row in range(NUM_CELLS // 2 - 4, NUM_CELLS // 2 + 6):
            for col in range(NUM_CELLS // 2 - 3, NUM_CELLS // 2 + 5):
                menu_blk = pygame.Rect(
                    row * SIZE_PER_CELL, col * SIZE_PER_CELL, SIZE_PER_CELL, SIZE_PER_CELL)
                pygame.draw.rect(self.screen, BLACK, menu_blk)
        for row in range(NUM_CELLS // 2 - 5, NUM_CELLS // 2 + 5):
            for col in range(NUM_CELLS // 2 - 4, NUM_CELLS // 2 + 4):
                menu_blk = pygame.Rect(
                    row * SIZE_PER_CELL, col * SIZE_PER_CELL, SIZE_PER_CELL, SIZE_PER_CELL)
                pygame.draw.rect(self.screen, MENU_BROWN_BLOCK_COLOR, menu_blk)

    def draw_elements(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_grass()
        self.snake.draw_snake(self.screen)
        self.apple.draw_item(self.screen)

        if self.has_portal:
            self.portal_1.draw_item(self.screen)
            self.portal_2.draw_item(self.screen)
            self.portal_3.draw_item(self.screen)
            self.portal_4.draw_item(self.screen)

        if self.has_block:
            for blk in self.blocks:
                blk.draw_item(self.screen)

        self.draw_score()
        self.draw_timer()

    def update(self):
        self.recv_input = False
        self.snake.move_snake()

    def draw_score(self):
        score_text = str(self.score)
        score_font = self.font.render(score_text, True, SCORE_TEXT_COLOR)
        score_rect = score_font.get_rect(
            center=(SCORE_COORDINATES[0], SCORE_COORDINATES[1]))

        score_box_margin = 5
        apple_rect = self.apple.get_image().get_rect(
            midright=(score_rect.left, score_rect.centery))
        score_bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width +
                                    score_rect.width + score_box_margin, apple_rect.height)

        pygame.draw.rect(self.screen, SCORE_BOX_BG_COLOR, score_bg_rect)
        self.screen.blit(score_font, score_rect)
        self.screen.blit(self.apple.get_image(), apple_rect)
        pygame.draw.rect(self.screen, SCORE_BOX_OUTLINE_COLOR,
                         score_bg_rect, SCORE_BOX_OUTLINE_WIDTH)
        
    def draw_timer(self):
        tot_seconds = self.time // EVENT_CYCLE
        minu = tot_seconds // 60
        seconds = tot_seconds - minu * 60
        timer_text = str(minu) + ":" + "%02d" % seconds
        timer_font = self.font.render(timer_text, True, TIMER_TEXT_COLOR)
        timer_rect = timer_font.get_rect(
            center=(TIMER_COORDINATES[0], TIMER_COORDINATES[1]), ) #center need to change

        timer_box_margin = 5
        #MADE CHANEGS --------------------------------------------------------------------
        timer_bg_rect = pygame.Rect(timer_rect.left, timer_rect.top, timer_rect.width +
                                    timer_rect.width + timer_box_margin, timer_rect.height)

        # pygame.draw.rect(self.screen, TIMER_BOX_BG_COLOR, timer_bg_rect)
        self.screen.blit(timer_font, timer_rect)
        #self.screen.blit(self.apple.get_image(), apple_rect)
        # pygame.draw.rect(self.screen, TIMER_BOX_OUTLINE_COLOR,
        #                  timer_bg_rect, TIMER_BOX_OUTLINE_WIDTH)
        #-------------------------------------------------------------------------------------


    @staticmethod
    def get_map_size():
        return NUM_CELLS

    def draw_text(self, FONT, text, color, x, y):
        surface = FONT.render(text, True, color)
        rect = surface.get_rect()
        rect.midtop = (x, y)
        SCREEN.blit(surface, rect)

    def main_menu(self, font):
        self.enable_bot = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_e:
                        self.enable_bot = True
                        return

            SCREEN.fill(BACKGROUND_COLOR)
            self.draw_grass()
            self.draw_menu_block()
            self.draw_text(font, "Snake Game", BLACK,
                           WIDTH // 2, HEIGHT // 2 - 110)
            self.draw_text(font, "Press ENTER to start",
                           WHITE, WIDTH // 2, HEIGHT // 2 - 10)
            self.draw_text(font, "Press E to begin bot",
                           WHITE, WIDTH // 2, HEIGHT // 2 + 40)
            self.draw_text(font, "Press Q to quit", WHITE,
                           WIDTH // 2, HEIGHT // 2 + 90)

            pygame.display.flip()

    def game_over_menu(self, font):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

            SCREEN.fill(BACKGROUND_COLOR)
            self.draw_grass()
            self.draw_menu_block()
            self.draw_text(font, "Game Over", BLACK,
                           WIDTH // 2, HEIGHT // 2 - 115)
            tot_seconds = self.time // EVENT_CYCLE
            minu = tot_seconds // 60
            seconds = tot_seconds - minu * 60
            timer_text = str(minu) + ":" + "%02d" % seconds
            self.draw_text(font, "Score: " + str(self.score) + "      Time: " + timer_text, BLACK,
                           WIDTH // 2, HEIGHT // 2 - 45)
            self.draw_text(font, "Press ENTER to continue",
                           WHITE, WIDTH // 2, HEIGHT // 2 + 25)
            self.draw_text(font, "Press Q to quit", WHITE,
                           WIDTH // 2, HEIGHT // 2 + 95)

            pygame.display.flip()
