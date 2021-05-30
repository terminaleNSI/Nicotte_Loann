# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 13:56:05 2021

@author: loann
"""
import pygame
import fonctions_utiles as FU
import images as imgs
import random as rdm
import math
import slime
import golem


class Spawner(pygame.sprite.Sprite):
    def __init__(self, jeu, x, y, mob, rate, ms):
        super().__init__()
        self.jeu = jeu
        self.mob = mob
        self.rate = rate
        self.imgs = imgs.images_spawner
        self.last_spawn = ms
        self.last_fire = ms
        self.rect = self.imgs.get("spawner").get_rect()
        self.rect.topleft = (x, y)
        self.fire = []

    def display(self, ms):
        self.jeu.screen.blit(self.imgs.get(self.mob), self.rect.topleft)

        self.jeu.screen.blit(self.imgs.get("spawner"), self.rect.topleft)
        for x, y in self.fire:
            self.jeu.screen.blit(self.imgs.get("flame"), (x, y))

        if self.last_fire + 100 < ms:
            self.last_fire = ms
            x = rdm.randint(self.rect.left - FU.convert(32),
                            self.rect.left + FU.convert(32))

            y = rdm.randint(self.rect.top - FU.convert(32),
                            self.rect.top + FU.convert(32))
            self.fire.append((x, y))
            if len(self.fire) > 10:
                self.fire = self.fire[1:]

        if self.last_spawn + self.rate < ms:
            self.spawn_mob(ms)
            self.last_spawn = ms

    def spawn_mob(self, ms):
        d = rdm.randint(FU.convert(50), FU.convert(300))
        a = rdm.randint(0, 360)
        x = self.rect.centerx + math.cos(math.radians(a)) * d
        y = self.rect.centery + math.sin(math.radians(a)) * d
        if self.mob == "slime":
            mob = slime.Slime(ms, self.jeu)
            mob.rect.center = (x, y)
            self.jeu.slimes.append(mob)

        elif self.mob == "golem":
            mob = golem.Golem(ms, self.jeu)
            mob.rect.center = (x, y)
            self.jeu.golems.append(mob)
