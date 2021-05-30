# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 11:25:29 2021

@author: loann
"""
import pygame
import images as img
import fonctions_utiles as FU


class Map:
    def __init__(self, jeu):
        self.jeu = jeu
        self.centerx = FU.convert(1696)
        self.centery = FU.convert(811)
        self.img = img.carte
        self.blip = img.player_blip

    def display(self, player, screen, golems, slimes):
        x = (self.centerx - FU.convert(250) * (self.jeu.salle[1] + 1) -
             ((player.rect.centerx - FU.convert(448)) * 250 / 1174))
        y = (self.centery - FU.convert(250) * (self.jeu.salle[0] + 1) -
             ((player.rect.centery - FU.convert(28)) * 250 / 1174))

        screen.blit(self.img, (x, y))
        screen.blit(self.blip[player.direction],
                    (self.centerx - FU.convert(10),
                     self.centery - FU.convert(10)))
        mobs = golems + slimes
        for mob in mobs:
            x = (self.centerx + (mob.rect.centerx -
                                 player.rect.centerx) * 250 / 1174)
            y = (self.centery + (mob.rect.centery -
                                 player.rect.centery) * 250 / 1174)

            pygame.draw.circle(screen, (255, 0, 0), (x, y), FU.convert(3))
