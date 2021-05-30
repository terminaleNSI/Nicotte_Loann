# -*- coding: utf-8 -*-
"""
Created on Mon May 10 15:13:34 2021

@author: Elève
"""

import pygame
import images as img
import math
import chest
import fonctions_utiles as FU
import random as rdm

class Wyvern(pygame.sprite.Sprite):
    def __init__(self, jeu, vie):
        self.jeu = jeu
        self.name = "wyvern"

        self.images = img.wyvern
        self.health_bar = img.health_bar
        self.health_bar.append(
            self.health_bar[1].subsurface([0,
                                           0,
                                           ((self.health_bar[1].get_width() - FU.convert(40)) * vie / 150),
                                           self.health_bar[1].get_height()]).convert_alpha())
        self.direction = 0
        self.action = "hover"
        self.move_pos = None
        self.n_image = 0
        self.last_image = pygame.time.get_ticks()
        self.last_action = pygame.time.get_ticks()

        self.image = self.images[self.action][self.n_image][self.direction]

        self.rect = self.image.get_rect()
        self.rect.center = (self.jeu.screen.get_width() / 2,
                            self.jeu.screen.get_height() * 0.25)

        self.x, self.y = self.rect.center
        self.deplacement = 0

        self.vie = vie

    def display(self):
        self.image = self.images[self.action][self.n_image][self.direction]
        self.jeu.screen.blit(self.image, self.rect.topleft)
        self.display_life()

    def display_life(self):
        x = self.jeu.screen.get_width() / 2 - self.health_bar[0].get_width() / 2
        self.jeu.screen.blit(self.health_bar[0], (x, FU.convert(20)))
        self.jeu.screen.blit(self.health_bar[2], (x, FU.convert(20)))


    def update(self, time):
        x = self.jeu.player.rect.centerx - self.rect.centerx
        y = self.jeu.player.rect.centery - self.rect.centery

        if self.action == 'hover':
            if self.last_image + 90 < time:
                self.direction = self.get_direction(math.degrees(math.atan2(y, x)))
                self.n_image += 1
                self.last_image = time
                if self.n_image == 8:
                    self.n_image = 0

        elif self.action == 'die':
            if self.last_image + 90 + math.exp(self.n_image) < time:
                self.n_image += 1
                self.last_image = time
                if self.n_image == 8:
                    self.jeu.wyverns.remove(self)

        elif self.action == 'hit':
            if self.last_image + 90< time:
                self.n_image += 1
                self.last_image = time
                if self.n_image == 8:
                    self.action = 'hover'
                    self.n_image = 0

        elif self.action == 'fly':
            if self.move_pos:
                x = self.move_pos[0] - self.rect.centerx
                y = self.move_pos[1] - self.rect.centery
                angle = math.atan2(y, x)
                print(FU.get_pos_salle(self.move_pos[0], self.move_pos[1]))
                print(math.degrees(angle))
                self.direction = self.get_direction(math.degrees(angle))

                self.x += math.cos(angle)
                self.y += math.sin(angle)
                print((math.cos(math.radians(angle)), math.sin(math.radians(angle))))

                self.rect.center = self.x, self.y

                if math.sqrt(((self.x - self.move_pos[0]) **2) + ((self.y - self.move_pos[1])**2)) < FU.convert(50):
                    self.move_pos = None
                    self.action = "hover"

            if self.last_image + 90 < time:
                self.n_image += 1
                self.last_image = time
                if self.n_image == 8:
                    self.n_image = 1

                if self.deplacement > FU.convert(100):
                    self.deplacement = 0
                    self.action = 'hover'

        self.update_action()



    def kill(self):
        self.n_image = 0
        self.action = 'die'
        self.jeu.chest.append(chest.Chest(self.jeu,
                                          self.rect.centerx,
                                          self.rect.centery,
                                          [rdm.randint(0, 32) for i in range(3)]))

    def get_direction(self, angle):
        return_val = 0
        if angle > 157.5 or angle < -157.5:
            return_val = 0
        elif angle < -112.5:
            return_val = 1
        elif angle < -67.5:
            return_val = 2
        elif angle < -22.5:
            return_val = 3
        elif angle < 22.5:
            return_val = 4
        elif angle < 67.5:
            return_val = 5
        elif angle < 112.5:
            return_val = 6
        elif angle < 157.5:
            return_val = 7

        return return_val

    def update_action(self):
        if self.action != "die":
            if self.last_action + 5000 < pygame.time.get_ticks():
                self.last_action = pygame.time.get_ticks()
                pos = rdm.choice(self.jeu.spawnable)

                self.goto(FU.get_pos_screen(pos[0], pos[1]))

    def goto(self, pos):
        self.move_pos = (pos[0], pos[1])
        self.action = "fly"

    def take_domage(self, jeu, quantity):
        self.vie -= quantity
        if self.vie <= 0:
            self.kill()
        else:
            self.health_bar[2] =\
                self.health_bar[1].subsurface([0,
                                               0,
                                               ((self.health_bar[1].get_width() - FU.convert(40)) * self.vie / 150),
                                               self.health_bar[1].get_height()]).convert_alpha()
