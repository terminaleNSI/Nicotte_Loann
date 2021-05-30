# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 08:18:14 2021

@author: loann
"""

import pygame
import os

# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((1366, 768))
# screen = pygame.display.set_mode((1920, 1080))


def convert(x):
    return round(x * screen.get_width() / 1920)


def init_salles():
    global salles

    salles = [
        [pygame.transform.scale(
            pygame.image.load("assets/salles/0-0.png").convert(),
            (convert(1024), convert(1024))),

         pygame.transform.scale(
            pygame.image.load("assets/salles/1-0.png").convert(),
            (convert(1024), convert(1024))),

         pygame.transform.scale(
            pygame.image.load("assets/salles/2-0.png").convert(),
            (convert(1024), convert(1024)))],

        [pygame.transform.scale(
            pygame.image.load("assets/salles/0-1.png").convert(),
            (convert(1024), convert(1024))),

         pygame.transform.scale(
            pygame.image.load("assets/salles/1-1.png").convert(),
            (convert(1024), convert(1024))),

         pygame.transform.scale(
            pygame.image.load("assets/salles/2-1.png").convert(),
            (convert(1024), convert(1024)))],
        ]

    return 4


def init_cursor():
    global cursor
    nb = 0
    cursor = []
    for i in range(3):
        cursor.append(pygame.transform.scale(pygame.image.load(
            f"assets/inventaire/recipes_book/cursor{str(i)}.png").convert_alpha(), (convert(64), convert(102))))
        nb += 1

    return nb


def init_spike():
    global images_spikes
    nb = 0
    images_spikes = []
    for i in range(5):
        images_spikes.append(pygame.transform.scale(pygame.image.load(
            f"assets/spike/s{i}.png").convert_alpha(), (convert(64), convert(64))))
        nb += 1

    return nb


def init_torches_up():
    global images_torches_up
    nb = 0
    images_torches_up = []
    for i in os.listdir("assets/torches/torche_u"):
        images_torches_up.append(pygame.transform.scale(pygame.image.load(
            f"assets/torches/torche_u/{i}").convert_alpha(),
            (convert(14), convert(41))))
        nb += 1

    return nb


def init_torches_left():
    global images_torches_left
    nb = 0
    images_torches_left = []
    for i in os.listdir("assets/torches/torche_l"):
        images_torches_left.append(pygame.transform.scale(pygame.image.load(
            f"assets/torches/torche_l/{i}").convert_alpha(),
            (convert(14), convert(41))))
        nb += 1

    return nb


def init_torches_right():
    global images_torches_right
    nb = 0
    images_torches_right = []
    for i in os.listdir("assets/torches/torche_r"):
        images_torches_right.append(pygame.transform.scale(pygame.image.load(
            f"assets/torches/torche_r/{i}").convert_alpha(),
            (convert(14), convert(41))))
        nb += 1

    return nb


def init_back_name():
    global back_name
    back_name = pygame.image.load("assets/inventaire/back_name.png")

    return 1


def init_img_coeur():
    global images_coeur
    nb = 0
    images_coeur = []
    for i in os.listdir("assets/stats_player/coeurs"):
        images_coeur.append(pygame.transform.scale(
            pygame.image.load(f"assets/stats_player/coeurs/{i}"
                              ).convert_alpha(), (convert(45), convert(39))))
        nb += 1

    return nb


def init_img_armor():
    global images_armor
    nb = 0
    images_armor = []
    for i in os.listdir("assets/stats_player/armure"):
        images_armor.append(pygame.transform.scale(
            pygame.image.load(f"assets/stats_player/armure/{i}"
                              ).convert_alpha(), (convert(45), convert(45))))
        nb += 1

    return nb


def init_images_inv():
    global images_inv
    nb = 0
    images_inv = []
    for i in range(3):
        images_inv.append(pygame.transform.scale(pygame.image.load(
            f"assets/inventaire/inventaire{str(i)}.png").convert_alpha(),
            (convert(654), convert(584))))
        nb += 1

    return nb


def init_back_flou():
    global flou
    flou = pygame.transform.scale(pygame.image.load(
        "assets/inventaire/flou.png").convert_alpha(),
        (convert(64), convert(64)))

    return 1

def init_back_flou_chest():
    global flou_chest
    flou_chest = pygame.image.load("assets/chest/flou.png").convert_alpha()

    return 1

def init_none_equiped():
    global images_none_equiped
    nb = 0
    images_none_equiped = {}
    for nom in os.listdir("assets/inventaire/none_equiped"):
        images_none_equiped[nom[:len(nom) - 4]] = pygame.transform.scale(pygame.image.load(
            f"assets/inventaire/none_equiped/{nom}").convert_alpha(),
            (convert(64), convert(64)))

        nb += 1

    return nb


def init_display_part():
    global images_display_part
    nb = 0
    images_display_part = {}
    for nom in os.listdir("assets/inventaire/display"):
        images_display_part[nom[:len(nom) - 4]] = pygame.transform.scale(pygame.image.load(
            f"assets/inventaire/display/{nom}").convert_alpha(),
            (convert(195), convert(265)))

        nb += 1

    return nb


def init_slimes():
    global images_slime
    nb = 0
    image = pygame.image.load("assets/slime/slime_sprite.png")
    images_slime = [[]for i in range(20)]
    for i in range(20):
        for j in range(10):
            images_slime[i].append(pygame.transform.scale(image.subsurface(
                (32 * j, 32 * i, 32, 32)).convert_alpha(), (convert(128), convert(128))))
            nb += 1

    return nb


def init_portes():
    global images_porte
    images_porte = []
    for i in range(2):
        images_porte.append(pygame.transform.scale(pygame.image.load(
            f"assets/porte/porte{str(i)}.png").convert_alpha(),
            (convert(960), convert(1080))))
    return 2


def init_image_craft():
    global image_craft
    image_craft = pygame.transform.scale(pygame.image.load(
        "assets/inventaire/recipes_book/recipes.png").convert_alpha(),
        (convert(427), convert(241)))

    return 1


def init_item_craft():
    global images_item_craft
    nb = 0
    images_item_craft = {}
    for nom in os.listdir("assets/inventaire/recipes_book/items"):
        images_item_craft[nom[:len(nom) - 4]] = pygame.transform.scale(pygame.image.load(
            f"assets/inventaire/recipes_book/items/{nom}").convert_alpha(),
            (convert(79), convert(79)))

        nb += 1

    return nb


def init_item_recipes():
    global images_item_recipes
    nb = 0
    images_item_recipes = {}
    for nom in os.listdir("assets/inventaire/recipes_book/items"):
        images_item_recipes[nom[:len(nom) - 4]] = pygame.transform.scale(pygame.image.load(
            f"assets/inventaire/recipes_book/items/{nom}").convert_alpha(),
            (convert(50), convert(50)))

        nb += 1

    return nb


def init_background():
    global carte, background, player_blip
    background = pygame.transform.scale(
        pygame.image.load("assets/background.png").convert_alpha(),
        screen.get_size())

    carte = pygame.transform.scale(
        pygame.image.load("assets/carte.png").convert_alpha(),
        (convert(2000), convert(2000)))

    img = pygame.image.load("assets/player_blip.png").convert_alpha()
    player_blip = []

    for i in range(4):
        player_blip.append(pygame.transform.scale(
            img.subsurface([50 * i, 0, 50, 50]).convert_alpha(),
            (convert(20), convert(20))))

    return 6


def init_image_golem():
    global img_golem
    sprite_size = {"walk.png": (7, 4), "atk.png": (
        7, 4), "die.png": (7, 1), "idle.png": (2, 1)}
    img_golem = {anim[:len(anim) - 4]:
                 [[pygame.transform.scale(
                     pygame.image.load(f"assets/golem/{anim}")
                     .subsurface([64 * i, 96 * j, 64, 96]),
                     (convert(116), convert(173)))
                     for i in range(sprite_size.get(anim)[0])]
                     for j in range(sprite_size.get(anim)[1])]
                 for anim in os.listdir("assets/golem")}

    return 65


def init_spikes_atk():
    global spikes_atk
    img = pygame.image.load("assets/spike/spikes.png")
    spikes_atk = [
        [pygame.transform.scale(
            img.subsurface([64 * i, 64 * j, 64, 64])
            .convert_alpha(), (convert(128), convert(128)))
            for i in range(10)]
        for j in range(4)]
    return 40


def init_main_menu():
    global mm
    mm = [pygame.transform.scale(
        pygame.image.load(f"assets/main_menu/mm{i}.png").convert(),
        (convert(1920), convert(1080)))
        for i in range(6)]

    return 5


def init_main_menu_stats():
    global mms
    mms = [pygame.transform.scale(
        pygame.image.load(f"assets/main_menu/stats_menu/mm{i}.png").convert(),
        (convert(1920), convert(1080)))
        for i in range(3)]

    return 5


def init_item_loot():
    global images_item_loot
    nb = 0
    images_item_loot = {}
    for nom in os.listdir("assets/inventaire/recipes_book/items"):
        images_item_loot[nom[:len(nom) - 4]] = pygame.transform.scale(pygame.image.load(
            f"assets/inventaire/recipes_book/items/{nom}").convert_alpha(),
            (convert(30), convert(30)))

        nb += 1

    return nb


def init_images_spawner():
    global images_spawner
    nb = 0
    images_spawner = {}
    for nom in os.listdir("assets/spawner"):
        images_spawner[nom[:len(nom) - 4]] = pygame.transform.scale(pygame.image.load(
            f"assets/spawner/{nom}").convert_alpha(),
            (convert(64), convert(64)))

        nb += 1

    return nb


def init_images_archer():
    global images_archer
    sprite_size = {"walk.png": 5, "shoot.png": 6, "die.png": 3}
    images_archer = {nom[:len(nom) - 4]: [[pygame.transform.scale(
        pygame.image.load(f"assets/archer/{nom}").subsurface(
            (72 * i, 72 * j, 72, 72)).convert_alpha(),
        (convert(160), convert(160)))
        for j in range(sprite_size.get(nom))]
        for i in range(8)] for nom in os.listdir("assets/archer")}

    images_archer['idle'] = images_archer.get('walk')

    return 112

def init_image_wyvern():
    global wyvern
    wyvern = [[[None for y in range(8)]for j in range(8)]for i in range(7)]

    image = pygame.image.load("assets/wyvern/wyvern.png")

    for i in range(7):
        for j in range(8):
            for y in range(8):
                wyvern[i][y][j] = pygame.transform.scale(
                    image.subsurface([i*7*256 + y * 256, j * 256, 256, 256]),
                    (convert(512), convert(512))).convert_alpha()

    wyvern = {"hover" : wyvern[0], "fly" : wyvern[1], "hit" : wyvern[2],
              "breath" : wyvern[3], "boost" : wyvern[4], "roar" : wyvern[5],
              "die" : wyvern[6]}

    return 8*8*7

def init_health_bar():
    global health_bar
    health_bar = [pygame.transform.scale(pygame.image.load("assets/health_bar/bar.png"), (convert(800), convert(80))).convert_alpha(),
                  pygame.transform.scale(pygame.image.load("assets/health_bar/health.png"), (convert(800), convert(80))).convert_alpha()]

    return 3

def init_chest():
    global chest, back_item
    chest = [pygame.transform.scale(pygame.image.load(f"assets/chest/chest{i}.png"), (convert(72), convert(72))).convert_alpha() for i in range(3)]
    back_item = pygame.transform.scale(pygame.image.load("assets/chest/back_item.png"), (convert(100), convert(100))).convert_alpha()

    return 4

def init_anim_chest():
    global anim_chest
    anim_chest = pygame.image.load("assets/chest/anim0.png").convert_alpha()

    return 1


def init_item_chest():
    global items_chest
    nb = 0
    items_chest = {}
    for nom in os.listdir("assets/inventaire/recipes_book/items"):
        items_chest[nom[:len(nom) - 4]] = pygame.transform.scale(pygame.image.load(
            f"assets/inventaire/recipes_book/items/{nom}").convert_alpha(),
            (convert(100), convert(100)))

        nb += 1

    return nb

def init_pressure_plate():
    global pressure_plate
    pressure_plate = [[pygame.transform.scale(pygame.image.load(
            f"assets/pressure_plate/{i}off.png").convert_alpha(), (convert(64), convert(64))) for i in range(1, 7)],
        [pygame.transform.scale(pygame.image.load(
            f"assets/pressure_plate/{i}on.png").convert_alpha(), (convert(64), convert(64))) for i in range(1, 7)]]

    return 12
