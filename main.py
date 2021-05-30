# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 13:33:17 2021

@author: loann
"""

import pygame
import random as rdm
import math
import fonctions_utiles as FU
import animDoor
import golem
import inventaire
import chat
import carte
import player as pl
import images as img


def game(player_imgs):

    inv = inventaire.inventaire(img.screen)
    player = pl.Player(inv, player_imgs)
    anim_door = animDoor.AnimDoor()
    console = chat.Console(FU.convert(1500), FU.convert(28),
                           FU.convert(393),
                           FU.screen.get_height() / 2 - FU.convert(28))

    spawnable, hitbox_player = False, False
    hitbox_slime, hitbox_arrow, hitbox_golem = False, False, False
    show_inv = False
    time = pygame.time.get_ticks()
    mape = carte.Map()

    while FU.play:
        FU.clock.tick(100)
        pygame.display.update()
        time = pygame.time.get_ticks()
        mape.display(player, FU.screen)
        FU.screen.blit(img.background, (0, 0))
        mouse = pygame.mouse.get_pos()
        FU.display_salle()

        if spawnable:
            for i, j in FU.spawnable:
                x = FU.get_pos_screen(i, j)[0]
                y = FU.get_pos_screen(i, j)[1]
                pygame.draw.line(FU.screen, (255, 0, 0), (x, y),
                                 (x + FU.convert(63),
                                  y + FU.convert(63)))
                pygame.draw.line(FU.screen, (255, 0, 0),
                                 (x + FU.convert(63), y),
                                 (x, y + FU.convert(63)))

        for spike in FU.spikes:
            spike.update(FU.screen, time)

        for torche in FU.torches:
            torche.update(FU.screen, time)

        for arrow in FU.arrows:
            arrow.display(FU.screen, player, inv, time)

        if hitbox_arrow:
            for arrow in FU.arrows:
                arrow.display_hitbox(FU.screen, time)

        for mob in FU.slimes:
            mob.display(time)
            distance = FU.get_distance(player, mob)
            pygame.draw.line(FU.screen,
                             (255 - distance * 255 / FU.convert(1200),
                              distance * 255 / FU.convert(1200), 0),
                             (mob.get_center_screen()),
                             (player.get_center_screen()))
            mob.hit_arrow(FU.arrows)
            if (distance < 100 and time > mob.last_shoot + 2000 and
                    not mob.anim_jump):
                mob.shoot(player, time)

            if hitbox_slime:
                mob.display_hitbox()
            if time > mob.last_jump + 1300:
                mob.jump(time)
            if mob.dead:
                FU.slimes.remove(mob)

        for mob in FU.golems:
            mob.display(time, player)
            mob.hit_arrow(FU.arrows)
            if hitbox_golem:
                mob.display_hitbox(FU.screen)

        player.display(FU.screen, time, show_inv, console.open)

        console.display(FU.screen, time)

        if hitbox_player:
            player.display_hitbox(FU.screen)

        if player.get_center_salle() in FU.pos_portes:
            FU.display_open_porte()

        elif player.get_center_salle() in FU.pos_coffres:
            FU.display_open_coffre()

        if show_inv:
            inv.display(mouse)

        if anim_door.play:
            anim_door.display(FU.screen)
            if anim_door.active:
                if player.get_center_salle()[0] == 1:
                    FU.salle = (FU.salle[0], FU.salle[1] - 1)
                    (FU.pos_walls, FU.pos_coffres, FU.pos_portes, FU.spikes,
                     FU.torches, FU.spawnable) = FU.init_salle(FU.salle)
                    player.posx = FU.get_pos_screen(
                        15, 0)[0] - player.width - player.speed

                elif player.get_center_salle()[0] == 14:
                    FU.salle = (FU.salle[0], FU.salle[1] + 1)
                    (FU.pos_walls, FU.pos_coffres, FU.pos_portes, FU.spikes,
                     FU.torches, FU.spawnable) = FU.init_salle(FU.salle)
                    player.posx = FU.get_pos_screen(
                        1, 0)[0] + player.speed

                elif player.get_center_salle()[1] == 2:
                    FU.salle = (FU.salle[0] - 1, FU.salle[1])
                    (FU.pos_walls, FU.pos_coffres, FU.pos_portes, FU.spikes,
                     FU.torches, FU.spawnable) = FU.init_salle(FU.salle)
                    player.posy = FU.get_pos_screen(
                        0, 15)[1] - player.height - player.speed

                elif player.get_center_salle()[1] == 14:
                    FU.salle = (FU.salle[0] + 1, FU.salle[1])
                    (FU.pos_walls, FU.pos_coffres, FU.pos_portes, FU.spikes,
                     FU.torches, FU.spawnable) = FU.init_salle(FU.salle)
                    player.posy = FU.get_pos_screen(
                        0, 1)[1] + player.speed

        FU.display_fps()

        if player.speed == 4:
            if (((pygame.K_RIGHT in FU.key_pressed or
                  pygame.K_d in FU.key_pressed) and
                 (pygame.K_UP in FU.key_pressed or
                  pygame.K_z in FU.key_pressed))
                or ((pygame.K_RIGHT in FU.key_pressed or
                     pygame.K_d in FU.key_pressed) and
                    (pygame.K_DOWN in FU.key_pressed or
                     pygame.K_s in FU.key_pressed))
                or ((pygame.K_LEFT in FU.key_pressed or
                     pygame.K_q in FU.key_pressed) and
                    (pygame.K_UP in FU.key_pressed or
                     pygame.K_z in FU.key_pressed))
                or ((pygame.K_LEFT in FU.key_pressed or
                     pygame.K_q in FU.key_pressed) and
                    (pygame.K_DOWN in FU.key_pressed or
                     pygame.K_s in FU.key_pressed))):
                player.speed = 4 / math.sqrt(2)
        elif player.speed == 4 / math.sqrt(2):
            player.speed = 4

        for key in FU.key_pressed:
            if (not anim_door.play and not show_inv and not console.open
                    and not player.bumped):

                if key == pygame.K_RIGHT or key == pygame.K_d:
                    player.move_right(time)

                elif key == pygame.K_LEFT or key == pygame.K_q:
                    player.move_left(time)

                elif key == pygame.K_UP or key == pygame.K_z:
                    player.move_up(time)

                elif key == pygame.K_DOWN or key == pygame.K_s:
                    player.move_down(time)

        if ((pygame.K_RIGHT in FU.key_pressed or
             pygame.K_d in FU.key_pressed or
             pygame.K_UP in FU.key_pressed or
             pygame.K_z in FU.key_pressed or
             pygame.K_LEFT in FU.key_pressed or
             pygame.K_q in FU.key_pressed or
                pygame.K_DOWN in FU.key_pressed or
                pygame.K_s in FU.key_pressed) and
                not show_inv and not console.open):
            player.move = True
        else:
            player.move = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                FU.play = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if show_inv:
                    if inv.part == 0 or inv.part == 1:
                        if (inv.posx + FU.convert(25) <= mouse[0] <=
                            inv.posx + FU.convert(558) and
                                inv.posy + FU.convert(345) <= mouse[1] <=
                                inv.posy + FU.convert(543)):

                            x = int((mouse[0] - inv.posx -
                                     FU.convert(25)) // FU.convert(67))
                            y = int((mouse[1] - inv.posy -
                                     FU.convert(345)) // FU.convert(67))

                            if pygame.K_LSHIFT in FU.key_pressed and inv.part == 0:
                                inv.shift_item_inventory(x, y)
                            elif event.button == 1 and not inv.hand:
                                inv.pick_item_inventory(x, y)
                            elif event.button == 3 and inv.hand:
                                inv.drop_1_item_inventory(x, y)

                        else:
                            if inv.part == 0:
                                inv.set_craft(mouse)
                                inv.set_recipes(mouse)
                                for i in range(2):
                                    for j in range(4):
                                        if (inv.posx + FU.convert(77 + 265 * i) <=
                                            mouse[0] <=
                                            inv.posx +
                                                FU.convert(77 + 265 * i + 67)
                                            and inv.posy + FU.convert(40 + 67 * j)
                                            <= mouse[1] <= (inv.posy +
                                                            FU.convert(40 + 67 *
                                                                       (j + 1)))):

                                            if pygame.K_LSHIFT in FU.key_pressed:
                                                inv.shift_item_equiped(i, j)
                                            elif event.button == 1:
                                                inv.pick_item_equiped(i, j)

                            elif inv.part == 1:
                                inv.set_part(mouse)
                                inv.set_recipes(mouse)
                                if (inv.posx + FU.convert(64) <= mouse[0] <=
                                    inv.posx + FU.convert(329) and
                                        inv.posy + FU.convert(41) <= mouse[1] <=
                                        inv.posy + FU.convert(306)):

                                    x = int((mouse[0] - inv.posx -
                                             FU.convert(64)) // FU.convert(67))
                                    y = int((mouse[1] - inv.posy -
                                             FU.convert(41)) // FU.convert(67))

                                    if pygame.K_LSHIFT in FU.key_pressed:
                                        inv.shift_item_crafting(x, y)
                                    elif event.button == 1 and not inv.hand:
                                        inv.pick_item_crafting(x, y)
                                    elif event.button == 3 and inv.hand:
                                        inv.drop_1_item_crafting(x, y)

                                if inv.posx + FU.convert(437) <= mouse[0] <= inv.posx + FU.convert(501) and inv.posy + FU.convert(142) <= mouse[1] <= inv.posy + FU.convert(206):
                                    if pygame.K_LSHIFT in FU.key_pressed:
                                        inv.shift_item_crafted()
                                    elif event.button == 1:
                                        inv.pick_item_crafted()

                    elif inv.part == 2:
                        inv.set_part(mouse)
                        inv.set_craft(mouse)

                        if (inv.crafts.cursor_x <= mouse[0] <= inv.crafts.cursor_x + inv.crafts.size[0] and
                                inv.crafts.cursor_y <= mouse[1] <= inv.crafts.cursor_y + inv.crafts.size[1]):
                            inv.crafts.pressed = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if show_inv:
                    if inv.part == 0 or inv.part == 1 and inv.hand:
                        if (inv.posx + FU.convert(25) <= mouse[0] <=
                            inv.posx + FU.convert(558) and
                                inv.posy + FU.convert(345) <= mouse[1] <=
                                inv.posy + FU.convert(543)):
                            x = int((mouse[0] - inv.posx -
                                     FU.convert(25)) // FU.convert(67))
                            y = int((mouse[1] - inv.posy -
                                     FU.convert(345)) // FU.convert(67))

                            if event.button == 1:
                                inv.drop_item_inventory(x, y)

                        else:
                            if inv.part == 0:
                                for i in range(2):
                                    for j in range(4):
                                        if (inv.posx + FU.convert(77 + 265 * i) <=
                                            mouse[0] <=
                                            inv.posx +
                                                FU.convert(77 + 265 * i + 64)
                                            and inv.posy + FU.convert(40 + 67 * j)
                                            <= mouse[1] <= (inv.posy +
                                                            FU.convert(40 + 67 *
                                                                       (j + 1)))):

                                            if event.button == 1:
                                                inv.drop_item_equiped(i, j)

                                if (inv.posx + FU.convert(442) <= mouse[0] <=
                                    inv.posx + FU.convert(506) and
                                    inv.posy + FU.convert(175) <= mouse[1] <=
                                        inv.posy + FU.convert(303)):
                                    if mouse[1] > inv.posy + FU.convert(249):
                                        inv.drop_item_equiped(2, 3)
                                    else:
                                        inv.drop_item_equiped(2, 2)

                            elif inv.part == 1:
                                if (inv.posx + FU.convert(64) <= mouse[0] <=
                                    inv.posx + FU.convert(329) and
                                        inv.posy + FU.convert(41) <= mouse[1] <=
                                        inv.posy + FU.convert(306)):

                                    x = int((mouse[0] - inv.posx -
                                             FU.convert(64)) // FU.convert(67))
                                    y = int((mouse[1] - inv.posy -
                                             FU.convert(41)) // FU.convert(67))

                                    if event.button == 1:
                                        inv.drop_item_crafting(x, y)

                    else:
                        inv.crafts.pressed = False

                    if inv.hand and event.button == 1:
                        inv.reste_hand()

            elif event.type == pygame.MOUSEWHEEL:
                if inv.part == 2:
                    if event.y == -1:
                        inv.crafts.down_cursor()

                    else:
                        inv.crafts.up_cursor()

            elif event.type == pygame.KEYDOWN:
                if event.key not in FU.key_pressed:
                    FU.key_pressed.append(event.key)

                if (pygame.K_F4 in FU.key_pressed and
                        pygame.K_LALT in FU.key_pressed):
                    FU.play = False

                if pygame.key.name(event.key) == "caps lock":
                    FU.caps_lock = not FU.caps_lock

                if console.open:
                    console.enter_key(pygame.key.name(event.key))
                    if (event.key == pygame.K_RETURN or
                            event.key == pygame.K_KP_ENTER):
                        console.execute_entry(inv, player, time)
                        console.open = False
                        console.supr_entry()

                    if event.key == pygame.K_BACKSPACE:
                        console.delete_entry(time)

                if (event.key == pygame.K_TAB or
                        (not console.open and event.key == pygame.K_t)):
                    console.open = not console.open
                    show_inv = False
                    if not console.open:
                        console.supr_entry()

                elif event.key == pygame.K_ESCAPE:
                    if show_inv:
                        show_inv = False
                        inv.close_inv()

                    elif console.open:
                        console.open = False
                        console.supr_entry()

                    else:
                        FU.play = False

                elif not console.open:
                    if event.key == pygame.K_r:
                        player.posx = FU.screen.get_width() / 2
                        player.posy = FU.screen.get_height() / 2

                    elif (event.key == pygame.K_COLON and
                          (pygame.K_RSHIFT in FU.key_pressed or
                           pygame.K_LSHIFT in FU.key_pressed
                           or FU.caps_lock)):
                        console.open = True
                        console.add_char("/")

                    elif event.key == pygame.K_F1:
                        spawnable = not spawnable

                    elif event.key == pygame.K_F2:
                        hitbox_player = not hitbox_player

                    elif event.key == pygame.K_F3:
                        hitbox_slime = not hitbox_slime

                    elif event.key == pygame.K_F4:
                        hitbox_arrow = not hitbox_arrow

                    elif event.key == pygame.K_F5:
                        hitbox_golem = not hitbox_golem

                    elif event.key == pygame.K_e or event.key == pygame.K_i:
                        show_inv = not show_inv
                        if not show_inv:
                            inv.close_inv()

                    elif event.key == pygame.K_g:
                        inv.aug_arrow(1)

                    elif event.key == pygame.K_h:
                        inv.dim_arrow(1)

                    elif event.key == pygame.K_w and FU.spawnable:
                        FU.golems.append(golem.Golem(FU.screen, time))

                    elif event.key == pygame.K_j:
                        if player.vie + 1 <= player.max_vie:
                            player.vie += 1

                    elif event.key == pygame.K_k:
                        if player.vie - 1 > 0:
                            player.take_damage(1)

                    elif event.key == pygame.K_l:
                        if player.max_vie + 1 <= 7:
                            player.max_vie += 1

                    elif event.key == pygame.K_m:
                        if player.max_vie - 1 > 0:
                            player.max_vie -= 1
                            if player.vie > player.max_vie:
                                player.vie -= 1

                    if FU.slimes:
                        if event.key == pygame.K_v:
                            mob = rdm.choice(FU.slimes)
                            mob.roulade()

                        elif event.key == pygame.K_b:
                            mob = rdm.choice(FU.slimes)
                            if not mob.anim_death:
                                mob.death()

                    elif event.key == pygame.K_SPACE:
                        if player.get_center_salle() in FU.pos_portes:
                            anim_door.play = True

                        elif player.get_center_salle() in FU.pos_coffres:
                            pass

            if event.type == pygame.KEYUP:
                if event.key in FU.key_pressed:
                    FU.key_pressed.remove(event.key)
