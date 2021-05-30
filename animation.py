# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 22:54:05 2021

@author: loann
"""
import fonctions_utiles as FU
import pygame


class Animation:

    def __init__(self, images, x, y, ms, delay=100, mode=None, display_mode="Corner"):

        self.images = images
        self.rect = images[0].get_rect()
        self.display_mode = display_mode

        if self.display_mode == "Corner":
            self.rect.topleft = x, y
        elif self.display_mode == "Center":
            self.rect.center = x, y

        self.n_image = 0
        self.delay = delay
        self.default_delay = self.delay
        self.last_play = ms
        self.mode = mode
        self.active = False
        self.angle = 0
        self.origin_image = self.images[0]

    def update(self, screen, ms, jeu=None):
        if self.mode == "spike":
            screen.blit(self.images[self.n_image], self.rect.topleft)

            if self.last_play + self.delay < ms:
                self.last_play = ms
                self.delay = self.default_delay
                self.n_image += 1
                self.active = False
                if self.n_image == len(self.images):
                    self.n_image = 0
                    self.delay = 2000
                    self.active = False
                elif self.n_image == 1:
                    self.delay = 1000
                    self.active = True

        elif self.mode == "rotate":
            screen.blit(self.images[0], self.rect.topleft)
            if self.last_play + self.delay < ms:
                self.last_play = ms
                self.angle += 10
                self.images[0] = pygame.transform.rotozoom(self.origin_image, self.angle, 1).convert_alpha()
                self.rect = self.images[0].get_rect(center=self.rect.center)


        else:
            screen.blit(self.images[self.n_image], self.rect.topleft)

            if self.last_play + self.delay < ms:
                self.last_play = ms
                self.n_image += 1
                if self.n_image == len(self.images):
                    self.n_image = 0
                    if self.mode == "spike_atk":
                        jeu.anim_atk.remove(self)
