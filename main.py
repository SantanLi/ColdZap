import pygame as pg
import sys
from pygame.math import Vector2
import json

import drawing_functions as df
import classes as cl


pg.init()
screen = pg.display.set_mode((350, 500))

quit = False
player = cl.Player()
clock = pg.time.Clock()


Comfortaa = pg.font.Font("assets/fonts/Comfortaa.ttf", 60)
Comfortaa_small = pg.font.Font("assets/fonts/Comfortaa.ttf", 20)

with open("GameData/settings.json") as f:
    settings = json.load(f)
    if settings["music"] == 0:
        music_playing = False
    elif settings["music"] == 1:
        music_playing = True
        pg.mixer.music.load("assets/audio/menu.mp3")
    elif settings["music"] == 2:
        music_playing = True
        pg.mixer.music.load("assets/audio/Supert.mp3")
if music_playing:
    pg.mixer.music.play(-1)


def main(saved=False):
    if saved:
        with open("Gamedata/saves.json") as f:
            save = json.load(f)
            level = save["levelId"]
            score = save["score"]
            lives = save["lives"]
    else:
        level = 0
        score = 0
        lives = 5

    with open(f"Gamedata/Levels/Level{level}.json") as f:
        level_data = json.load(f)
    enemies = []
    for i in level_data["enemies"]:
        enemies.append(
            cl.Enemy(
                level_data["enemies"][i]["type"],
                (level_data["enemies"][i]["positions"]),
                level_data["enemies"][i]["speed"],
            )
        )

    global quit

    def event_handler():
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP or event.key == pg.K_w:
                    player.move("up")
                elif event.key == pg.K_DOWN or event.key == pg.K_s:
                    player.move("down")
                elif event.key == pg.K_LEFT or event.key == pg.K_a:
                    player.move("left")
                elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                    player.move("right")
                elif event.key == pg.K_ESCAPE or event.key == pg.K_q:
                    return True

    back_button = cl.TxtButton(20, 480, "<=", (0, 0, 0), Comfortaa_small)

    while not quit:
        clock.tick(60)
        quit = (
            pg.event.get(pg.QUIT) or event_handler()
        )  # quit if window is closed or event_handler returns True

        df.draw_bg(screen)  # draw background

        player.update(screen)  # update player
        for enemy in enemies:
            enemy.update(screen)  # update enemies
        cl.displayBullets(screen)  # update bullets

        df.draw_ui(screen, Comfortaa_small, level, score, lives)  # draw ui

        if back_button.update(
            screen, pg.mouse.get_pos() if pg.mouse.get_pressed()[0] else (0, 0)
        ):
            df.fade_to(screen, (0, 0, 0), 0.15)
            return menu

        pg.display.flip()

    pg.quit()
    sys.exit()


def menu():
    def paused():
        back_button = cl.TxtButton(175, 200, "Resume", (0, 0, 0), Comfortaa_small)
        while True:
            df.draw_bg(screen)
            df.draw_txt(screen, "Paused", 175, 100, (0, 0, 0), Comfortaa)
            if back_button.update(
                screen, pg.mouse.get_pos() if pg.mouse.get_pressed()[0] else (0, 0)
            ):
                df.fade_to(screen, (0, 0, 0), 0.15)
                break

    global quit

    def event_handler():
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE or event.key == pg.K_q:
                    return True
                elif event.key == pg.K_RETURN:
                    return False

    new_game = cl.TxtButton(175, 200, "New Game", (0, 0, 0), Comfortaa_small)
    load_game = cl.TxtButton(175, 250, "Load Game", (0, 0, 0), Comfortaa_small)
    view_highscore = cl.TxtButton(175, 300, "Highscores", (0, 0, 0), Comfortaa_small)
    quit_game = cl.TxtButton(175, 350, "Quit", (0, 0, 0), Comfortaa_small)

    while not quit:
        clock.tick(60)

        quit = (
            pg.event.get(pg.QUIT) or event_handler()
        )  # quit if window is closed or event_handler returns True

        df.draw_menu_bg(screen)  # draw background
        mouse_pos = (
            pg.mouse.get_pos() if pg.mouse.get_pressed()[0] else (0, 0)
        )  # get mouse position if mouse is pressed, else (0,0)

        df.draw_txt(screen, "ColdZap", 175, 100, (0, 0, 0), Comfortaa)

        if quit_game.update(screen, mouse_pos):
            df.fade_to(screen, (0, 0, 0), 0.15)
            break
        if load_game.update(screen, mouse_pos):
            df.fade_to(screen, (0, 0, 0), 0.15)
            return loadscreen
        if view_highscore.update(screen, mouse_pos):
            df.fade_to(screen, (0, 0, 0), 0.15)
            return highscore
        if new_game.update(screen, mouse_pos):
            df.fade_to(screen, (0, 0, 0), 0.15)
            return main

        pg.display.flip()

    pg.quit()
    sys.exit()


def loadscreen():
    return main(True)


def highscore():
    with open("Gamedata/highscores.json") as f:
        highscore = json.load(f)

        print(highscore)
    return menu


if __name__ == "__main__":
    active_screen = menu
    while True:
        active_screen = active_screen()
