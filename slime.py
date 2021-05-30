# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 17:12:36 2021
@author: loann
"""
import math
import loot
import pygame
import images as img
import fonctions_utiles as FU
import random as rdm


class Slime(pygame.sprite.Sprite):
    def __init__(self, ms, jeu):
        super().__init__()
        self.name = "slime"
        self.jeu = jeu
        self.screen = self.jeu.screen

        lens = FU.convert(128)
        pos = rdm.choice(jeu.spawnable)
        pos = FU.get_pos_screen(pos[0], pos[1])
        posx = pos[0] - FU.convert(lens) * 5/12
        posy = pos[1] - lens / 2 - FU.convert(64) * 1/6
        self.anim_jump = False
        self.anim_roulade = False
        self.anim_shoot = False
        self.anim_death = False

        self.dead = False

        self.couleur = rdm.randint(0, 3)

        self.angle = 0

        self.last_jump = ms
        self.last_shoot = ms

        self.images = img.images_slime
        self.image = self.images[0 + 5 * self.couleur][0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (posx, posy)

        self.n_image = 0
        self.last_play = ms

    def display(self):
        self.screen.blit(self.image, self.rect.topleft)

    def update(self, ms):
        if self.anim_death:
            self.image = self.images[4 + 5 * self.couleur][self.n_image]

        elif self.anim_shoot:
            self.image = self.images[3 + 5 * self.couleur][self.n_image]

        elif self.anim_roulade:
            self.image = self.images[1 + 5 * self.couleur][self.n_image]

        elif self.anim_jump:
            self.image = self.images[2 + 5 * self.couleur][self.n_image]

        else:
            self.image = self.images[0 + 5 * self.couleur][self.n_image]

        if ms > self.last_jump + 1300:
            self.jump(ms)

        if self.last_play + 80 < ms:
            self.n_image += 1
            self.last_play = ms
            coef = 6
            if self.anim_death:
                pass

            elif self.anim_roulade and not self.anim_shoot:
                self.rect.top += FU.convert(10)

            elif self.anim_jump and not self.anim_shoot:
                distance = (-(coef/80000) * ((80 * self.n_image) ** 2) +
                            coef/100 * (80 * self.n_image))

                self.rect.left += math.cos(math.radians(self.angle)
                                           ) * FU.convert(distance)
                self.rect.top += math.sin(math.radians(self.angle)
                                          ) * FU.convert(distance)

            if self.n_image == 10:
                if self.anim_death:
                    self.jeu.slimes.remove(self)
                    self.drop_loot()
                self.anim_jump = False
                self.anim_roulade = False
                self.anim_shoot = False
                self.n_image = 0


    def display_hitbox(self):
        pygame.draw.rect(self.screen, (255, 0, 0),
                         [self.rect.left + self.rect.width * 1/3,
                          self.rect.top + self.rect.height * 2/3,
                          self.rect.width * 1/3,
                          self.rect.width * 1/3], 1)

        pygame.draw.rect(self.screen, (0, 0, 255), self.rect, 1)

        pygame.draw.circle(self.screen, (255, 0, 0), self.rect.center, 2)

    def shoot(self, player, ms):
        self.n_image = 0
        self.anim_shoot = True

        self.last_shoot = ms

        player.take_damage(1)

    def jump(self, ms):
        if not self.anim_death:
            self.n_image = 0
            self.anim_jump = True
            self.last_jump = ms
            self.angle = rdm.randint(0, 360)

        movex = math.cos(math.radians(self.angle)) * FU.convert(90)
        movey = math.sin(math.radians(self.angle)) * FU.convert(90)

        pts = [FU.get_pos_salle(self.rect.left + self.rect.width * 1/3 + movex,
                                self.rect.top + self.rect.width * 2/3 + movey),
               FU.get_pos_salle(self.rect.left + self.rect.width * 1/3 + movex,
                                self.rect.top + self.rect.width + movey),
               FU.get_pos_salle(self.rect.left + self.rect.width * 2/3 + movex,
                                self.rect.top + self.rect.width * 2/3 + movey),
               FU.get_pos_salle(self.rect.left + self.rect.width * 2/3 + movex,
                                self.rect.top + self.rect.width + movey)]

        go = True

        for i in pts:
            if i in self.jeu.pos_walls:
                go = False

        while not go:
            go = True

            self.angle = rdm.randint(0, 360)

            movex = math.cos(math.radians(self.angle)) * FU.convert(90)
            movey = math.sin(math.radians(self.angle)) * FU.convert(90)

            pts = [FU.get_pos_salle(self.rect.left + self.rect.width * 1/3
                                    + movex,
                                    self.rect.top + self.rect.width * 2/3
                                    + movey),
                   FU.get_pos_salle(self.rect.left + self.rect.width * 1/3
                                    + movex,
                                    self.rect.top + self.rect.width + movey),
                   FU.get_pos_salle(self.rect.left + self.rect.width * 2/3
                                    + movex,
                                    self.rect.top + self.rect.width * 2/3
                                    + movey),
                   FU.get_pos_salle(self.rect.left + self.rect.width * 2/3
                                    + movex,
                                    self.rect.top + self.rect.width + movey)]

            for i in pts:
                if i in self.jeu.pos_walls:
                    go = False

    def roulade(self):
        self.n_image = 0
        self.anim_roulade = True

    def kill(self):
        self.n_image = 0
        self.anim_death = True

    def get_center_screen(self):
        return (self.rect.left + self.rect.width / 2,
                self.rect.top + self.rect.width * 5 / 6)

    def hit_spear_dagger(self, player):
        if ((player.last_anim == "spear" and player.n_image == 5 and
             FU.get_distance(player, self) < 80) or
                (player.last_anim == "dagger" and player.n_image == 5 and
                 FU.get_distance(player, self) < 60) and
                abs(player.direction - self.direction) == 2):

            self.kill()

    def drop_loot(self):
        for i in range(rdm.randint(1, 4)):
            name = rdm.choice(["stick", "string", "arrow", "flint"])
            center = self.get_center_screen()
            d = rdm.randint(0, 60)
            a = rdm.randint(0, 360)
            x = center[0] + math.cos(math.radians(a)) * d
            y = center[1] + math.sin(math.radians(a)) * d
            self.jeu.loot.append(loot.Loot(self.jeu, name, x, y))
