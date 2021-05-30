# -*- coding: utf-8 -*-
"""
Created on Fri May 14 13:51:18 2021

@author: loann
"""
import images as img
import fonctions_utiles as FU
import pygame
import animation
import math

class Chest():
    def __init__(self, jeu, x, y, items, open = "False"):
        self.jeu = jeu

        self.images = img.chest
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.anim_loot = animation.Animation([img.anim_chest],
                                        self.jeu.screen.get_width() / 2,
                                        self.jeu.screen.get_height() / 2,
                                        pygame.time.get_ticks(),
                                        delay = 50,
                                        mode = "rotate",
                                        display_mode = "Center")

        self.x = x
        self.y = y

        self.items = items
        if open == "False":
            self.open = False
        else:
            self.open = True
            self.image = self.images[1]
        self.anim = False

        self.time_open = 0

        self.image_items = self.item_surface()

    def display(self):
        width = self.image.get_width()
        height = self.image.get_height()
        self.jeu.screen.blit(self.image, (self.x - width / 2,
                                          self.y - height / 2))

        if self.in_range() and not self.open:
            self.jeu.display_open_coffre()

    def display_loot(self):
        if self.anim:
            self.anim_loot.update(self.jeu.screen, pygame.time.get_ticks())
            self.jeu.screen.blit(self.image_items, (self.jeu.screen.get_width() / 2 - self.image_items.get_width() / 2,
                                                    (self.jeu.screen.get_height() / 2 - self.image_items.get_height() / 2)))


    def update(self):
        time = pygame.time.get_ticks()
        if not self.open and pygame.K_SPACE in self.jeu.key_pressed and self.in_range():
            self.open_chest()

        if self.anim and pygame.K_SPACE in self.jeu.key_pressed and self.time_open + 1000 < time:
            self.anim = False

    def in_range(self):
        x, y = self.jeu.player.rect.center
        return math.sqrt(((self.x - x) **2) + ((self.y - y)**2)) < FU.convert(100)

    def open_chest(self):
        self.open = True
        self.anim = True
        self.time_open = pygame.time.get_ticks()
        self.image = self.images[1]

        for item in self.items:
            self.jeu.inv.give(FU.items_ID.get(item), 1)

    def item_surface(self):
        if len(self.items) < 5:
            width = len(self.items)
        else:
            width = 5

        height = math.ceil(len(self.items) / 5)

        image_items = pygame.Surface((width * FU.convert(100) + (width-1) * FU.convert(20), height * FU.convert(100) + (height-1) * FU.convert(10)), pygame.SRCALPHA)

        items = [5 if len(self.items) - 5*i >= 5 else len(self.items) - 5 * i for i in range(height)]

        images = img.items_chest
        if len(self.items) >= 5:
            for i in range(len(items)):
                for j in range(items[i]):
                    image_items.blit(
                        img.back_item,
                        (j * FU.convert(100) + (5-items[i])*FU.convert(50) + j * FU.convert(20),
                         i * FU.convert(100) + i * FU.convert(20)))
                    image_items.blit(
                        images.get(
                            FU.items_ID.get(
                                self.items[i * 5 + j])),
                        (j * FU.convert(100) + (5-items[i])*FU.convert(50) + j * FU.convert(20),
                         i * FU.convert(100) + i * FU.convert(20)))

        else:
            for i in range(len(items)):
                for j in range(items[i]):
                    image_items.blit(
                        img.back_item, (j * FU.convert(100) + j * FU.convert(20),
                                        i * FU.convert(100) + i * FU.convert(20)))
                    image_items.blit(
                        images.get(
                            FU.items_ID.get(
                                self.items[i * 5 + j])),
                        (j * FU.convert(100) + j * FU.convert(20),
                         i * FU.convert(100) + i * FU.convert(20)))

        return image_items

    def kill(self):
        self.jeu.chest.remove(self)
