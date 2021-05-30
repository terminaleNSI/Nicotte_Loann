# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 13:33:17 2021

@author: loann
"""

import pygame
import math
import fonctions_utiles as FU
import images as img


def game(jeu, run):
    player = jeu.player
    mape = jeu.mape
    inv = jeu.inv
    console = jeu.console

    while run:
        jeu.clock.tick(100)
        pygame.display.update()
        time = pygame.time.get_ticks()
        mape.display(player, jeu.screen, jeu.golems, jeu.slimes)
        jeu.screen.blit(img.background, (0, 0))
        mouse = pygame.mouse.get_pos()
        jeu.display_salle()

        jeu.auto_save()

        if jeu.pos_spawnable:
            for i, j in jeu.spawnable:
                x = FU.get_pos_screen(i, j)[0]
                y = FU.get_pos_screen(i, j)[1]
                pygame.draw.line(jeu.screen, (255, 0, 0), (x, y),
                                 (x + FU.convert(63),
                                  y + FU.convert(63)))
                pygame.draw.line(jeu.screen, (255, 0, 0),
                                 (x + FU.convert(63), y),
                                 (x, y + FU.convert(63)))

        for spike in jeu.spikes:
            spike.update(jeu.screen, time, jeu)

        for torche in jeu.torches:
            torche.update(jeu.screen, time, jeu)

        console.display(time)

        jeu.display_all()

        if player.get_center_salle() in jeu.pos_portes:
            jeu.display_open_porte()

        elif player.get_center_salle() in jeu.pos_coffres:
            jeu.display_open_coffre()

        if jeu.show_inv:
            inv.display(mouse)

        if jeu.anim_door.play:
            jeu.anim_door.display(jeu.screen)
            if jeu.anim_door.active:
                if player.get_center_salle()[0] == 1:
                    jeu.save_entity(jeu.salle)
                    jeu.salle = (jeu.salle[0], jeu.salle[1] - 1)
                    jeu.init_salle()
                    player.rect.left = FU.get_pos_screen(
                        15, 0)[0] - player.rect.width - player.speed

                elif player.get_center_salle()[0] == 14:
                    jeu.save_entity(jeu.salle)
                    jeu.salle = (jeu.salle[0], jeu.salle[1] + 1)
                    jeu.init_salle()
                    player.rect.left = FU.get_pos_screen(
                        1, 0)[0] + player.speed

                elif player.get_center_salle()[1] == 2:
                    jeu.save_entity(jeu.salle)
                    jeu.salle = (jeu.salle[0] - 1, jeu.salle[1])
                    jeu.init_salle()
                    player.rect.top = FU.get_pos_screen(
                        0, 15)[1] - player.rect.height - player.speed

                elif player.get_center_salle()[1] == 14:
                    jeu.save_entity(jeu.salle)
                    jeu.salle = (jeu.salle[0] + 1, jeu.salle[1])
                    jeu.init_salle()
                    player.rect.top = FU.get_pos_screen(
                        0, 1)[1] + player.speed

        jeu.display_fps()

        if player.speed == 4:
            if (((pygame.K_RIGHT in jeu.key_pressed or
                  pygame.K_d in jeu.key_pressed) and
                 (pygame.K_UP in jeu.key_pressed or
                  pygame.K_z in jeu.key_pressed))
                or ((pygame.K_RIGHT in jeu.key_pressed or
                     pygame.K_d in jeu.key_pressed) and
                    (pygame.K_DOWN in jeu.key_pressed or
                     pygame.K_s in jeu.key_pressed))
                or ((pygame.K_LEFT in jeu.key_pressed or
                     pygame.K_q in jeu.key_pressed) and
                    (pygame.K_UP in jeu.key_pressed or
                     pygame.K_z in jeu.key_pressed))
                or ((pygame.K_LEFT in jeu.key_pressed or
                     pygame.K_q in jeu.key_pressed) and
                    (pygame.K_DOWN in jeu.key_pressed or
                     pygame.K_s in jeu.key_pressed))):
                player.speed = 4 / math.sqrt(2)
        elif player.speed == 4 / math.sqrt(2):
            player.speed = 4

        for key in jeu.key_pressed:
            if (not jeu.anim_door.play and not jeu.show_inv and
                    not console.open and not player.bumped):

                if key == pygame.K_RIGHT or key == pygame.K_d:
                    player.move_right(time)

                elif key == pygame.K_LEFT or key == pygame.K_q:
                    player.move_left(time)

                elif key == pygame.K_UP or key == pygame.K_z:
                    player.move_up(time)

                elif key == pygame.K_DOWN or key == pygame.K_s:
                    player.move_down(time)

        if ((pygame.K_RIGHT in jeu.key_pressed or
             pygame.K_d in jeu.key_pressed or
             pygame.K_UP in jeu.key_pressed or
             pygame.K_z in jeu.key_pressed or
             pygame.K_LEFT in jeu.key_pressed or
             pygame.K_q in jeu.key_pressed or
                pygame.K_DOWN in jeu.key_pressed or
                pygame.K_s in jeu.key_pressed) and
                not jeu.show_inv and not console.open):
            player.move = True
        else:
            player.move = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jeu.save_game()
                return run

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if jeu.show_inv:
                    if inv.part == 0 or inv.part == 1:
                        if (inv.posx + FU.convert(25) <= mouse[0] <=
                            inv.posx + FU.convert(558) and
                                inv.posy + FU.convert(345) <= mouse[1] <=
                                inv.posy + FU.convert(543)):

                            x = int((mouse[0] - inv.posx -
                                     FU.convert(25)) // FU.convert(67))
                            y = int((mouse[1] - inv.posy -
                                     FU.convert(345)) // FU.convert(67))

                            if (pygame.K_LSHIFT in jeu.key_pressed and
                                    inv.part == 0):
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
                                        if (inv.posx + FU.convert(77 + 265 * i)
                                            <= mouse[0] <=
                                            inv.posx +
                                                FU.convert(77 + 265 * i + 67)
                                            and inv.posy +
                                            FU.convert(40 + 67 * j)
                                            <= mouse[1] <=
                                            (inv.posy +
                                             FU.convert(40 + 67 * (j + 1)))):

                                            if (pygame.K_LSHIFT in
                                                    jeu.key_pressed):
                                                inv.shift_item_equiped(i, j)
                                            elif event.button == 1:
                                                inv.pick_item_equiped(i, j)

                                if (inv.posx + FU.convert(442) <= mouse[0] <=
                                    inv.posx + FU.convert(506) and
                                    inv.posy + FU.convert(175) <= mouse[1] <=
                                        inv.posy + FU.convert(303)):
                                    if mouse[1] > inv.posy + FU.convert(249):
                                        if pygame.K_LSHIFT in jeu.key_pressed:
                                            inv.shift_item_equiped(2, 3)
                                        else:
                                            inv.pick_item_equiped(2, 3)
                                    else:
                                        if pygame.K_LSHIFT in jeu.key_pressed:
                                            inv.shift_item_equiped(2, 2)
                                        else:
                                            inv.pick_item_equiped(2, 2)

                            elif inv.part == 1:
                                inv.set_part(mouse)
                                inv.set_recipes(mouse)
                                if (inv.posx + FU.convert(64) <= mouse[0] <=
                                    inv.posx + FU.convert(329) and
                                        inv.posy + FU.convert(41)
                                        <= mouse[1] <=
                                        inv.posy + FU.convert(306)):

                                    x = int((mouse[0] - inv.posx -
                                             FU.convert(64)) // FU.convert(67))
                                    y = int((mouse[1] - inv.posy -
                                             FU.convert(41)) // FU.convert(67))

                                    if pygame.K_LSHIFT in jeu.key_pressed:
                                        inv.shift_item_crafting(x, y)
                                    elif event.button == 1 and not inv.hand:
                                        inv.pick_item_crafting(x, y)
                                    elif event.button == 3 and inv.hand:
                                        inv.drop_1_item_crafting(x, y)

                                if (inv.posx + FU.convert(437) <= mouse[0] <=
                                    inv.posx + FU.convert(501) and inv.posy +
                                    FU.convert(142) <= mouse[1] <= inv.posy +
                                        FU.convert(206)):
                                    if pygame.K_LSHIFT in jeu.key_pressed:
                                        inv.shift_item_crafted()
                                    elif event.button == 1:
                                        inv.pick_item_crafted()

                    elif inv.part == 2:
                        inv.set_part(mouse)
                        inv.set_craft(mouse)

                        if (inv.crafts.cursor_x <= mouse[0] <=
                            inv.crafts.cursor_x + inv.crafts.size[0] and
                                inv.crafts.cursor_y <= mouse[1] <=
                                inv.crafts.cursor_y + inv.crafts.size[1]):
                            inv.crafts.pressed = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if jeu.show_inv:
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

                        elif (inv.posx + FU.convert(584) <= mouse[0] <=
                              inv.posx + FU.convert(635) and
                                inv.posy + FU.convert(496) <= mouse[1] <=
                                inv.posy + FU.convert(552) and inv.hand):
                                    inv.hand = None

                        else:
                            if inv.part == 0:
                                for i in range(2):
                                    for j in range(4):
                                        if (inv.posx + FU.convert(77 + 265 * i)
                                            <= mouse[0] <=
                                            inv.posx +
                                                FU.convert(77 + 265 * i + 64)
                                            and inv.posy +
                                            FU.convert(40 + 67 * j)
                                            <= mouse[1] <=
                                            (inv.posy +
                                             FU.convert(40 + 67 * (j + 1)))):

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
                                        inv.posy + FU.convert(41)
                                        <= mouse[1] <=
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
                if event.key not in jeu.key_pressed:
                    jeu.key_pressed.append(event.key)

                if (pygame.K_F4 in jeu.key_pressed and
                        pygame.K_LALT in jeu.key_pressed):
                    jeu.save_game()
                    run = False

                if pygame.key.name(event.key) == "caps lock":
                    jeu.caps_lock = not jeu.caps_lock

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
                    jeu.show_inv = False
                    if not console.open:
                        console.supr_entry()

                elif event.key == pygame.K_ESCAPE:
                    if jeu.show_inv:
                        jeu.show_inv = False
                        inv.close_inv()

                    elif console.open:
                        console.open = False
                        console.supr_entry()

                    else:
                        jeu.save_game()
                        return run

                elif not console.open:
                    if event.key == pygame.K_r:
                        player.posx = FU.screen.get_width() / 2
                        player.posy = FU.screen.get_height() / 2

                    elif (event.key == pygame.K_COLON and
                          (pygame.K_RSHIFT in jeu.key_pressed or
                           pygame.K_LSHIFT in jeu.key_pressed
                           or jeu.caps_lock)):
                        console.open = True
                        console.add_char("/")

                    elif event.key == pygame.K_F1:
                        jeu.pos_spawnable = not jeu.pos_spawnable

                    elif event.key == pygame.K_F2:
                        jeu.hitbox_player = not jeu.hitbox_player

                    elif event.key == pygame.K_F3:
                        jeu.hitbox_slime = not jeu.hitbox_slime

                    elif event.key == pygame.K_F4:
                        jeu.hitbox_arrow = not jeu.hitbox_arrow

                    elif event.key == pygame.K_F5:
                        jeu.hitbox_golem = not jeu.hitbox_golem

                    elif event.key == pygame.K_e or event.key == pygame.K_i:
                        jeu.show_inv = not jeu.show_inv
                        if not jeu.show_inv:
                            inv.close_inv()

                    elif event.key == pygame.K_g:
                        inv.aug_arrow(1)

                    elif event.key == pygame.K_h:
                        inv.dim_arrow(1)

                    elif event.key == pygame.K_f:
                        player.pick_item()

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

                    elif event.key == pygame.K_SPACE:
                        if not jeu.wyverns and jeu.copleted_pp():
                            if player.get_center_salle() in jeu.pos_portes:
                                jeu.anim_door.play = True

            if event.type == pygame.KEYUP:
                if event.key in jeu.key_pressed:
                    jeu.key_pressed.remove(event.key)

    return run
