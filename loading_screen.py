# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 10:48:03 2021

@author: Lebobe Timothé
"""


import os
import pygame
import threading

import animation
import main_menu
import images as img


def convert(x):
    return round(x * screen.get_width() / 1920)


pygame.init()

screen = img.screen
clock = pygame.time.Clock()
pygame.mouse.set_cursor(*pygame.cursors.tri_left)

pour_txt = pygame.font.SysFont(None, convert(42))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def load_sprites_player():

    sprite_size = {"bow": (13, 4), "die": (6, 1), "dagger": (
        6, 4), "spellcast": (7, 4), "spear": (8, 4), "walkcycle": (9, 4)}

    global nb1

    return_val = {}
    for anim in os.listdir("assets/player/players"):
        return_val[anim] = {}
        x, y = sprite_size.get(anim)[0], sprite_size.get(anim)[1]
        for part in os.listdir(f"assets/player/players/{anim}"):
            return_val[anim][part] = []
            c_img = pygame.image.load(
                f"assets/player/players/{anim}/{part}").convert_alpha()
            height = c_img.get_height()
            width = c_img.get_width()
            for i in range(y):
                temp = []
                for j in range(x):
                    temp.append(pygame.transform.scale(
                        c_img .subsurface((
                            width/x * j, height/y * i, width/x, height/y)),
                        (convert(width/x * 2), convert(height/y * 2))))
                    nb1 += 1
                return_val[anim][part].append(temp)

    print(nb1)

    return return_val


def load_images():
    global nb2
    nb2 += img.init_salles()
    nb2 += img.init_cursor()
    nb2 += img.init_spike()
    nb2 += img.init_torches_left()
    nb2 += img.init_torches_right()
    nb2 += img.init_torches_up()
    nb2 += img.init_back_name()
    nb2 += img.init_img_armor()
    nb2 += img.init_img_coeur()
    nb2 += img.init_back_flou()
    nb2 += img.init_image_wyvern()
    nb2 += img.init_display_part()
    nb2 += img.init_none_equiped()
    nb2 += img.init_images_inv()
    nb2 += img.init_slimes()
    nb2 += img.init_portes()
    nb2 += img.init_image_craft()
    nb2 += img.init_item_craft()
    nb2 += img.init_item_recipes()
    nb2 += img.init_background()
    nb2 += img.init_image_golem()
    nb2 += img.init_spikes_atk()
    nb2 += img.init_main_menu()
    nb2 += img.init_main_menu_stats()
    nb2 += img.init_item_loot()
    nb2 += img.init_item_chest()
    nb2 += img.init_anim_chest()
    nb2 += img.init_images_spawner()
    nb2 += img.init_images_archer()
    nb2 += img.init_health_bar()
    nb2 += img.init_chest()
    nb2 += img.init_back_flou_chest()
    nb2 += img.init_pressure_plate()


    print(nb2)


def loading_page(run: bool = True) -> bool:
    clock.tick(100)
    time = pygame.time.get_ticks()

    screen.blit(sablier, (0, 0))

    chargement_anim.update(screen, time)

    pygame.draw.rect(screen, WHITE, [convert(
        60),  convert(870), convert(1800), convert(30)])
    pygame.draw.rect(screen, BLACK, [convert(62), convert(
        872), convert(1796) * (nb1 + nb2) / nb_image_max, convert(26)])

    pourcent = pour_txt.render(
        str(round((nb1 + nb2) * 100 / nb_image_max)) +
        " %", True, (125, 125, 125))

    screen.blit(pourcent, ((screen.get_width() -
                            pourcent.get_width()) / 2,  convert(871)))

    clock.tick(100)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

    return run


class Load_sprites_p(threading.Thread):

    def __init__(self):
        super().__init__()
        self.imgs = {}
        self.state = True

    def run(self) -> None:
        self.imgs = load_sprites_player()
        self.state = False


class Load_images(threading.Thread):

    def __init__(self):
        super().__init__()
        self.state = True

    def run(self) -> None:
        load_images()
        self.state = False


run = True

nb1 = 0
nb2 = 0

thread1 = Load_sprites_p()
thread2 = Load_images()
thread1.start()
thread2.start()

sablier = pygame.transform.scale(
    pygame.image.load("assets/loading_screen.png").convert(),
    (convert(1920), convert(1080)))


images_chargement = [pygame.transform.scale(pygame.image.load(
    f"assets/chargement/{i}").convert_alpha(),
    (convert(200), convert(200))) for i in os.listdir("assets/chargement")]

chargement_anim = animation.Animation(
    images_chargement, screen.get_width() / 2 - convert(100),
    screen.get_height() / 2 - convert(200), pygame.time.get_ticks())

clock = pygame.time.Clock()

nb_image_max = 7111


def play():
    global run
    while run:
        if (nb1 + nb2 >= nb_image_max and not
                thread1.state and not thread2.state):
            thread1._stop()
            thread2._stop()
            run = main_menu.main_menu(thread1.imgs, run)

        else:
            run = loading_page(run)

    pygame.quit()


if __name__ == "__main__":
    pass
