# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 12:24:25 2021

@author: loann
"""
import images as img


class AnimDoor:
    def __init__(self):
        self.play = False
        self.active = False
        self.full = False
        self.w = 10

        self.img = img.images_porte

    def display(self, screen):
        screen.blit(self.img[0], (-screen.get_width() / 2 + self.w, 0))
        screen.blit(self.img[1], (screen.get_width() - self.w, 0))

        if not self.full:
            self.w += 10
            if self.w >= screen.get_width() / 2:
                self.full = True
                self.active = True
        else:
            self.active = False
            self.w -= 10
            if self.w <= 0:
                self.play = False
                self.full = False
                self.w = 10
