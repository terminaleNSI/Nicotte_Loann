# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 19:43:21 2021

@author: loann
"""
import random as rdm
import images as img
import pygame
import math
import arrow
import fonctions_utiles as FU

class Archer(pygame.sprite.Sprite):
    def __init__(self, jeu):
        self.imgs = img.images_archer
        self.jeu = jeu
        self.name = "archer"

        self.direction = 4
        self.action = "walk"
        self.n_image = 0
        self.last_img = pygame.time.get_ticks()
        self.angle = 0

        self.image = self.imgs.get(self.action)[self.direction][self.n_image]
        self.rect = self.image.get_rect()
        pos = rdm.choice(jeu.spawnable)
        pos = FU.get_pos_screen(pos[0], pos[1])

        self.rect.bottom = pos[1]
        self.rect.left = pos[0]

        self.x = self.rect.left
        self.y = self.rect.top


    def display(self):
        try:
            self.jeu.screen.blit(self.imgs[self.action][self.get_direction(self.angle)][self.n_image], self.rect.topleft)
        except:
            None

    def update(self, ms):
        if self.action != "die":
            if FU.get_distance(self.jeu.player, self) < FU.convert(300):

                x = self.jeu.player.rect.centerx - self.rect.centerx
                y = self.jeu.player.rect.centery - self.rect.centery
                self.angle = math.degrees(math.atan2(y, x))

                self.action = 'shoot'
            elif FU.get_distance(self.jeu.player, self) < FU.convert(400):

                x = self.jeu.player.rect.centerx - self.rect.centerx
                y = self.jeu.player.rect.centery - self.rect.centery
                self.angle = math.degrees(math.atan2(y, x))

                self.action = 'walk'
                self.x += math.cos(math.radians(self.angle))
                self.y += math.sin(math.radians(self.angle))

                self.rect.topleft = self.x, self.y

        if self.action == 'walk' and self.last_img + 100 < ms:
            self.n_image += 1
            self.last_img = ms
            if self.n_image > 4:
                self.n_image = 0

        elif self.action == 'shoot' and self.last_img + 200 < ms:
            self.last_img = ms
            self.n_image += 1
            if self.n_image == 2:
                self.shoot(self.angle)
            if self.n_image > 5:
                self.n_image = 0

        elif self.action == 'die':
            if self.last_img + 300 < ms:
                self.last_img = ms
                self.n_image += 1
                if self.n_image == 3:
                    self.jeu.archer.remove(self)

    def kill(self):
        self.action = "die"
        self.n_image = 0

    def shoot(self, angle):

        self.jeu.arrows.append(arrow.Arrow(self.rect.centerx, self.rect.centery,
                                          angle, pygame.time.get_ticks(), 4, "archer"))

    def get_center_screen(self):
        return self.rect.center

    def get_direction(self, angle):
        return_val = 0
        if angle > 157.5 or angle < -157.5:
            return_val = 6
        elif angle < -112.5:
            return_val = 7
        elif angle < -67.5:
            return_val = 0
        elif angle < -22.5:
            return_val = 1
        elif angle < 22.5:
            return_val = 2
        elif angle < 67.5:
            return_val = 3
        elif angle < 112.5:
            return_val = 4
        elif angle < 157.5:
            return_val = 5

        return return_val
