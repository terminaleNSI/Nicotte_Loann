# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 08:48:46 2021

@author: loann
"""
import pygame
import images as imgs
import fonctions_utiles as FU
import jeu
import statistics_page as sp


def main_menu(img, run):
    while run:
        pygame.mouse.set_cursor(*pygame.cursors.tri_left)
        pygame.display.update()
        mouse = pygame.mouse.get_pos()
        FU.screen.blit(imgs.mm[0], (0, 0))
        for i in range(5):
            if FU.convert(795) <= mouse[0] <= FU.convert(1793):
                if (FU.convert(126) + FU.convert(157) * i <= mouse[1] <=
                        FU.convert(263) + FU.convert(157) * i):
                    FU.screen.blit(imgs.mm[i + 1], (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return run

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(5):
                    if FU.convert(795) <= mouse[0] <= FU.convert(1793):
                        if (FU.convert(126) + FU.convert(157) * i <= mouse[1]
                                <= FU.convert(263) + FU.convert(157) * i):
                            if i == 0 or i == 1:
                                if i == 1:
                                    FU.reset_save()
                                    fichier = open("assets/save/boss", "w")
                                    fichier.write("wyvern True 150")

                                game = jeu.Jeu(img)
                                run = game.init_game(run)


                            elif i == 3:
                                run = sp.stats_screen(run)

                            elif i == 4:
                                run = False
                                return run

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    return run

                elif event.key == pygame.K_AMPERSAND or event.key == pygame.K_KP1:
                    game = jeu.Jeu(img)
                    run = game.init_game(run)

                elif event.key == 50 or event.key == pygame.K_KP2:
                    FU.reset_save()

                elif event.key == pygame.K_QUOTEDBL or event.key == pygame.K_KP3:
                    None

                elif event.key == pygame.K_QUOTE or event.key == pygame.K_KP4:
                    run = sp.stats_screen(run)

                elif event.key == pygame.K_LEFTPAREN or event.key == pygame.K_KP5:
                    run = False
                    return run
    return run
