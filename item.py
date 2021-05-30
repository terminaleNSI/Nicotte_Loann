# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 21:08:28 2021

@author: loann
"""
import pygame
import fonctions_utiles as FU
import images as img


class Item_armor:
    def __init__(self, name):
        self.name = name
        self.type = FU.item_type.get(name)

        self.img_inv = pygame.transform.scale(
            pygame.image.load(
                "assets/inventaire/armor/{}.png".format(name)
            ).convert_alpha(), (FU.convert(64), FU.convert(64)))

        self.txt_name = FU.font_item.render(FU.item_name.get(self.name),
                                            True, (255, 255, 255))

        self.back_nom = pygame.transform.scale(
            img.back_name, (self.txt_name.get_width(),
                            self.txt_name.get_height()))

    def display(self, screen, pos, loc):
        if loc == "inv":
            screen.blit(self.img_inv, pos)

    def display_name(self, screen, mouse):
        screen.blit(self.back_nom,
                    (mouse[0], mouse[1] - self.back_nom.get_height()))

        screen.blit(self.txt_name,
                    (mouse[0],
                     mouse[1] - self.back_nom.get_height() - FU.convert(5)))


class Item_weapons:
    def __init__(self, name):
        self.name = name
        self.type = FU.item_type.get(name)

        self.img_inv = pygame.transform.scale(
            pygame.image.load(
                "assets/inventaire/weapons/{}.png".format(name)
            ).convert_alpha(), (FU.convert(64), FU.convert(64)))

        self.txt_name = FU.font_item.render(FU.item_name.get(self.name),
                                            True, (255, 255, 255))

        self.back_nom = pygame.transform.scale(
            img.back_name, (self.txt_name.get_width(),
                            self.txt_name.get_height()))

    def display(self, screen, pos, loc):
        if loc == "inv":
            screen.blit(self.img_inv, pos)

    def display_name(self, screen, mouse):
        screen.blit(self.back_nom,
                    (mouse[0], mouse[1] - self.back_nom.get_height()))

        screen.blit(self.txt_name,
                    (mouse[0],
                     mouse[1] - self.back_nom.get_height() - FU.convert(5)))


class Item:
    def __init__(self, name, quantity):
        self.name = name
        self.type = FU.item_type.get(name)

        self.quantity = quantity

        self.font = FU.font

        self.txt_quantity = self.font.render(
            str(self.quantity), True, (255, 255, 255))

        self.img_inv = pygame.transform.scale(pygame.image.load(
            "assets/inventaire/items/{}.png".format(name)
        ).convert_alpha(), (FU.convert(64), FU.convert(64)))

        self.txt_name = FU.font_item.render(FU.item_name.get(self.name),
                                            True, (255, 255, 255))

        self.back_nom = pygame.transform.scale(
            img.back_name, (self.txt_name.get_width(),
                            self.txt_name.get_height()))

    def display(self, screen, pos, loc):
        if loc == "inv":
            screen.blit(self.img_inv, pos)
            screen.blit(self.txt_quantity,
                        (pos[0] + FU.convert(60) -
                         self.txt_quantity.get_width(),
                         pos[1] + FU.convert(60) -
                         self.txt_quantity.get_height()))

    def display_name(self, screen, mouse):
        screen.blit(self.back_nom,
                    (mouse[0], mouse[1] - self.back_nom.get_height()))

        screen.blit(self.txt_name,
                    (mouse[0],
                     mouse[1] - self.back_nom.get_height() - FU.convert(5)))

    def aug_quantity(self, quantity):
        self.quantity += quantity
        self.txt_quantity = self.font.render(
            str(self.quantity), True, (255, 255, 255))

    def dim_quantity(self, quantity):
        self.quantity -= quantity
        self.txt_quantity = self.font.render(
            str(self.quantity), True, (255, 255, 255))
