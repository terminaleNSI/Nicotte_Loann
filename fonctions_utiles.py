# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 13:33:53 2021

@author: loann
"""
import pygame
import math
import images as img
import loot
import os
import re

pygame.init()
screen = img.screen


def convert(x):
    return round(x * screen.get_width() / 1920)


def convert_inv(x):
    return round(x * 1920 / screen.get_width())


def get_plan(salle):
    plan = open(f"assets/plan/{salle[1]}-{salle[0]}.txt", "r")
    plan = plan.readlines()
    for line in range(len(plan)):
        plan[line] = plan[line][:16]
    return plan


def get_pos_salle(x, y):
    x -= convert(448)
    y -= convert(28)
    return round(x // convert(64)), round(y // convert(64))


def get_pos_screen(x, y):
    return convert(448 + x * 64), convert(28 + y * 64)


def get_distance(player, mob):
    center = player.get_center_screen()
    x1 = center[0]
    y1 = center[1]

    center = mob.get_center_screen()
    x2 = center[0]
    y2 = center[1]

    if isinstance(mob, loot.Loot):
        y1 = player.rect.bottom - convert(10)

    return math.sqrt(((x1 - x2)**2) + ((y1 - y2)**2))


def reset_save():
    fichier = open("assets/save/inventory.txt", "w")
    for i in range(3):
        for j in range(8):
            fichier.write("None;")
        fichier.write("\n")

    fichier = open("assets/save/equiped.txt", "w")
    fichier.write(
        "quiver None\nfeets None\nlegs None\nchestplate None\nbelt None\nhelmet None\ngloves None\narrow None\nweapons None\nsheild None")

    fichier = open("assets/save/player.txt", "w")
    fichier.write(
        """salle (0, 0)\nplayerx 960\nplayery 540\nplayervie 3\nplayermaxvie 3\nplayerbody None""")

    for i in os.listdir("assets/save/entity"):
        fichier = open(f"assets/save/entity/{i}", "w")
        fichier.write("")


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

def update_time_played():
    fichier = open("assets/save/stats.txt", "r")
    time = fichier.read()
    time = re.findall("\\d+", time)
    time = int(time[0]) * 3600 + int(time[1]) * 60 + int(time[2])
    time += 1
    h = time // 3600
    r = time - (h * 3600)
    m = r // 60
    s = r - (m * 60)
    if h < 10:
        h = "0" + str(h)
    else:
        h = str(h)

    if m < 10:
        m = "0" + str(m)
    else:
        m = str(m)

    if s < 10:
        s = "0" + str(s)
    else:
        s = str(s)

    fichier.close()
    fichier = open("assets/save/stats.txt", "w")
    fichier.write(f"time {h}:{m}:{s}")
    fichier.close()

def get_list(string):
    return_val = []
    for i in string:
        i = i.replace('[', '').replace(']', '').replace(',', '')
        return_val.append(int(i))
    return(return_val)


armor_value = {"chestplate_brown": 0.5, "chestplate_white": 0.5,
               "chestplate_chain": 1.5, "chestplate_leather": 1,
               "chestplate_metal": 2.5, "feet_leather": 0.5,
               "feet_metal": 1, "gloves": 0.5, "helmet_chain": 1,
               "helmet_leather": 0.5, "helmet_metal0": 1.5,
               "helmet_metal1": 1.5, "helmet_metal2": 1.5,
               "helmet_metal3": 1.5, "helmet_metal4": 1.5,
               "helmet_metal5": 1.5, "helmet_metal6": 1.5,
               "helmet_metal7": 1.5, "hood_chain": 1, "hood_leather": 0.5,
               "legs_leather": 1, "legs_metal": 1.5}

item_name = {"chestplate_brown": "T-Shirt Marron",
             "chestplate_white": "T-Shirt Blanc",
             "chestplate_chain": "Cotte de Maille",
             "chestplate_leather": "Plastron en Cuir",
             "chestplate_metal": "Plastron en Metal",
             "feet_leather": "Botte en Cuir",
             "feet_metal": "Botte en Metal", "gloves": "Gant en Metal",
             "helmet_chain": "Casque en Maille",
             "helmet_leather": "Casque en Cuir",
             "helmet_metal0": "Casque en Metal",
             "helmet_metal1": "Casque en Metal",
             "helmet_metal2": "Casque en Metal",
             "helmet_metal3": "Casque en Metal",
             "helmet_metal4": "Casque en Metal",
             "helmet_metal5": "Casque en Metal",
             "helmet_metal6": "Casque en Metal",
             "helmet_metal7": "Casque en Metal",
             "hood_chain": "Chapeau en Maille",
             "hood_leather": "Chapeau en Cuir",
             "legs_leather": "Jambiere en Cuir",
             "legs_metal": "Jambiere en Metal",
             "belt_leather": "Ceinture en Cuir",
             "belt_rope": "Ceinture en Corde",
             "bow": "Arc", "bow_up": "Arc ameliore",
             "dagger": "Dague", "quiver": "Carquois",
             "saber": "Sabre", "saber_blue": "Sabre laser bleu",
             "saber_red": "Sabre laser rouge", "arrow": "Fleche",
             "sheild1": "Bouclier", "spear": "Lance",
             "rope": "Corde", "stick": "Baton",
             "string": "Ficelle", "gold_ingot": "Lingot d'or",
             "coal": "Charbon", "silver_ingot": "Lingot d'argent",
             "tin_ingot": "Lingot d'etain", "copper_ingot": "Lingot de cuivre",
             "steel_ingot": "Lingot d'acier", "iron_ingot": "Lingot de fer",
             "iron_bar": "Tige en fer", "cable": "Cable", "flint": "Silex"}

item_type = {"chestplate_brown": "chestplate",
             "chestplate_white": "chestplate",
             "chestplate_chain": "chestplate",
             "chestplate_leather": "chestplate",
             "chestplate_metal": "chestplate", "feet_leather": "feets",
             "feet_metal": "feets", "gloves": "gloves",
             "helmet_chain": "helmet", "helmet_leather": "helmet",
             "helmet_metal0": "helmet", "helmet_metal1": "helmet",
             "helmet_metal2": "helmet", "helmet_metal3": "helmet",
             "helmet_metal4": "helmet", "helmet_metal5": "helmet",
             "helmet_metal6": "helmet", "helmet_metal7": "helmet",
             "hood_chain": "helmet", "hood_leather": "helmet",
             "legs_leather": "legs", "legs_metal": "legs",
             "belt_leather": "belt", "belt_rope": "belt", "bow": "weapons",
             "bow_up": "weapons", "dagger": "weapons", "saber": "weapons",
             "saber_blue": "weapons", "saber_red": "weapons", "quiver": "quiver",
             "sheild1": "sheild", "spear": "weapons", "arrow": "item",
             "rope": "item", "stick": "item", "string": "item",
             "gold_ingot": "item", "coal": "item", "silver_ingot": "item",
             "tin_ingot": "item", "copper_ingot": "item",
             "steel_ingot": "item", "iron_ingot": "item",
             "iron_bar": "item", "cable": "item", "flint": "item"}

item_class = {"armor": ["chestplate_brown", "chestplate_white",
                        "chestplate_chain", "chestplate_leather",
                        "chestplate_metal", "feet_leather", "feet_metal",
                        "gloves", "helmet_chain", "helmet_leather",
                        "helmet_metal0", "helmet_metal1", "helmet_metal2",
                        "helmet_metal3", "helmet_metal4", "helmet_metal5",
                        "helmet_metal6", "helmet_metal7", "hood_chain",
                        "hood_leather", "legs_leather", "legs_metal",
                        "belt_leather", "belt_rope"],
              "weapons": ["bow", "dagger", "quiver",  "sheild1", "spear",
                          "bow_up", "saber", "saber_blue", "saber_red"],
              "item": ["rope", "stick", "string", "arrow", "gold_ingot",
                       "coal", "silver_ingot", "tin_ingot", "copper_ingot",
                       "steel_ingot", "iron_ingot", "iron_bar", "cable",
                       "flint"]}

fichier = open("assets/items_ID.txt", "r")
items_ID = {}
lst = fichier.read()
lst = lst.split("\n")
for i in range(len(lst)):
    lst[i] = lst[i].split(":")
    items_ID[lst[i][0]] = int(lst[i][1])
    items_ID[int(lst[i][1])] = lst[i][0]

target_cursor = pygame.cursors.compile(("          XXXX          ",
                                        "          X..X          ",
                                        "          X..X          ",
                                        "        XXX..XXX        ",
                                        "       X........X       ",
                                        "      X...X..X..X       ",
                                        "     X..XXX..XXX..X     ",
                                        "    X..X  X..X  X..X    ",
                                        "   X..X   X..X   X..X   ",
                                        "   X..X   X..X   X..X   ",
                                        "XXXX.XXXXX XX XXXXX.XXXX",
                                        "X.........X  X.........X",
                                        "X.........X  X.........X",
                                        "XXXX.XXXXX XX XXXXX.XXXX",
                                        "   X..X   X..X   X..X   ",
                                        "   X..X   X..X   X..X   ",
                                        "    X..X  X..X  X..X    ",
                                        "     X..XXX..XXX..X     ",
                                        "      X...X..X...X      ",
                                        "       X........X       ",
                                        "        XXX..XXX        ",
                                        "          X..X          ",
                                        "          X..X          ",
                                        "          XXXX          ",))


sounds_footstep = [pygame.mixer.Sound(
    f"assets/sounds/footsteps/{i}")
    for i in os.listdir("assets/sounds/footsteps")]

font_fps = pygame.font.SysFont(None, 20)
font_txt = pygame.font.SysFont(None, 35)
font_die = pygame.font.SysFont("assets/font/Die.ttf", convert(200))
font_item = pygame.font.Font("assets/font/font.ttf", convert(40))
font = pygame.font.Font("assets/font/font.ttf", convert(20))
txt_porte = font_txt.render(
    "Press SPACE for take door", True, (255, 255, 255))
boss_porte = font_txt.render(
    "You need to kill the boss to take the door", True, (200, 0, 0))
pp_porte = font_txt.render(
    "You need to solve the puzzle to take the door", True, (200, 0, 0))
pp_failed = font_txt.render("Failed !", True, (200, 0, 0))
pp_completed = font_txt.render("Complete !", True, (0, 200, 0))
you_die = font_die.render("YOU DIED", True, (200, 0, 0))
txt_coffre = font_die.render(
    "Press SPACE for open chest", True, (255, 255, 255))
