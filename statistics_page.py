# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 17:10:19 2021

@author: loann
"""
import pygame
import fonctions_utiles as FU
import images as imgs


def stats_screen(run):
    fichier = open("assets/save/stats.txt")
    time = fichier.read()
    time = pygame.font.SysFont(None, 100).render(time, True, (0, 0, 0))

    while run:
        mouse = pygame.mouse.get_pos()
        pygame.display.update()
        if (FU.convert(795) <= mouse[0] <= FU.convert(1793) and
                FU.convert(754) <= mouse[1] <= FU.convert(889)):
            FU.screen.blit(imgs.mms[1], (0, 0))
        else:
            FU.screen.blit(imgs.mms[0], (0, 0))

        FU.screen.blit(time, (FU.convert(795), FU.convert(164)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return run

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (FU.convert(795) <= mouse[0] <= FU.convert(1793) and
                        FU.convert(754) <= mouse[1] <= FU.convert(889)):
                    return run

    return run
