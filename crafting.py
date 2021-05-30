# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 19:00:42 2021

@author: loann
"""
import pygame
import fonctions_utiles as FU
import images as img


class Crafting:
    def __init__(self):

        self.crafts = {"bow": [["rope", "stick", None, None],
                               ["rope", None, "stick", None],
                               ["rope", None, "stick", None],
                               ["rope", "stick", None, None]],
                       "arrow": [[None, None, None, "flint"],
                                 [None, None, "stick", None],
                                 [None, "stick", None, None],
                                 ["stick", None, None, None]],
                       "rope": [["string", "string", None, None],
                                ["string", "string", None, None],
                                ["string", "string", None, None],
                                [None, None, None, None]],
                       "spear": [[None, None, None, "dagger"],
                                 [None, None, "stick", None],
                                 [None, "stick", None, None],
                                 ["stick", None, None, None]],
                       "belt_rope": [[None, None, None, None],
                                     ["string", "string", "string", "string"],
                                     ["string", None, None, "string"],
                                     ["string", "string", "string", "string"]],
                       "iron_bar": [["iron_ingot", None, None, None],
                                    ["iron_ingot", None, None, None],
                                    [None, None, None, None],
                                    [None, None, None, None]],
                       "cable": [["iron_ingot", "string", "silver_ingot", None],
                                 [None, None, None, None],
                                 [None, None, None, None],
                                 [None, None, None, None]],
                       "bow_up": [["cable", "iron_bar", None, None],
                                  ["cable", "bow", "stick", None],
                                  ["cable", "bow", "stick", None],
                                  ["cable", "iron_bar", None, None]]}

        self.size = (FU.convert(64), FU.convert(102))

        self.cursor = img.cursor

        self.cursor_x = FU.convert(1122)
        self.cursor_y = FU.convert(285)

        self.cursor_min = FU.convert(285)
        self.cursor_max = FU.convert(795) - self.size[1]

        self.len = FU.convert(408)

        self.pressed = False

        self.img_craft = img.image_craft
        self.img_item_craft = img.images_item_craft
        self.img_item_recipe = img.images_item_recipes

        self.nb_craft = len(self.crafts)

    def craft(self, table):
        for keys, craft in self.crafts.items():
            if craft == table:
                return keys

        return None

    def display(self, screen, mouse):
        self.display_cursor(screen, mouse)
        haut = pygame.Surface.subsurface(screen,
                                         (FU.convert(664),
                                          0,
                                          FU.convert(427),
                                          FU.convert(285))).convert_alpha()

        bas = pygame.Surface.subsurface(screen,
                                        (FU.convert(664),
                                         FU.convert(795),
                                         FU.convert(427),
                                         FU.convert(284))).convert_alpha()

        h = 0
        for craft, recipe in self.crafts.items():
            x = FU.convert(664)
            y = ((FU.convert(285) + self.img_craft.get_height() * h) -
                 (self.get_cursor_value() * (self.nb_craft - 2) *
                  (self.img_craft.get_height() / 100)))
            screen.blit(self.img_craft, (x, y))
            h += 1

            screen.blit(self.img_item_craft.get(craft),
                        (x + FU.convert(315), y + FU.convert(94)))
            for i in range(4):
                for j in range(4):
                    if recipe[i][j]:
                        screen.blit(self.img_item_recipe.get(
                            recipe[i][j]), (x + FU.convert(33 + j * 53),
                                            y + FU.convert(29 + i * 53)))

        screen.blit(haut, (FU.convert(664), 0))
        screen.blit(bas, (FU.convert(664), FU.convert(795)))

    def display_cursor(self, screen, mouse):
        if self.pressed:
            img = 2

        elif (self.cursor_x <= mouse[0] <= self.cursor_x + self.size[0] and
              self.cursor_y <= mouse[1] <= self.cursor_y + self.size[1]):
            img = 1

        else:
            img = 0

        screen.blit(self.cursor[img], (self.cursor_x, self.cursor_y))

        self.update_cursor(mouse)

    def update_cursor(self, mouse):
        if self.pressed:
            self.cursor_y = mouse[1] - self.size[1] / 2
            if self.cursor_y < self.cursor_min:
                self.cursor_y = self.cursor_min

            elif self.cursor_y > self.cursor_max:
                self.cursor_y = self.cursor_max

    def up_cursor(self):
        if not self.pressed:
            self.cursor_y -= 50
            if self.cursor_y <= self.cursor_min:
                self.cursor_y = self.cursor_min

    def down_cursor(self):
        if not self.pressed:
            self.cursor_y += 50
            if self.cursor_y >= self.cursor_max:
                self.cursor_y = self.cursor_max

    def reset_cursor(self):
        self.pressed = False
        self.cursor_y = FU.convert(285)

    def get_cursor_value(self):
        return (self.cursor_y - self.cursor_min) * 100 / self.len
        return (self.cursor_y - self.cursor_min) * 100 / self.len
