# -*- coding: utf-8 -*-
"""
Created on Thu May 20 15:07:07 2021

@author: Elève
"""

import fonctions_utiles as FU
import images as img
import pygame

class Enigme_pressure_plate:
    def __init__(self, jeu):
        self.jeu = jeu
        self.pos = [(7, 4), (11, 9), (4, 6), (4, 9), (11, 6), (8, 11)]
        self.images = img.pressure_plate
        self.pressed = [False for i in range(6)]
        self.order = []
        self.time_all_pressed = None
        self.completed = False


    def display(self):
        for i in range(6):
            if self.pressed[i]:
                self.jeu.screen.blit(self.images[1][i], FU.get_pos_screen(self.pos[i][0], self.pos[i][1]))
            else:
                self.jeu.screen.blit(self.images[0][i], FU.get_pos_screen(self.pos[i][0], self.pos[i][1]))

    def update(self):
        time = pygame.time.get_ticks()
        if not self.completed:
            pos = self.jeu.player.get_center_salle()
            if pos in self.pos:
                index = self.pos.index(pos)
                if not self.pressed[index]:
                    self.pressed[index] = True
                    self.order.append(index + 1)
                    if len(self.order) == 6:
                        self.time_all_pressed = time

            if len(self.order) == 6:
                if self.order == [1, 2, 3, 4, 5, 6]:
                    self.completed = True

                elif self.time_all_pressed + 1500 < time:
                    self.reset()

                else:
                    self.jeu.screen.blit(FU.pp_failed, (self.jeu.screen.get_width() / 2 -
                                            FU.pp_failed.get_width() / 2,
                                            3 * self.jeu.screen.get_height() / 4))

        elif self.time_all_pressed + 10000 < time:
            self.reset()

        elif self.time_all_pressed + 5000 > time:
            self.jeu.screen.blit(FU.pp_completed, (self.jeu.screen.get_width() / 2 -
                                            FU.pp_completed.get_width() / 2,
                                            3 * self.jeu.screen.get_height() / 4))

    def reset(self):
        self.pressed = [False for i in range(6)]
        self.order = []
        self.time_all_pressed = None
        self.completed = False
