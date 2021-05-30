# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 11:57:32 2021

@author: loann
"""
import pygame
import images as imgs
import fonctions_utiles as FU


class Loot(pygame.sprite.Sprite):
    def __init__(self, jeu, name, x, y, quantity=1):
        super().__init__()
        self.jeu = jeu
        self.name = name
        self.quantity = quantity
        self.img = imgs.images_item_loot.get(self.name)
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)

    def display(self, screen):
        screen.blit(self.img, (self.rect.topleft))

    def kill(self):
        self.jeu.loot.remove(self)

    def collect(self, inv):
        inv.give(self.name, self.quantity)
        self.kill()

    def get_center_screen(self):
        return (self.rect.centerx, self.rect.centery)
