# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 10:44:52 2021

@author: Elève
"""
import pygame
import pyperclip
import slime
import golem
import archer
import wyvern
import images as img
import fonctions_utiles as FU


class Console:
    def __init__(self, posx, posy, width, height, jeu):
        self.jeu = jeu
        self.posx = int(posx)
        self.posy = int(posy)
        self.height = int(height)
        self.width = int(width)
        self.img_fond = pygame.transform.scale(img.flou,
                                               (self.width, self.height))
        self.img_entry = pygame.transform.scale(img.flou,
                                                (self.width, FU.convert(30)))
        self.rect = self.img_fond.get_rect()
        self.rect.topleft = (self.posx, self.posy)

        self.chat_txt = []
        self.open = False
        self.history = [""]

        self.font = pygame.font.SysFont(None, FU.convert(35))
        self.entry = ""
        self.n_history = 0

        self.n_entry = 0

        self.entry_txt = self.font.render(self.entry, True, (0, 0, 0))
        self.maj = {"<": ">", ",": "?", ";": ".", ":": "/", "!": "§", "ù": "%",
                    "*": "µ", "$": "£", "=": "+", ")": "°"}

        self.alt = {"$": "¤", "=": "}", ")": "]", '3': "#", "4": "{", "5": "[",
                    "6": "|", "0": "^"}
        self.not_maj = {"1": "&", "2": "é", "3": '"', "4": "'",
                        "5": "(", "6": "-", "7": "è", "8": "_", "9": "ç",
                        "0": "à", "²": "²"}

        self.last_del = 0

    def display(self, ms):
        self.jeu.screen.blit(self.img_fond, (self.posx, self.posy))
        self.display_entry(ms)
        self.display_chat()
        pygame.draw.line(self.jeu.screen, (0, 0, 0),
                         (self.rect.left,
                          self.rect.bottom - FU.convert(30)),
                         (self.rect.right,
                          self.rect.bottom - FU.convert(30)),
                         FU.convert(4))
        pygame.draw.rect(self.jeu.screen,  (0, 0, 0), self.rect, FU.convert(4))

    def display_entry(self, ms):
        if self.open:
            if self.entry_txt.get_width() + FU.convert(12) > self.width:
                x = self.rect.left - \
                    (self.entry_txt.get_width() - self.width + FU.convert(12))
                left = self.jeu.screen.subsurface(
                    [x, self.rect.bottom - FU.convert(30),
                     self.entry_txt.get_width() - self.width + FU.convert(12),
                     FU.convert(28)]).convert_alpha()
            else:
                x = self.rect.left
                left = None

            self.jeu.screen.blit(
                self.img_entry, (self.rect.bottomleft[0],
                                 self.rect.bottom - FU.convert(30)))

            self.jeu.screen.blit(self.entry_txt,
                                 (x + FU.convert(5),
                                  self.rect.bottomleft[1] - FU.convert(28)))

            if left:
                self.jeu.screen.blit(left, (x, self.rect.bottom -
                                            FU.convert(30)))

            if (ms // 500) % 2:
                if not left:
                    if len(self.entry):
                        x = (self.n_entry * self.entry_txt.get_width() /
                             len(self.entry) + FU.convert(6))
                    else:
                        x = FU.convert(6)

                    pygame.draw.line(self.jeu.screen, (20, 20, 20),
                                     (self.rect.left + x,
                                      self.rect.bottom - FU.convert(28)),
                                     (self.rect.left + x, self.rect.bottom
                                      - FU.convert(2)))
                else:
                    pygame.draw.line(self.jeu.screen, (20, 20, 20),
                                     (self.rect.right - FU.convert(6),
                                      self.rect.bottom - FU.convert(28)),
                                     (self.rect.right - FU.convert(6),
                                      self.rect.bottom - FU.convert(2)))

    def display_chat(self):
        for num, line in enumerate(self.chat_txt):
            self.jeu.screen.blit(line,
                                 (self.rect.bottomleft[0] + FU.convert(5),
                                  self.rect.bottomleft[1] -
                                  (2 + num) * FU.convert(26) - FU.convert(5)))

    def enter_key(self, key):

        if (pygame.K_RSHIFT in self.jeu.key_pressed or
            pygame.K_LSHIFT in self.jeu.key_pressed
                or self.jeu.caps_lock):
            if self.maj.get(key):
                self.add_char(self.maj.get(key))
            elif key.isdigit():
                self.add_char(key)
            elif key.isalpha() and len(key) == 1:
                self.add_char(key.upper())

        elif pygame.K_RALT in self.jeu.key_pressed:
            if self.alt.get(key):
                self.add_char(self.alt.get(key))

        elif pygame.K_LCTRL in self.jeu.key_pressed:
            if key == "c":
                pyperclip.copy(self.entry)
            elif key == "v":
                self.entry = pyperclip.paste()
                self.n_entry = len(self.entry)

        elif len(key) == 1:
            if key.isdigit():
                self.add_char(self.not_maj.get(key))
            else:
                self.add_char(key)

        elif len(key) == 3 and key[0] == "[" and key[2] == "]":
            self.add_char(key[1])

        elif key == "space":
            self.add_char(" ")

        elif key == "up":
            if self.n_history > 0:
                self.n_history -= 1
            self.entry = self.history[self.n_history]
            self.n_entry = len(self.entry)

        elif key == "down":
            if self.n_history < len(self.history) - 1:
                self.n_history += 1
            self.entry = self.history[self.n_history]
            self.n_entry = len(self.entry)

        elif key == "right":
            if self.n_entry < len(self.entry):
                self.n_entry += 1

        elif key == "left":
            if self.n_entry > 0:
                self.n_entry -= 1

        self.update_entry()

    def supr_entry(self):
        self.entry = ""
        self.update_entry()
        self.n_history = len(self.history) - 1
        self.n_entry = 0

    def execute_entry(self, inv, player, ms):
        if self.entry:
            self.entry = self.entry.lower()
            if self.entry[0] == "/":
                cmd = self.entry[1:].split(" ")

                if cmd[0] == "give":
                    if len(cmd) == 2:
                        cmd.append("1")
                    self.chat_txt.insert(0, self.font.render(
                        inv.give(cmd[1], cmd[2]), True, (0, 0, 0)))

                elif cmd[0] == "spawn":
                    if len(cmd) == 2:
                        cmd.append("1")
                    self.chat_txt.insert(0, self.font.render(
                        self.spawn(cmd[1], cmd[2], ms), True, (0, 0, 0)))

                elif cmd[0] == "heal":
                    self.chat_txt.insert(0, self.font.render(
                        player.heal(), True, (0, 0, 0)))

                elif cmd[0] == "killall":
                    self.chat_txt.insert(0, self.font.render(
                        self.killall(), True, (0, 0, 0)))

                elif cmd[0] == "collect":
                    self.chat_txt.insert(0, self.font.render(
                        self.collect(inv, cmd[1]), True, (0, 0, 0)))

                elif cmd[0] == "resetchest":
                    self.chat_txt.insert(0, self.font.render(
                        self.reset_chest(), True, (0, 0, 0)))

                else:
                    self.chat_txt.insert(0, self.font.render(
                        "[Error] Commande inconnue", True, (0, 0, 0)))



                if len(self.history) == 1 or self.history[-2] != self.entry:
                    self.history.pop(-1)
                    self.history.append(self.entry)
                    self.history.append("")
                    self.n_history = len(self.history) - 2

            else:
                self.chat_txt.insert(0, self.font.render(
                    self.entry, True, (0, 0, 0)))

            self.supr_entry()

    def delete_entry(self, ms):
        if self.n_entry > 0:
            self.entry = self.entry[:(self.n_entry - 1)] + \
                self.entry[self.n_entry:]
            self.update_entry()
            self.n_entry -= 1

    def update_entry(self):
        self.entry_txt = self.font.render(self.entry, True, (0, 0, 0))

    def add_char(self, char):
        self.entry = self.entry[:self.n_entry] + \
            char + self.entry[self.n_entry:]
        self.n_entry += 1
        self.update_entry()

    def reset_chest(self):
        for chest in self.jeu.chest:
            print(chest.items)
            chest.open = False
            chest.anim = False
            chest.time_open = None
            chest.image = chest.images[0]

        return f"[Chest] {len(self.jeu.chest)} reset"


    def spawn(self, mob, quantity, ms):
        if mob == 'slime':
            for i in range(int(quantity)):
                self.jeu.slimes.append(slime.Slime(ms, self.jeu))

            return f"[Spawn] {quantity} {mob}"

        elif mob == 'golem':
            for i in range(int(quantity)):
                self.jeu.golems.append(golem.Golem(ms, self.jeu))

            return f"[Spawn] {quantity} {mob}"

        elif mob == 'archer':
            for i in range(int(quantity)):
                self.jeu.archer.append(archer.Archer(self.jeu))

            return f"[Spawn] {quantity} {mob}"

        elif mob == 'wyvern':
            for i in range(int(quantity)):
                self.jeu.wyverns.append(wyvern.Wyvern(self.jeu, 150))

            return f"[Spawn] {quantity} {mob}"

        else:
            return "[Error] Mob inconnu"

    def killall(self):
        nb = (len(self.jeu.slimes) + len(self.jeu.golems) +
              len(self.jeu.loot) + len(self.jeu.archer) +
              len(self.jeu.wyverns) + len(self.jeu.chest))

        for sl in self.jeu.slimes:
            sl.kill()

        for go in self.jeu.golems:
            go.kill()

        for ar in self.jeu.archer:
            ar.kill()

        for ch in self.jeu.chest:
            ch.kill()

        for wy in self.jeu.wyverns:
            wy.kill()

        self.jeu.loot = []

        return f"[Kill] {nb} mobs"

    def collect(self, inv, name):
        if name == "all":
            nb = len(self.jeu.loot)
            for loot in self.jeu.loot:
                loot.collect(inv)

            return f"[Collect] {nb} items"

        elif name in FU.item_name.keys():
            nb = 0
            for loot in self.jeu.loot:
                if loot.name == "name":
                    loot.collect(inv)
                    nb += 1

            return f"[Collect] {nb} {name}"

        return "[Collect] Item inconnu"
