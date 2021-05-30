# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 15:24:24 2021

@author: loann
"""
import pygame
import fonctions_utiles as FU
import math


class Arrow(pygame.sprite.Sprite):
    def __init__(self, posx, posy, angle, ms, speed = 7, shooter = "player"):
        super().__init__()
        self.angle = angle
        self.shooter = shooter
        self.image = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load("assets/player/arrow.png"), (FU.convert(31), 5)), -angle)
        self.rect = self.image.get_rect()
        self.rect.center = (posx, posy)
        self.points = []

        self.speed = speed
        self.travel = True
        self.shoot = ms

        self.x, self.y = self.rect.center

    def display(self, screen, player, inv, ms, jeu):

        if self.travel:
            self.x += math.cos(math.radians(self.angle)) * self.speed
            self.y += math.sin(math.radians(self.angle)) * self.speed

            self.rect.center = self.x, self.y

            for pos in self.points:
                pygame.draw.circle(screen, (130, 130, 130), (pos), 1)

            if (FU.get_pos_salle(self.rect.topleft[0],
                                 self.rect.topleft[1]) in jeu.pos_walls or
                FU.get_pos_salle(self.rect.topright[0],
                                 self.rect.topright[1]) in jeu.pos_walls or
                FU.get_pos_salle(self.rect.bottomright[0],
                                 self.rect.bottomright[1]) in jeu.pos_walls or
                    FU.get_pos_salle(self.rect.bottomleft[0],
                                     self.rect.bottomright[1]) in jeu.pos_walls):
                self.travel = False

        else:
            if pygame.sprite.collide_mask(self, player):
                self.kill(jeu)
                inv.aug_arrow(1)

            if self.shoot + 10000 < ms and self in jeu.arrows:
                self.kill(jeu)

        screen.blit(self.image, (self.rect.x, self.rect.y))
        self.points.append(self.rect.center)

        if len(self.points) > 5:
            self.points.pop(0)

    def display_hitbox(self, screen, ms):
        pygame.draw.rect(screen, (0, 0, 255), self.rect, 1)

    def kill(self, jeu):
        if self in jeu.arrows:
            jeu.arrows.remove(self)

    def check_hit(self, jeu):
        for entity in jeu.get_alive():
            if self.travel and pygame.sprite.collide_mask(entity, self):
                if self.shooter == "player":
                    if entity.name == "slime" and not entity.anim_death:
                        self.kill(jeu)
                        entity.kill()

                    elif entity.name == "golem" and entity.action != "die":
                        self.kill(jeu)
                        entity.vie -= 1
                        if entity.vie <= 0:
                            entity.kill()
                        else:
                            entity.bump_arrow(self)

                    elif entity.name == "archer" and entity.action != "die":
                        self.kill(jeu)
                        entity.kill()

                    elif entity.name == "wyvern" and entity.action != "die":
                        self.kill(jeu)
                        entity.take_domage(jeu, 2)

                else:
                    if entity.name == "player":
                        self.kill(jeu)
                        entity.take_domage_golem(math.radians(self.angle))
