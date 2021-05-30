# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 12:48:09 2021

@author: loann
"""
import pygame
import math
import loot
import images as img
import fonctions_utiles as FU
import random as rdm
import animation as anim


class Golem(pygame.sprite.Sprite):
    def __init__(self, ms, jeu):
        super().__init__()
        self.name = "golem"
        self.screen = jeu.screen
        self.jeu = jeu
        self.time = ms

        self.vie = 3
        self.speed = 1.2

        self.direction = 0

        self.images = img.img_golem
        self.n_image = 0

        self.image = self.images["idle"][0][0]
        self.rect = self.image.get_rect()
        pos = rdm.choice(jeu.spawnable)
        pos = FU.get_pos_screen(pos[0], pos[1])

        self.rect.bottom = pos[1]
        self.rect.left = pos[0]

        self.x = self.rect.left
        self.y = self.rect.top

        self.action = "idle"

        self.bumped = False
        self.nb_bump = 0
        self.bumbed_direction = 0

    def display(self):
        self.image = self.images[self.action][self.direction][self.n_image]

        self.screen.blit(self.image, self.rect.topleft)

    def display_hitbox(self):
        pygame.draw.circle(self.screen, (0, 255, 0), self.get_center_screen(),
                           FU.convert(400), 1)
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect, 1)

    def update(self, ms):
        if not self.bumped:
            if self.action != "die" and self.action != "atk":
                if (FU.get_distance(self.jeu.player, self) < FU.convert(400) and
                        not self.jeu.player.bumped):
                    if FU.get_distance(self.jeu.player, self) > 50:
                        pos_p = self.jeu.player.get_center_screen()
                        pos_g = self.get_center_screen()
                        x = pos_p[0] - pos_g[0]
                        y = pos_p[1] - pos_g[1]
                        direction = math.degrees(math.atan2(y, x))
                        self.moove(direction)
                        self.action = "walk"
                    elif self.action != "atk":
                        self.n_image = 0
                        self.action = "atk"

                else:
                    self.action = "idle"
                    self.direction = 0
                    if self.n_image > 1:
                        self.n_image = 0

            if self.action == "idle":
                if self.time + 250 < ms:
                    self.time = ms
                    self.n_image += 1
                    if self.n_image == 2:
                        self.n_image = 0

            elif self.action == "atk":
                if self.time + 150 < ms:
                    self.time = ms
                    self.n_image += 1
                    if self.n_image == 5:
                        pos_g = self.get_center_screen()
                        pos_p = self.jeu.player.get_center_screen()
                        x = pos_p[0] - pos_g[0]
                        y = pos_p[1] - pos_g[1]
                        direction = math.atan2(y, x)
                        if FU.get_distance(self.jeu.player, self) < 100:
                            self.jeu.anim_atk.append(
                                anim.Animation(img.spikes_atk[
                                    rdm.randint(0, 3)],
                                    pos_p[0] +
                                    math.cos(direction) * 25,
                                    pos_p[1] +
                                    math.sin(direction) * 25,
                                    ms, 80, "spike_atk", "Center"))
                            self.jeu.player.take_domage_golem(direction)
                        else:
                            self.jeu.anim_atk.append(
                                anim.Animation(img.spikes_atk[
                                    rdm.randint(0, 3)],
                                    pos_g[0] +
                                    math.cos(direction) * 35,
                                    pos_g[1] +
                                    math.sin(direction) * 35,
                                    ms, 80, "spike_atk", "Center"))

                    elif self.n_image == 7:
                        self.n_image = 0
                        self.action = "walk"

            else:
                if self.time + 110 < ms:
                    self.time = ms
                    self.n_image += 1
                    if self.n_image == 7:
                        self.n_image = 0
                        if self.action == "die":
                            self.jeu.golems.remove(self)
                            self.drop_loot()

        else:
            if self.time + 40 < ms:
                self.nb_bump += 1
                x_up = math.cos(self.bumbed_direction) * 8
                y_up = math.sin(self.bumbed_direction) * 8
                self.time = ms

                if (FU.get_pos_salle(self.rect.right + x_up,
                                     self.rect.bottom + y_up)
                        not in self.jeu.pos_walls and
                    FU.get_pos_salle(self.rect.left + x_up,
                                     self.rect.top - self.rect.height * 1/3
                                     + y_up)
                        not in self.jeu.pos_walls):
                    self.x += x_up
                    self.y += y_up

                    self.rect.left = self.x
                    self.rect.top = self.y

                if self.nb_bump == 10:
                    self.nb_bump = 0
                    self.bumped = False

        self.display_life()

    def moove(self, direction):
        if -45 <= direction <= 45:
            self.direction = 3
        elif 45 <= direction <= 135:
            self.direction = 2
        elif 135 <= direction or -135 >= direction:
            self.direction = 1
        else:
            self.direction = 0

        self.x += math.cos(math.radians(direction)) * self.speed
        self.y += math.sin(math.radians(direction)) * self.speed

        self.rect.left = self.x
        self.rect.top = self.y

    def display_life(self):
        FU.draw_rect_alpha(self.jeu.screen, (0, 0, 0, 100),
                           [self.rect.left + FU.convert(20),
                            self.rect.bottom,
                            FU.convert(78),
                            FU.convert(10)])

        FU.draw_rect_alpha(self.jeu.screen, (0, 255, 0, 100),
                           [self.rect.left + FU.convert(22),
                            self.rect.bottom + FU.convert(2),
                            FU.convert(74) * self.vie / 3,
                            FU.convert(6)])

    def get_center_screen(self):
        return (int(self.rect.left + self.rect.width / 2),
                int(self.rect.top + self.rect.height * 2 / 3))

    def kill(self):
        self.action = "die"
        self.n_image = 0
        self.direction = 0

    def hit_spear_dagger(self, player):
        if ((player.last_anim == "spear" and player.n_image == 5 and
             FU.get_distance(player, self) < 80) or
                (player.last_anim == "dagger" and player.n_image == 5 and
                 FU.get_distance(player, self) < 60) and
                abs(player.direction - self.direction) == 2):
            pos_p = player.get_center_screen()
            pos_g = self.get_center_screen()
            x = pos_p[0] - pos_g[0]
            y = pos_p[1] - pos_g[1]
            if not self.bumped:
                self.vie -= 1
            self.bumbed_direction = math.radians(
                (math.degrees(math.atan2(y, x)) + 360) - 180)
            self.bumped = True
            self.n_image = 0
            self.action = "walk"
            if self.vie <= 0:
                self.kill()

    def bump_arrow(self, arrow):
        self.bumped = True
        self.bumbed_direction = math.radians(arrow.angle)
        self.n_image = 0
        self.action = "walk"

    def drop_loot(self):
        for i in range(rdm.randint(1, 3)):
            center = self.get_center_screen()
            d = rdm.randint(0, 60)
            a = rdm.randint(0, 360)
            x = center[0] + math.cos(math.radians(a)) * d
            y = center[1] + math.sin(math.radians(a)) * d
            self.jeu.loot.append(loot.Loot(self.jeu, "iron_ingot", x, y))
