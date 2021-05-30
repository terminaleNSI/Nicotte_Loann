# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 16:24:28 2021

@author: loann
"""

import pygame
import carte
import chat
import player as pl
import animDoor
import animation
import inventaire
import game
import images as img
import fonctions_utiles as FU
import slime
import golem
import loot
import arrow
import archer
import spawner
import wyvern
import chest
import enigme_pressure_plate


class Jeu:
    def __init__(self, player_imgs):
        self.screen = img.screen
        self.clock = pygame.time.Clock()

        self.play = True
        self.caps_lock = False
        self.salle = (1, 0)
        self.slimes = []
        self.golems = []
        self.archer = []
        self.wyverns = []
        self.loot = []
        self.chest = []

        self.key_pressed = []

        self.arrows = []
        self.anim_atk = []

        self.enigme_pp = enigme_pressure_plate.Enigme_pressure_plate(self)

        self.inv = inventaire.inventaire(self.screen)
        self.player = pl.Player(self.inv, player_imgs, self)
        self.anim_door = animDoor.AnimDoor()
        self.console = chat.Console(FU.convert(1500), FU.convert(28),
                                    FU.convert(393),
                                    FU.screen.get_height() / 2 -
                                    FU.convert(28), self)

        self.pos_spawnable, self.hitbox_player = False, False
        self.hitbox_slime, self.hitbox_arrow = False, False
        self.show_inv, self.hitbox_golem = False, False
        self.time = pygame.time.get_ticks()
        self.last_save = self.time
        self.mape = carte.Map(self)

        (self.pos_walls, self.pos_coffres, self.pos_portes, self.spikes,
         self.torches, self.spawnable, self.spawners) = [], [], [], [], [], [], []

    def init_game(self, run):

        fichier = open("assets/save/player.txt", "r")
        lst = fichier.read()
        lst = lst.split("\n")
        for i in range(len(lst)):
            lst[i] = lst[i].split(" ")

        for i in lst:
            if i[0] == "salle":
                self.salle = int(i[1][1]), int(i[2][0])

            elif i[0] == "playerx":
                self.player.rect.centerx = FU.convert(int(i[1]))

            elif i[0] == "playery":
                self.player.rect.centery = FU.convert(int(i[1]))

            elif i[0] == "playervie":
                self.player.vie = int(i[1])

            elif i[0] == "playermaxvie":
                self.player.max_vie = int(i[1])

            elif i[0] == "playerbody" and i[1] != "None":
                self.inv.body = i[1]

        self.init_salle()


        fichier.close()
        pygame.display.set_caption("Dongeon Game")
        run = game.game(self, run)

        return run

    def save_game(self):
        self.save_player()
        self.inv.save_inventory()
        self.save_entity(self.salle)

    def save_player(self):
        fichier = open("assets/save/player.txt", "w")
        fichier.write(f"salle {self.salle[0],self.salle[1]}\n")
        fichier.write(f"playerx {FU.convert_inv(self.player.rect.centerx)}\n")
        fichier.write(f"playery {FU.convert_inv(self.player.rect.centery)}\n")
        fichier.write(f"playervie {self.player.vie}\n")
        fichier.write(f"playermaxvie {self.player.max_vie}\n")
        fichier.write(f"playerbody {self.inv.body}")
        fichier.close()

    def auto_save(self):
        if self.last_save + 10000 < pygame.time.get_ticks():
            self.save_game()
            self.last_save = pygame.time.get_ticks()

    def save_entity(self, salle):
        ms = pygame.time.get_ticks()
        fichier = open(f"assets/save/entity/{salle[1]}-{salle[0]}.txt", "w")
        for entity in self.get_entity():
            if isinstance(entity, slime.Slime):
                fichier.write(
                    f"slime {FU.convert_inv(entity.rect.centerx)} {FU.convert_inv(entity.rect.centery)} {entity.couleur}\n")

            elif isinstance(entity, golem.Golem):
                fichier.write(
                    f"golem {FU.convert_inv(entity.rect.centerx)} {FU.convert_inv(entity.rect.centery)} {entity.vie}\n")

            elif isinstance(entity, loot.Loot):
                fichier.write(
                    f"loot {FU.convert_inv(entity.rect.centerx)} {FU.convert_inv(entity.rect.centery)} {entity.name} {entity.quantity}\n")

            elif isinstance(entity, arrow.Arrow):
                fichier.write(
                    f"arrow {FU.convert_inv(entity.rect.centerx)} {FU.convert_inv(entity.rect.centery)} {entity.angle} {ms - entity.shoot}\n")

            elif isinstance(entity, archer.Archer):
                fichier.write(
                    f"archer {FU.convert_inv(entity.rect.centerx)} {FU.convert_inv(entity.rect.centery)}\n")

            elif isinstance(entity, chest.Chest):
                fichier.write(
                    f"chest {FU.convert_inv(entity.x)} {FU.convert_inv(entity.y)} {entity.open} {entity.items}\n")

        if salle == (0, 2):
            fichier = open("assets/save/boss.txt", "w")
            if self.wyverns:
                fichier.write(f"wyvern true {self.wyverns[0].vie}\n")
            else:
                fichier.write("wyvern false 0\n")

    def load_entity(self, salle):
        time = pygame.time.get_ticks()
        fichier = open(f"assets/save/entity/{salle[1]}-{salle[0]}.txt", "r")
        lst = fichier.read()
        lst = lst.split('\n')
        for i in range(len(lst)):
            lst[i] = lst[i].split(" ")

            if lst[i][0] == 'slime':
                nslime = slime.Slime(time, self)
                nslime.rect.center = (FU.convert(int(lst[i][1])),
                                      FU.convert(int(lst[i][2])))
                nslime.couleur = int(lst[i][3])
                self.slimes.append(nslime)

            elif lst[i][0] == 'golem':
                ngolem = golem.Golem(time, self)
                ngolem.rect.center = (FU.convert(int(lst[i][1])),
                                      FU.convert(int(lst[i][2])))
                ngolem.x, ngolem.y = ngolem.rect.topleft
                ngolem.vie = int(lst[i][3])
                self.golems.append(ngolem)

            elif lst[i][0] == 'archer':
                narcher = archer.Archer(self)
                narcher.rect.center = (FU.convert(int(lst[i][1])),
                                       FU.convert(int(lst[i][2])))
                narcher.x, narcher.y = narcher.rect.topleft
                self.archer.append(narcher)

            elif lst[i][0] == 'loot':
                nloot = loot.Loot(self, lst[i][3], FU.convert(int(lst[i][1])),
                                  FU.convert(int(lst[i][2])), int(lst[i][4]))
                self.loot.append(nloot)

            elif lst[i][0] == 'arrow':
                narrow = arrow.Arrow(FU.convert(int(lst[i][1])),
                                     FU.convert(int(lst[i][2])),
                                     float(lst[i][3]), time)
                self.arrows.append(narrow)

            elif lst[i][0] == 'chest':
                nchest = chest.Chest(self,
                                     FU.convert(int(lst[i][1])),
                                     FU.convert(int(lst[i][2])),
                                     FU.get_list(lst[i][4:]),
                                     open = lst[i][3])
                self.chest.append(nchest)

        if salle == (0, 2):
            fichier = open("assets/save/boss.txt", "r")
            lst = fichier.read()
            lst = lst.split('\n')
            for i in range(len(lst)):
                lst[i] = lst[i].split(" ")

            if lst[0][1] == "true":
                self.wyverns.append(wyvern.Wyvern(self, int(lst[0][2])))

    def reset_entity(self):
        self.slimes = []
        self.golems = []
        self.loot = []
        self.arrows = []
        self.archer = []
        self.wyverns = []
        self.chest = []

    def get_entity(self):
        return self.slimes + self.golems + self.loot + self.arrows + self.archer + self.wyverns + self.chest

    def get_alive(self):
        return self.slimes + self.golems + self.archer + [self.player] + self.wyverns

    def display_salle(self):
        self.screen.blit(img.salles[self.salle[0]][self.salle[1]],
                         (FU.convert(448), FU.convert(28)))

        if self.salle == (1, 2):
            self.enigme_pp.display()
            self.enigme_pp.update()

    def display_open_porte(self):
        if not self.wyverns and self.copleted_pp():
            self.screen.blit(FU.txt_porte, (self.screen.get_width() / 2 -
                                            FU.txt_porte.get_width() / 2,
                                            2 * self.screen.get_height() / 3))

        elif not self.copleted_pp():
            self.screen.blit(FU.pp_porte, (self.screen.get_width() / 2 -
                                            FU.pp_porte.get_width() / 2,
                                            2 * self.screen.get_height() / 3))

        elif self.wyverns:
            self.screen.blit(FU.boss_porte, (self.screen.get_width() / 2 -
                                            FU.boss_porte.get_width() / 2,
                                            2 * self.screen.get_height() / 3))

    def display_open_coffre(self):
        self.screen.blit(FU.txt_coffre, (self.screen.get_width() / 2 -
                                         FU.txt_porte.get_width() / 2,
                                         2 * self.screen.get_height() / 3))

    def display_fps(self):
        FPS = FU.font_fps.render(
            f"{round(self.clock.get_fps())} FPS", True, (100, 100, 100))
        self.screen.blit(FPS, (4, 4))

    def init_salle(self):
        self.reset_entity()
        plan = FU.get_plan(self.salle)
        (self.pos_walls, self.pos_coffres, self.pos_portes, self.spikes,
         self.torches, self.spawnable, self.spawners) = [], [], [], [], [], [], []

        for i in range(len(plan)):
            for j in range(len(plan[i])):
                pos = FU.get_pos_screen(j, i)

                if plan[i][j] == 'P':
                    self.pos_portes.append((j, i))

                elif plan[i][j] == '^':
                    self.torches.append(
                        animation.Animation(img.images_torches_up,
                                            pos[0] +
                                            FU.convert(25),
                                            pos[1] +
                                            FU.convert(11),
                                            pygame.time.get_ticks()))

                elif plan[i][j] == '>':
                    self.torches.append(
                        animation.Animation(img.images_torches_right,
                                            pos[0] +
                                            FU.convert(50),
                                            pos[1] +
                                            FU.convert(10),
                                            pygame.time.get_ticks()))

                elif plan[i][j] == '<':
                    self.torches.append(
                        animation.Animation(img.images_torches_left,
                                            pos[0],
                                            pos[1] +
                                            FU.convert(10),
                                            pygame.time.get_ticks()))

                elif plan[i][j] == 'S':
                    pos = FU.get_pos_screen(j, i)
                    self.spikes.append(
                        animation.Animation(img.images_spikes,
                                            pos[0], pos[1],
                                            pygame.time.get_ticks(),
                                            100, "spike"))

                elif plan[i][j] == 'M':
                    pos = FU.get_pos_screen(j, i)
                    self.spawners.append(
                        spawner.Spawner(self, pos[0], pos[1], "slime", 10000,
                                        pygame.time.get_ticks()))
                    self.pos_walls.append((j, i))

                elif plan[i][j] == 'X':
                    self.pos_walls.append((j, i))

                elif plan[i][j] == 'C':
                    self.pos_coffres.append((j, i))

                elif plan[i][j] == "1":
                    self.spawnable.append((j, i))

        self.load_entity(self.salle)

    def copleted_pp(self):
        return not(self.salle == (1, 2) and not self.enigme_pp.completed)

    def display_all(self):
        display = ([self.player] + self.slimes + self.golems +
                   self.arrows + self.anim_atk + self.loot + self.archer +
                   self.wyverns + self.chest)
        for i in range(len(display)):
            for j in range(len(display)):
                if display[i].rect.bottom < display[j].rect.bottom:
                    display[i], display[j] = display[j], display[i]

        time = pygame.time.get_ticks()
        for mob in display:
            if isinstance(mob, pl.Player):
                mob.display(self.screen, time, self.show_inv, self.console.open)
                if self.hitbox_player:
                    self.player.display_hitbox(self.screen)

            elif isinstance(mob, arrow.Arrow):
                mob.display(self.screen, self.player, self.inv, time, self)
                mob.check_hit(self)
                if self.hitbox_arrow:
                    arrow.display_hitbox(self.screen, time)

            elif isinstance(mob, golem.Golem):
                mob.display()
                if not self.anim_door.play and not self.player.die:
                    mob.update(time)
                mob.hit_spear_dagger(self.player)
                if self.hitbox_golem:
                    mob.display_hitbox()

            elif isinstance(mob, slime.Slime):
                mob.display()
                if not self.anim_door.play and not self.player.die:
                    mob.update(time)
                mob.hit_spear_dagger(self.player)
                if self.hitbox_slime:
                    mob.display_hitbox()

            elif isinstance(mob, animation.Animation):
                mob.update(self.screen, time, self)

            elif isinstance(mob, archer.Archer):
                mob.display()
                if not self.anim_door.play and not self.player.die:
                    mob.update(time)

            elif isinstance(mob, loot.Loot):
                mob.display(self.screen)

            elif isinstance(mob, wyvern.Wyvern):
                mob.display()
                if not self.anim_door.play and not self.player.die:
                    mob.update(time)

            elif isinstance(mob, chest.Chest):
                mob.display()
                if not self.anim_door.play and not self.player.die:
                    mob.update()

        for coffre in self.chest:
            coffre.display_loot()

        if self.player.die:
            if self.player.die_time + 4000 > pygame.time.get_ticks():
                s = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
                s.fill((0, 0, 0))
                s.set_alpha((pygame.time.get_ticks() - self.player.die_time) * 255 / 2000)
                self.screen.blit(s, (0, 0))

                s = FU.you_die
                s.set_alpha((pygame.time.get_ticks() - self.player.die_time) * 255 / 2000)
                self.screen.blit(s, ((self.screen.get_width() - FU.you_die.get_width()) / 2, (self.screen.get_height() - FU.you_die.get_height()) / 2))
            else:
                FU.reset_save()
                self.init_salle()
                self.inv.init_inventory()
                self.inv.init_stuff()
