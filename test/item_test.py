import pygame
from pygame.math import Vector2
from lib.item import Item, Apple, Portal, Block
import random


def test_init():
    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))
    return screen


def test_exit():
    pygame.quit()


def test_apple():
    test_init()
    return Apple(25, 20)


def test_portal():
    test_init()
    return Portal(25, 20)

def test_block():
    test_init()
    return Block(25, 20)


def test_draw_item(mocker):
    mocker.patch('random.randint', return_value=10)
    screen = test_init()
    apple = test_apple()
    portal = test_portal()
    block = test_block()

    asset_apple, loc_apple = apple.draw_item_util()
    apple_asset = pygame.image.load('resources/apple.png').convert_alpha()
    assert (asset_apple.get_parent() == apple_asset.get_parent()
            and asset_apple.get_offset() == apple_asset.get_offset())
    assert loc_apple == pygame.Rect(250, 250, 25, 25)
    apple.draw_item(screen)

    asset_portal, loc_portal = portal.draw_item_util()
    portal_asset = pygame.image.load('resources/portal.png').convert_alpha()
    assert (asset_portal.get_parent() == portal_asset.get_parent()
            and asset_portal.get_offset() == portal_asset.get_offset())
    assert loc_portal == pygame.Rect(250, 250, 25, 25)
    portal.draw_item(screen)

    asset_block, loc_block = block.draw_item_util()
    block_asset = pygame.image.load('resources/block.png').convert_alpha()
    assert (asset_block.get_parent() == block_asset.get_parent()
            and asset_block.get_offset() == block_asset.get_offset())
    assert loc_block == pygame.Rect(250, 250, 25, 25)
    block.draw_item(screen)

    test_exit()
