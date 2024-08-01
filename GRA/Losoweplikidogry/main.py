import pygame as pg
from pygame.locals import *
from levels import levels
from random import randint as ri
import subprocess
import math
import time

pg.init()
#-----------------------------------USTAWIANIE PODSTAWOWYCH WARTOŚCI---------------------#
pixel = 64 # żeby wyglądało bardziej profesjonalnie XDDDD
width, height = 1216, 768  # 19 bloków szerokości i 12 bloków wysokości
window = pg.display.set_mode((width, height))  # USTAWIANIE OKNA
pg.display.set_caption("Mario Syndrom Adventure")   # NAZWA GRY (I TAK PÓŹNIEJ DODAJE DO NIEJ FPSY i CZAS GRY)
background = pg.transform.scale(pg.image.load('background.jpg'), (width, height))  #zdjęcie w tle
background_special = pg.transform.scale(pg.image.load('background_special.jpg'), (width,height))
fon = pg.font.Font('retro_computer_personal_use.ttf', 35) #import fontu
h1 = pg.font.Font('retro_computer_personal_use.ttf',60) #import fontu``
h2 = pg.font.Font('retro_computer_personal_use.ttf',50) #import fontu
serce_OKEJ  = pg.image.load('serce_okej.png') 
serce_zlamane = pg.image.load('serce_zlamane.png')
startscreen = pg.transform.scale(pg.image.load('startscreeen.png'), (width, height))
pg.display.set_icon(pg.image.load('Ico.png'))
key_bindings = {
    "move_left": pg.K_LEFT,
    "move_right": pg.K_RIGHT,
    "jump": pg.K_SPACE,
    "attack": pg.K_z,
    "use" : pg.K_e
}
#-----------------------------------------------------------------------------------------#

#-------------ŁADOWANIE DZWIĘKÓW-----------#
Mariusz_sfx = pg.mixer.Sound("itsmemariuszautysta.mp3")
skok_sfx = pg.mixer.Sound("skok.mp3")
monetkaegg_sfx = pg.mixer.Sound("doblamonetka.mp3")
monetka_sfx = pg.mixer.Sound("monetka.mp3")
kill_sfx = pg.mixer.Sound("kill.mp3")
minushp_sfx = pg.mixer.Sound("minusonehp.mp3")
off_sfx = pg.mixer.Sound("offmario.mp3")
head_sfx = pg.mixer.Sound("headshot.mp3")
boss_sounds = pg.mixer.Sound("mariosoundtrack.mp3")
knock = pg.mixer.Sound("knock.mp3")
hpminus = pg.mixer.Sound("-1hp.mp3")
winez = pg.mixer.Sound("winez.mp3")
mario_sound = pg.mixer.Sound("sigmamariobybartek.mp3")
for sound in [Mariusz_sfx, skok_sfx, monetkaegg_sfx, monetka_sfx, kill_sfx, minushp_sfx,off_sfx,head_sfx,boss_sounds,knock,hpminus,winez,mario_sound]:
    sound.set_volume(0.5)
#------------------------------------------#
def read_best_scores():
    try:
        with open("best.txt", "r") as file:
            lines = file.readlines()
            if lines:
                best_time = int(lines[0].strip())
                best_coins = int(lines[1].strip())
                best_mario_points = int(lines[2].strip())
                best_game = lines[3].strip()
                top_level = int(lines[4].strip())
                coin_counter = int(lines[5].strip())
                bronie = lines[6].strip()
            else:
                best_time = 'Nie ma'
                best_coins = 'Nie ma'
                best_mario_points = 'Nie ma'
                best_game = 'Nie ma'
                top_level = 'Nie ma'
                coin_counter = 0
                bronie = ''
    except (FileNotFoundError, IndexError, ValueError):
        best_time = 'Nie ma'
        best_coins = 'Nie ma'
        best_mario_points = 'Nie ma'
        best_game = 'Nie ma'
        top_level = 'Nie ma'
        coin_counter = 0
        bronie = ''
    return best_time, best_coins, best_mario_points, best_game, top_level, coin_counter, bronie

def write_best_scores(best_time, best_coins, best_mario_points, best_game, top_level,coin_counter, bronie, ):
    with open("best.txt", "w") as file:
        file.write(f"{best_time}\n{best_coins}\n{best_mario_points}\n{best_game}\n{top_level}\n{coin_counter}\n{bronie}\n")

#-------------------------------PRZYPISYWANIE PODSTAWOWEJ BRONI-------------------------------#
chosen_weapon = read_best_scores()[6].split(',')[0] 
#---------------------------------------------------------------------------------------------#

def start_screen(chosen_weapon,slider_value):
    running = True
    rainbow_colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (143, 0, 255)]
    color_index = 0
    title = "Mario Syndrom Adventure"
    pg.display.set_caption(f"Mario Syndrom Adventure")
    last_time = pg.time.get_ticks()
    while running:
        window.fill((0,0,0))
        startscreen.convert_alpha()
        startscreen.set_alpha(255)
        window.blit(startscreen, (0, 0))

        shadow_color = (50, 50, 50)
        shadow_offst = (3, 3)

        x_offset = 0
        for char in title:
            char_render = h1.render(char, True, rainbow_colors[color_index])
            shadow_text = h1.render(char, False, shadow_color)
            window.blit(shadow_text, (width//2 - len(title)*char_render.get_width()//2 + x_offset + shadow_offst[0], 50 + shadow_offst[1]))
            window.blit(char_render, (width//2 - len(title)*char_render.get_width()//2 + x_offset, 50))

            x_offset += char_render.get_width()

        actual_time = pg.time.get_ticks()
        if actual_time - last_time >= 1000:
            color_index = (color_index + 1) % len(rainbow_colors)
            last_time = actual_time

        play_button = fon.render("Play", True, (17, 16, 17))
        shadow_text = fon.render("Play", False, shadow_color)
        window.blit(shadow_text, (width//2 - play_button.get_width()//2 + shadow_offst[0] + 30,  200 + shadow_offst[1]))
        window.blit(play_button, (width//2 - play_button.get_width()//2 + 30, 200))

        quit_button = fon.render("Quit", True, (17, 16, 17))
        shadow_text = fon.render("Quit", False, shadow_color)
        window.blit(shadow_text, (width//2 - quit_button.get_width()//2 + shadow_offst[0] + 10,370 + shadow_offst[1]))
        window.blit(quit_button, (width//2 - quit_button.get_width()//2 + 10, 370))

        shop_button = h2.render("hop", True, (17,17,17))
        shadow_text = h2.render("hop", False, (200,200,200))
        window.blit(shadow_text, (width//2 - shop_button.get_width()//2 + shadow_offst[0] + 420,360 + shadow_offst[1]))
        window.blit(shop_button, (width//2 - shop_button.get_width()//2 + 420, 360))

        best_button = fon.render("Best\nStats", True, (100,100,100))
        shadow_text = fon.render("Best\nStats", False, shadow_color)
        window.blit(shadow_text, (width//2 - best_button.get_width()//2 + shadow_offst[0] - 320,390 + shadow_offst[1]))
        window.blit(best_button, (width//2 - best_button.get_width()//2 - 320, 390))
                
                
        levels_button = fon.render("Levels", True, (100,100,100))
        shadow_text = fon.render("Levels", False, shadow_color)
        window.blit(shadow_text, (width//2 - levels_button.get_width()//2 + shadow_offst[0] + 460,180 + shadow_offst[1]))
        window.blit(levels_button, (width//2 - levels_button.get_width()//2 + 460, 180))

        eq_button = fon.render("Eq", True, (100,100,100))
        shadow_text = fon.render("Eq", False, shadow_color)
        window.blit(shadow_text, (width//2 - eq_button.get_width()//2 + shadow_offst[0] - 440,200 + shadow_offst[1]))
        window.blit(eq_button, (width//2 - eq_button.get_width()//2 - 440, 200))


        settings_button = fon.render("Settings", True, (255,255,255))
        shadow_text = fon.render("Settings", False, shadow_color)
        window.blit(shadow_text, (width - settings_button.get_width() + shadow_offst[0] - 10 ,height - settings_button.get_height() + shadow_offst[1] - 5))
        window.blit(settings_button, (width - settings_button.get_width() - 10, height - settings_button.get_height()  -5))

        _,_,_,_,_,Coins,_ = read_best_scores()

        coins = fon.render(f"Coins : {Coins}", True, (255,255,0))
        shadow_text = fon.render(f"Coins : {Coins}", False, shadow_color)
        window.blit(shadow_text, (10 + shadow_offst[0],height - coins.get_height() + shadow_offst[1]))
        window.blit(shadow_text, (10 - shadow_offst[0],height - coins.get_height() - shadow_offst[1]))
        window.blit(shadow_text, (10 - shadow_offst[1],height - coins.get_height() + shadow_offst[0]))
        window.blit(shadow_text, (10 + shadow_offst[1],height - coins.get_height() - shadow_offst[0]))
        window.blit(coins, (10, height - coins.get_height()))
      

        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()

        if width//2 - play_button.get_width()//2 + 30 <= mouse[0] <= width//2 + play_button.get_width()//2 + 30 and \
           200 <= mouse[1] <= 200 + play_button.get_height():
            
            pg.draw.rect(window, (255, 0, 0), (width//2 - play_button.get_width()//2 + 30, 200, play_button.get_width(), play_button.get_height()), 3)
            if click[0] == 1:
                running = False
                main(1, chosen_weapon, 0, 0,slider_value)
        elif width//2 - eq_button.get_width()//2 - 440 <= mouse[0] <= width//2 + eq_button.get_width()//2 - 440 and \
                200 <= mouse[1] <= 200 + levels_button.get_height() :
                    pg.draw.rect(window, (255, 0, 0), (width//2 - eq_button.get_width()//2 - 440,200, eq_button.get_width(), eq_button.get_height()), 3)
                    if click[0] == 1:
                        running = False
                        Eq(chosen_weapon,slider_value)
        elif width//2 - levels_button.get_width()//2 + 460 <= mouse[0] <= width//2 + levels_button.get_width()//2 + 460 and \
                180 <= mouse[1] <= 180 + levels_button.get_height() :
                    pg.draw.rect(window, (255, 0, 0), (width//2 - levels_button.get_width()//2 + 460,180, levels_button.get_width(), levels_button.get_height()), 3)
                    if click[0] == 1:
                        running = False
                        Levels(chosen_weapon,slider_value)
        elif width//2 - quit_button.get_width()//2 + 10 <= mouse[0] <= width//2 + quit_button.get_width()//2 + 10 and \
             370 <= mouse[1] <= 370 + quit_button.get_height():
            
            pg.draw.rect(window, (255, 0, 0), (width//2 - quit_button.get_width()//2 + 10, 370, quit_button.get_width() , quit_button.get_height()), 3)
            if click[0] == 1:
                pg.quit()
        elif width//2 - shop_button.get_width()//2 + 370 <= mouse[0] <= width//2 + play_button.get_width()//2 + 420 and \
           360 <= mouse[1] <= 360 + play_button.get_height() + 20 :
            pg.draw.rect(window, (255, 0, 0), (width//2 - shop_button.get_width()//2 + 370,360, shop_button.get_width() + 50, shop_button.get_height()), 3)
            if click[0] == 1:
                running = False
                shop(slider_value)
        elif width//2 - best_button.get_width()//2 - 320 <= mouse[0] <= width//2 + best_button.get_width()//2 - 320 and \
           390 <= mouse[1] <= 390 + best_button.get_height() :
            pg.draw.rect(window, (255, 0, 0), (width//2 - best_button.get_width()//2 - 320,390, best_button.get_width(), best_button.get_height()), 3)
            if click[0] == 1:
                running = False
                besttime(slider_value,chosen_weapon)
        elif width - settings_button.get_width() - 10 <= mouse[0] <= width + settings_button.get_width() - 10 and \
           height - settings_button.get_height() - 5 <= mouse[1] <=height + settings_button.get_height() - 5 :
            pg.draw.rect(window, (255, 0, 0), (width - settings_button.get_width() - 10,height - settings_button.get_height() - 5, settings_button.get_width(), settings_button.get_height()), 3)
            if click[0] == 1:
                running = False
                settings(slider_value)
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                    if event.key == pg.K_f:
                        pg.display.toggle_fullscreen()
        pg.display.update()
def Eq(chosen_weapon,slider_value):
    running = True
    rainbow_colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (143, 0, 255)]
    color_index = 0
    last_time = pg.time.get_ticks()
    
    mario = Mario(width, height, read_best_scores()[6].split(',')[0])
    
    while running:
        window.fill((0,0,0))
        startscreen.convert_alpha()
        startscreen.set_alpha(50)
        window.blit(startscreen, (0, 0))
        
        title = "EQ"
        x_offset = 0
        for char in title:
            char_render = h1.render(char, True, rainbow_colors[color_index])
            window.blit(char_render, (width//2 - len(title)*char_render.get_width()//2 + x_offset, 10))
            x_offset += char_render.get_width()
        
        actual_time = pg.time.get_ticks()
        if actual_time - last_time >= 1000:
            color_index = (color_index + 1) % len(rainbow_colors)
            last_time = actual_time
        
        back_button = fon.render("Back", True, (255, 255, 255))
        window.blit(back_button, (width//2 - back_button.get_width()//2, height - back_button.get_height() - 100))

        bronie = mario.weapons
        
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        
        button_height = 300
        for weapon in bronie:
            weapon_text = fon.render(weapon, True, (255, 255, 255))
            window.blit(weapon_text, (width//2 - weapon_text.get_width()//2, button_height))
            
            if width//2 - weapon_text.get_width()//2 <= mouse[0] <= width//2 + weapon_text.get_width()//2 and \
             button_height <= mouse[1] <= button_height + weapon_text.get_height():
                
                pg.draw.rect(window, (255, 0, 0), (width//2 - weapon_text.get_width()//2, button_height, weapon_text.get_width() , weapon_text.get_height()), 3)
            
                if click[0] == 1:
                    chosen_weapon = weapon
                    mario.weapon = chosen_weapon
            button_height += 50

        if width//2 - back_button.get_width()//2 <= mouse[0] <= width//2 + back_button.get_width()//2 and \
             height - back_button.get_height() - 100 <= mouse[1] <= height - back_button.get_height() - 100 + back_button.get_height():
            pg.draw.rect(window, (255, 0, 0), (width//2 - back_button.get_width()//2, height - back_button.get_height() - 100, back_button.get_width() , back_button.get_height()), 3)
            if click[0] == 1:
                start_screen(chosen_weapon,slider_value)
                running = False

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                    if event.key == pg.K_f:
                        pg.display.toggle_fullscreen()
        pg.display.update()
def Levels(chosen_weapon,slider_value):
    running = True
    rainbow_colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (143, 0, 255)]
    color_index = 0
    last_time = pg.time.get_ticks()
    
    level_tile_width = 100
    level_tile_height = 50
    level_tiles_margin = 10
    level_tiles_per_row = 5
    
    while running:
        window.fill((0,0,0))
        startscreen.convert_alpha()
        startscreen.set_alpha(50)
        window.blit(startscreen, (0, 0))
        
        title = "Levels"
        x_offset = 0
        for char in title:
            char_render = h1.render(char, True, rainbow_colors[color_index])
            window.blit(char_render, (width//2 - len(title)*char_render.get_width()//2 + x_offset, 10))
            x_offset += char_render.get_width()
        
        actual_time = pg.time.get_ticks()
        if actual_time - last_time >= 1000:
            color_index = (color_index + 1) % len(rainbow_colors)
            last_time = actual_time
        
        back_button = fon.render("Back", True, (255, 255, 255))
        window.blit(back_button, (width//2 - back_button.get_width()//2, height - back_button.get_height() - 100))

        _, _, _, _, top_level,_,_ = read_best_scores()
        all_levels = len(levels)
        level_tiles = []
        if top_level == 'Nie ma':
            top_level = 0
        for level in range(1, all_levels + 1):
            row = (level - 1) // level_tiles_per_row
            col = (level - 1) % level_tiles_per_row
            x = col * (level_tile_width + level_tiles_margin) + (width - level_tile_width * level_tiles_per_row - level_tiles_margin * (level_tiles_per_row - 1)) // 2
            y = row * (level_tile_height + level_tiles_margin) + h1.get_height() + 50
            level_tiles.append((level, pg.Rect(x, y, level_tile_width, level_tile_height)))
            if level <= top_level:
                pg.draw.rect(window, (255, 255, 255), (x, y, level_tile_width, level_tile_height), 3)
                level_text = h2.render(str(level), True, (255, 255, 255))
            else:
                pg.draw.rect(window, (100, 100, 100), (x, y, level_tile_width, level_tile_height), 3)
                level_text = h2.render(str(level), True, (100, 100, 100))
            window.blit(level_text, (x + (level_tile_width - level_text.get_width()) // 2, y + (level_tile_height - level_text.get_height()) // 2))

        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        if width//2 - back_button.get_width()//2 <= mouse[0] <= width//2 + back_button.get_width()//2 and \
             height - back_button.get_height() - 100 <= mouse[1] <= height - back_button.get_height() - 100 + back_button.get_height():
            pg.draw.rect(window, (255, 0, 0), (width//2 - back_button.get_width()//2, height - back_button.get_height() - 100, back_button.get_width() , back_button.get_height()), 3)
            if click[0] == 1:
                start_screen(chosen_weapon,slider_value)
                running = False

        for level, rect in level_tiles:
            if rect.collidepoint(mouse) and level <= top_level:
                pg.draw.rect(window, (255, 0, 0), rect, 3)
                if click[0] == 1:
                    main(level, chosen_weapon,0, 0,slider_value)
                    running = False

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                    if event.key == pg.K_f:
                        pg.display.toggle_fullscreen()
        pg.display.update()

def besttime(slider_value, chosen_weapon):
    running = True
    rainbow_colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (143, 0, 255)]
    color_index = 0
    last_time = pg.time.get_ticks()
    while running:
        window.fill((0,0,0))
        startscreen.convert_alpha()
        startscreen.set_alpha(50)
        window.blit(startscreen, (0, 0))
        
        title = "BEST STATS"
        x_offset = 0
        for char in title:
            char_render = h1.render(char, True, rainbow_colors[color_index])
            window.blit(char_render, (width//2 - len(title)*char_render.get_width()//2 + x_offset, 10))
            x_offset += char_render.get_width()
        
        actual_time = pg.time.get_ticks()
        if actual_time - last_time >= 1000:
            color_index = (color_index + 1) % len(rainbow_colors)
            last_time = actual_time
        
        
        back_button = fon.render("Back", True, (255, 255, 255))
        window.blit(back_button, (width//2 - back_button.get_width()//2, height - back_button.get_height() - 100))

        reset_button = fon.render(f"           RESET\n(clear all game)", True, (255, 255, 255))
        window.blit(reset_button, (width//2 - reset_button.get_width()//2, height - reset_button.get_height() - 170))

        bests = read_best_scores()
        best_time = bests[0]
        Coins = bests[1]
        best_mario_points = bests[2]
        best_game = bests[3]

        stats = fon.render(f"Best time: {best_time}\nMost Coins: {Coins}\nMost Mario points: {best_mario_points}\nBest Level (time,coins,points,level):\n{best_game}", True, (255, 255, 255))
        window.blit(stats, (width//2 - stats.get_width()//2, height//2 - stats.get_height()//2 - 50))
        
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        if width//2 - back_button.get_width()//2 <= mouse[0] <= width//2 + back_button.get_width()//2 and \
             height - back_button.get_height() - 100 <= mouse[1] <= height - back_button.get_height() - 100 + back_button.get_height():
            pg.draw.rect(window, (255, 0, 0), (width//2 - back_button.get_width()//2, height - back_button.get_height() - 100, back_button.get_width() , back_button.get_height()), 3)
            if click[0] == 1:
                start_screen(chosen_weapon,slider_value)
                running = False
        elif width//2 - reset_button.get_width()//2 <= mouse[0] <= width//2 + reset_button.get_width()//2 and \
             height - reset_button.get_height() - 170 <= mouse[1] <= height - reset_button.get_height() - 170 + reset_button.get_height():
            pg.draw.rect(window, (255, 0, 0), (width//2 - reset_button.get_width()//2, height - reset_button.get_height() - 170, reset_button.get_width() , reset_button.get_height()), 3)
            if click[0] == 1:
                with open("best.txt", "w") as file:
                    write_best_scores('','','','','','','')
                    file.write("")
                    running = False
                    chosen_weapon = None
                    start_screen(chosen_weapon,slider_value)
                

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                    if event.key == pg.K_f:
                        pg.display.toggle_fullscreen()
        pg.display.update()

def shop(slider_value):
    mario = Mario(width, height,chosen_weapon)
    running = True
    rainbow_colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (143, 0, 255)]
    color_index = 0
    last_time = pg.time.get_ticks()
    
    weapons = {'glock': 500, 'shotgun': 1000, 'rifle': 10000}  # Lista dostępnych broni i ich ceny
    # def write_best_scores(best_time, best_coins, best_mario_points, best_game, top_level,coin_counter)
    a,b,c,d,e,coin_counter,bronie = read_best_scores()
    bronie = bronie.split(',') if bronie else []
    while running:
        window.fill((0,0,0))
        startscreen.convert_alpha()
        startscreen.set_alpha(50)
        window.blit(startscreen, (0, 0))
        
        title = "Sklep"
        x_offset = 0
        for char in title:
            char_render = h1.render(char, True, rainbow_colors[color_index])
            window.blit(char_render, (width//2 - len(title)*char_render.get_width()//2 + x_offset, 10))
            x_offset += char_render.get_width()
        
        actual_time = pg.time.get_ticks()
        if actual_time - last_time >= 1000:
            color_index = (color_index + 1) % len(rainbow_colors)
            last_time = actual_time

        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()

        # Wyświetlanie przycisków kupna broni
        button_height = 250
        for weapon in weapons:
            czy_jest = True
            if coin_counter >= weapons[weapon] and weapon not in bronie:
                buy_weapon_button = fon.render(f"Buy {weapon} - {weapons[weapon]} coins", True, (255, 255, 255))
                pg.draw.rect(window, (0, 255, 0), (width//2 - buy_weapon_button.get_width()//2, button_height, buy_weapon_button.get_width(), buy_weapon_button.get_height()), 3)
            elif weapon in bronie:
                czy_jest = False
            else:
                buy_weapon_button = fon.render(f"Buy {weapon} - {weapons[weapon]} coins", True, (100, 100, 100))
            
            if czy_jest and width//2 - buy_weapon_button.get_width()//2 <= mouse[0] <= width//2 + buy_weapon_button.get_width()//2 and \
               button_height <= mouse[1] <= button_height + buy_weapon_button.get_height() :
                
                pg.draw.rect(window, (255, 0, 0), (width//2 - buy_weapon_button.get_width()//2, button_height, buy_weapon_button.get_width(), buy_weapon_button.get_height()), 3)
                if click[0] == 1 and coin_counter >= weapons[weapon] and weapon not in bronie:
                    running = False
                    coin_counter -= weapons[weapon]
                    bronie.append(weapon)
                    write_best_scores(a,b,c,d,e,coin_counter, ",".join(bronie))
                    del weapons[weapon]
                    start_screen(chosen_weapon,slider_value)
                    break
            if czy_jest:
                window.blit(buy_weapon_button, (width//2 - buy_weapon_button.get_width()//2, button_height))
                button_height += 70 
        
        # Przycisk powrotu
        back_button = fon.render("Back", True, (255, 255, 255))
        window.blit(back_button, (width//2 - back_button.get_width()//2, height - back_button.get_height() - 100))

        if width//2 - back_button.get_width()//2 <= mouse[0] <= width//2 + back_button.get_width()//2 and \
           height - back_button.get_height() - 100 <= mouse[1] <= height - back_button.get_height() - 100 + back_button.get_height():
            
            pg.draw.rect(window, (255, 0, 0), (width//2 - back_button.get_width()//2, height - back_button.get_height() - 100, back_button.get_width() , back_button.get_height()), 3)
            if click[0] == 1:
                running = False
                start_screen(chosen_weapon,slider_value)

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_f:
                    pg.display.toggle_fullscreen()
        pg.display.update()

def settings(slider_value):
    running = True
    rainbow_colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (143, 0, 255)]
    color_index = 0
    last_time = pg.time.get_ticks()
    
    clicked_key = None
    
    slider_width = 200
    slider_height = 20
    slider_x = width // 2 - slider_width // 2
    slider_y = 150

    
    for sound in [Mariusz_sfx, skok_sfx, monetkaegg_sfx, monetka_sfx, kill_sfx, minushp_sfx,off_sfx, head_sfx,boss_sounds,knock,hpminus,winez, mario_sound]:
        sound.set_volume(slider_value)
    
    while running:
        window.fill((0,0,0))
        startscreen.convert_alpha()
        startscreen.set_alpha(50)
        window.blit(startscreen, (0, 0))
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        title = "Settings"
        x_offset = 0
        for char in title:
            char_render = h1.render(char, True, rainbow_colors[color_index])
            window.blit(char_render, (width//2 - len(title)*char_render.get_width()//2 + x_offset, 10))
            x_offset += char_render.get_width()
        
        actual_time = pg.time.get_ticks()
        if actual_time - last_time >= 1000:
            color_index = (color_index + 1) % len(rainbow_colors)
            last_time = actual_time
        
        pg.draw.rect(window, (255, 255, 255), (slider_x, slider_y, slider_width, slider_height))
        pg.draw.rect(window, (0, 255, 0), (slider_x, slider_y, int(slider_value * slider_width), slider_height))
        slider_button_radius = slider_height // 2
        slider_button_x = slider_x + int(slider_value * slider_width)
        slider_button_y = slider_y + slider_height // 2
        pg.draw.circle(window, (0, 0, 0), (slider_button_x, slider_button_y), slider_button_radius)
        
        if (click[0] == 1 and slider_x <= mouse[0] <= slider_x + slider_width and
                               slider_y <= mouse[1] <= slider_y + slider_height):
            slider_button_x = mouse[0]
            if slider_button_x < slider_x:
                slider_button_x = slider_x
            elif slider_button_x > slider_x + slider_width:
                slider_button_x = slider_x + slider_width
            slider_value = (slider_button_x - slider_x) / slider_width
            for sound in [Mariusz_sfx, skok_sfx, monetkaegg_sfx, monetka_sfx, kill_sfx, minushp_sfx, off_sfx, head_sfx,boss_sounds,knock,hpminus,winez,mario_sound]:
                sound.set_volume(slider_value)
        
        if clicked_key:
            rect_y = 250 + (key_text.get_height() + 10) * list(key_bindings.keys()).index(clicked_key)
            rect_height = key_text.get_height() + 10
            pg.draw.rect(window, (255, 0, 0), (width//2 - max_text_width//2 - 5, rect_y - rect_height//2, max_text_width + 10, rect_height), 3)
        
        y_offset = 250
        max_text_width = max(key_text.get_width() for key_text in [fon.render(f"{action}: {pg.key.name(key)}", True, (255, 255, 255)) for action, key in key_bindings.items()])
        for action, key in key_bindings.items():
            text = f"{action}: {pg.key.name(key)}"
            key_text = fon.render(text, True, (255, 255, 255))
            text_rect = key_text.get_rect(center=(width//2, y_offset))
            window.blit(key_text, text_rect)
            if click[0] == 1 and text_rect.collidepoint(mouse):
                clicked_key = action
            y_offset += key_text.get_height() + 10
        
        back_button = fon.render("Back", True, (255, 255, 255))
        window.blit(back_button, (width//2 - back_button.get_width()//2, height - back_button.get_height() - 100))
        
        if width//2 - back_button.get_width()//2 <= mouse[0] <= width//2 + back_button.get_width()//2 and \
             height - back_button.get_height() - 100 <= mouse[1] <= height - back_button.get_height() - 100 + back_button.get_height():
            pg.draw.rect(window, (255, 0, 0), (width//2 - back_button.get_width()//2, height - back_button.get_height() - 100, back_button.get_width() , back_button.get_height()), 3)
            if click[0] == 1:
                start_screen(chosen_weapon,slider_value)
                running = False
        
        if click[0] == 1:
            for action, key in key_bindings.items():
                text = f"{action}: {pg.key.name(key)}"
                key_text = fon.render(text, True, (255, 255, 255))
                text_rect = key_text.get_rect(center=(width//2, y_offset))
                if text_rect.collidepoint(mouse):
                    clicked_key = action
        
        volume_text = fon.render(f"Volume: {int(slider_value*100)}%", True, (255, 255, 255))
        window.blit(volume_text, (width//2 - volume_text.get_width()//2, slider_y - volume_text.get_height() - 10))
        
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if clicked_key and event.key not in key_bindings.values():
                    key_bindings[clicked_key] = event.key
                    clicked_key = None

        pg.display.update()
def type_text(screen, font, text, color, pos):
    shadow_color = (50, 50, 50)
    shadow_offst = (3, 3)
    for i in range(len(text) + 1):
        render_text = font.render(text[:i], True, color)
        shadow_text = font.render(text[:i], True, shadow_color)
        screen.blit(shadow_text, (pos[0] + shadow_offst[0],pos[1] + shadow_offst[1]))
        screen.blit(render_text, pos)
        pg.display.update()
        if text[i-1] != " ":
            time.sleep(0.1)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

def bron_brak():
    font = pg.font.SysFont(None, 48)
    running = True
    window.fill((0,0,0))
    intro_text = "ABY PRZEJŚĆ DO TEGO POZIOMU,\n   MUSISZ KUPIĆ LUB WYBRAĆ\n                    BROŃ W EQ"
    
    type_text(window, font, intro_text, pg.Color('white'), (width//4, height//2.6))
    time.sleep(1)
    running = False
    while running:
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    running = False
def hugoboss():
    font = pg.font.SysFont(None, 48)
    running = True
    
    intro_text = "Teraz zawalczysz z bossem, Henrykiem srebrnorękim\n                            POWODZENIA!!!"
    type_text(window, font, intro_text, pg.Color('white'), (200, 100))
    time.sleep(1)
    running = False
    while running:
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    running = False
def congrats():
    font = pg.font.SysFont(None, 48)
    intro_text = "Brawo udało ci się pokonać\n  tego bezczelnego drania,\n            GRATULACJE"
    winez.play()
    type_text(window, font, intro_text, pg.Color('aliceblue'), (width//3, height//2.5))
    time.sleep(1)
    knock.set_volume(2)
    knock.play()

class Brick():     # W TABLICY 1 OZNACZA PODŁOGĘ 
    def __init__(self, x, y):
        self.width = pixel
        self.height = pixel
        self.x = x
        self.y = y
        self.hitbox = pg.Rect(self.x, self.y, self.width, self.height)
        self.image = pg.image.load('brick.png')

class Obstacle():   # W TABLICY 2 OZNACZA TUBĘ MARIO
    def __init__(self, x, y):
        self.width = pixel
        self.height = pixel
        self.x = x
        self.y = y
        self.hitbox = pg.Rect(self.x, self.y, self.width, self.height)
        self.image = pg.image.load('obstacleleft.png')
        self.hiden = False

class EndOfLevel():  # W TABLICY 3 OZNACZA PUNKT PRZEJSCIA NA NASTĘPY POZIOM
    def __init__(self, x, y):
        self.image = pg.image.load('Portal.png')
        self.width = pixel
        self.height = pixel
        self.x = x
        self.y = y
        self.hitbox = pg.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

class Enemy(): # W TABLICY 4 OZNACZA PRZECIWNIKÓW
    def __init__(self, x, y, e_x, e_y, speed,): 
        self.e_x = e_x 
        self.e_y = e_y
        self.speed = speed
        self.image = pg.image.load('enemy.png')
        self.width = pixel
        self.height = pixel
        self.x = x
        self.y = y
        self.s_x = x
        self.s_y = y
        self.hitbox = pg.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        self.flag_x = True
        self.flag_y = True
        self.random_x = 0
        self.random_y = 0
        self.change = False
        self.time = 0
        self.images = {
            'enemy': pg.image.load('enemy.png'),
            'enemy2': pg.image.load('enemy2.png')
        }

    def walk(self, czas):
            image = 'enemy'
            if round(czas - 0.2, 1) >= self.time:
                self.change = not self.change
                self.time = round(czas, 1)
            image += '2' if self.change else ''
            self.image = self.images[image]
    def tick(self,  czas):    #CHODZENIE DO PRZODU I DO TYŁU  ( ALBO GÓRA DÓŁ )PRZEZ POSTAĆ 
        if self.flag_x:
            if self.x < self.random_x:
                self.x += self.speed
                self.walk(czas)
            else:
                self.flag_x = False
                self.random_x = ri(self.s_x, self.s_x + self.e_x)
                
        else:
            if self.x > self.s_x:
                self.x -= self.speed
                self.walk(czas)
            else:
                self.flag_x = True
                self.random_x = ri(self.s_x, self.s_x + self.e_x)
        
        if self.flag_y:
            if self.y < self.random_y:
                self.y += self.speed
                self.walk(czas)
            else:
                self.flag_y = False
                self.random_y = ri(self.s_y, self.s_y + self.e_y)
        else:
            if self.y > self.s_y:
                self.y -= self.speed
                self.walk(czas)
            else:
                self.flag_y = True
                self.random_y = ri(self.s_y, self.s_y + self.e_y)
        self.hitbox = pg.Rect(self.x, self.y, self.width, self.height)

class Boss():
    def __init__(self, x, y):
        self.images = {
            'boss1': pg.image.load('Boss.png'),
            'boss2': pg.image.load('Boss2.png'),
            'Bosszbronia1': pg.image.load('Bosszbronia.png'),
            'Bosszbronia2': pg.image.load('Bosszbronia2.png'),
            'bullet' : pg.transform.flip(pg.image.load('bullet_boss.png'), True,False)
        }
        self.original_images = self.images  # Zachowujemy oryginalne obrazy
        self.image = self.images['boss1']
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = x
        self.y = y
        self.hitbox = pg.Rect(x, y, self.width, self.height)
        self.fire_rate = 60  # Pociski będą wypuszczane co 60 klatek
        self.fire_countdown = self.fire_rate  # Odliczanie do kolejnego strzału
        self.bullets = []
        self.image_timer = 30
        self.boss_timer = 30
        self.lifes = 100

    def update(self, mario):
        distance = self.x + self.width//2 - mario.x
        distance_to = 900

        
        if mario.x <= self.x + self.width//2:
            self.images = self.original_images 
        else:
            self.images = {key: pg.transform.flip(img, True, False) for key, img in self.original_images.items()}
        
        if -distance_to <= distance <= distance_to:
            if self.boss_timer > 0:
                self.boss_timer -= 1
            else:
                self.boss_timer = 30
                self.image = self.images['Bosszbronia2'] if self.image == self.images['Bosszbronia1'] else self.images['Bosszbronia1']
            
            if self.fire_countdown > 0:
                self.fire_countdown -= 1
            else:
                self.fire_bullet(mario)
                self.fire_countdown = self.fire_rate
        else:
            if self.image_timer > 0:
                self.image_timer -= 1
            else:
                self.image_timer = 30
                self.image = self.images['boss2'] if self.image == self.images['boss1'] else self.images['boss1']

    def fire_bullet(self, mario):
        dx = mario.x - self.x
        dy = mario.y - (self.y + self.height // 1.5)
        angle = math.atan2(dy, dx)
        bullet = Bullet_boss(self.x, self.y + self.height // 1.5, angle, self.images)
        self.bullets.append(bullet)

class Bullet_boss():
    def __init__(self, x, y, angle, images):
        self.x = x
        self.y = y
        self.speed = 5  # Szybkość pocisku
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed
        
        self.image = pg.transform.scale(images['bullet'], (pixel//2, pixel//2))
    
        self.hitbox = self.image.get_rect()
        self.hitbox.center = (self.x, self.y)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.hitbox.center = (self.x, self.y)


class Coin(): # W tablicy 5 i oznacza monety 
    def __init__(self,x,y):
        self.width = pixel
        self.height = pixel
        self.x = x
        self.y = y
        self.img = pg.image.load("coin.png")
        self.hitbox = pg.Rect(x, y, self.width, self.height)
        self.easter = False
        self.mega = False

class Bullet(): #POCISKI Z BRONI
    def __init__(self, x, y, direction, weapon):
        
        self.weapon = weapon
        if weapon == 'glock':
            self.width = pixel // 2
            self.height = pixel // 4
            self.speed = 10
            self.life = 1
        elif weapon == 'shotgun':
            self.width = pixel // 3
            self.height = pixel // 3
            self.speed = 5
            self.life = 2
        elif weapon == 'rifle':
            self.width = pixel // 1.5
            self.height = pixel // 4
            self.speed = 15
            self.life = 3
        self.x = x 
        self.y = y + 10
        self.startx = x
        self.starty = y
        self.direction = direction
        self.image = pg.transform.scale(pg.image.load('bullet.png'), (self.width, self.height))
        self.hitbox = pg.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        
        
    def tick(self, window):
        if self.direction == 'left':
            self.x -= self.speed
            self.image = pg.transform.scale(pg.transform.flip(pg.image.load('bullet.png'), True, False), (self.width, self.height))
        else:
            self.x += self.speed
        self.hitbox = pg.Rect(self.x, self.y, self.width, self.height)

class Kolce(): # W TABLICY 7 
    def __init__(self,x,y):
        self.width = pixel
        self.height = pixel
        self.x = x
        self.y = y
        self.image = pg.image.load("kolce.png")
        self.hitbox = pg.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.easter = False

class Mario(): # NASZ GRACZ 
    def __init__(self, width, height, chosen_weapon,):
        self.image = pg.image.load('mario.png').convert_alpha() 
        self.width = pixel
        self.height = pixel
        self.x = width / 2 - self.width / 2
        self.y = height - 2 * self.height 
        self.hitbox = pg.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        self.jump = False
        self.jump_height = 250
        self.jump_distance = 0
        self.invincible_time = 0
        self.time = 0
        self.images = {
            'left': pg.image.load('mario.png').convert_alpha(),
            'right': pg.transform.flip(pg.image.load('mario.png').convert_alpha(), True, False),
            'left_alt': pg.image.load('mario1.png').convert_alpha(),
            'right_alt': pg.transform.flip(pg.image.load('mario1.png').convert_alpha(), True, False),
            'stand': pg.image.load('mariostoi.png').convert_alpha(),
            'stand2': pg.image.load('mariostoi2.png').convert_alpha()
        }
        self.change = True
        self.weapons = read_best_scores()[6].split(',')
        self.weapon = chosen_weapon
        self.bullets = []
        self.last_shot_time = 0
        if self.weapon == 'glock':
            self.shoot_delay = 1
        if self.weapon == 'shotgun':
            self.shoot_delay = 2
        if self.weapon == 'rifle':
            self.shoot_delay = 0.2
            

            
    def walk(self, right, czas):
        direction = 'right' if right else 'left'
        if round(czas - 0.2, 1) >= self.time:
            self.change = not self.change
            self.time = round(czas, 1)
        direction += '_alt' if self.change else ''
        self.image = self.images[direction]

    def stand(self, czas):
        standing = 'stand'
        if round(czas - 0.3, 1) >= self.time:
            self.change = not self.change
            self.time = round(czas, 1)
        standing += '2' if self.change else ''
        self.image = self.images[standing]

    def tick(self, bricks, czas, window):
        keys = pg.key.get_pressed()
        self.speed = 9

        okej = True # zmeinna czy self.image mario został zmieniony
        #-------------CHODZENIE LEWO PRAWO-------------#
        if keys[key_bindings["move_left"]] and self.x > 0:
            self.x -= self.speed
            x = True
            okej = False
            if self.jump:
                self.image = pg.transform.flip(pg.image.load('marioskok.png').convert_alpha(), True, False)
            else:
                self.walk(x, czas)
        if keys[key_bindings["move_right"]] and self.x < bricks[-1].width - self.width:
            self.x += self.speed
            x = False
            okej = False
            if self.jump:
                self.image = pg.image.load('marioskok.png').convert_alpha()
            else:
                self.walk(x, czas)
        #------------------------------

        #---------------SKAKANIE-----------------#
        if keys[key_bindings["jump"]] and not self.jump and self.y == bricks[-1].y - self.height - bricks[-1].height:
            self.jump = True
            self.jump_distance = 0
            skok_sfx.play()
        if self.jump:
            if self.jump_distance < self.jump_height:
                self.y -= self.speed
                self.jump_distance += self.speed
                if okej:
                    self.image = pg.image.load('marioskok.png').convert_alpha()
                    okej = False
            else:
                self.jump = False
        else:
            if self.y < bricks[-1].y - self.height - bricks[-1].height:
                self.y += self.speed
                
            if self.y > bricks[-1].y - self.height - bricks[-1].height:
                self.y = bricks[-1].y - self.height - bricks[-1].height
        #------------------------------------#
        #----------------STRZAŁY--------------#
        try:
            if keys[key_bindings["attack"]] and czas - self.last_shot_time > self.shoot_delay:
                if x:
                    direction = 'left'
                else:
                    direction = 'right'
                if self.weapon == None:
                    pass
                elif self.weapon == 'shotgun':
                    self.bullets.append(Bullet(self.x , self.y+20, direction, self.weapon))
                    self.bullets.append(Bullet(self.x, self.y, direction, self.weapon))
                    self.bullets.append(Bullet(self.x, self.y-20, direction, self.weapon))
                else:
                    self.bullets.append(Bullet(self.x, self.y, direction, self.weapon))
                self.last_shot_time = czas
        except (UnboundLocalError,AttributeError):
            pass
        for bullet in self.bullets:
            bullet.tick(window)
        #---------------STANIE#--------------#
        if okej:
            self.stand(czas)
        #------------------------------------#
        self.hitbox = pg.Rect(self.x, self.y, self.image.get_width(), self.image.get_height()) # resetowanie hitboxów

def generatelevel(levels, i, camera_x, bricks, obstacles, EndOfLevels, Enemies,Coins, kolce, boss, mario):  # generowanie poziomu
    list = levels[i]   # wybieranie aktualnego poziomu czyli 2 wymiar w tablicy
    for index_rzad, row in enumerate(list): #wchodzi w 3 wymiar,iteruje po rzędzie(y)enumerate używa się w listach(działa prawie jak rand)
        y = pixel * index_rzad  #aktualny y na tablicy
        for index_kolumna, value in enumerate(row): #ideruje po elementach w tablicy i sprawdza sekcje if'ów
            value = str(value)
            if value[0] == '1':
                brick = Brick(pixel * index_kolumna, y)
                # pg.draw.rect(window, (165, 42, 42), brick.hitbox.move(-camera_x, 0))
                bricks.append(brick)
            if value[0] == '2':
                obstacle = Obstacle(pixel * index_kolumna, y)
                if value[2] == '1':
                    obstacle.image = pg.image.load('obstacleleft.png')
                if value[2] == '2':
                    obstacle.image = pg.image.load('obstacleright.png')
                if value[2] == '3':
                    obstacle.image = pg.image.load('obstacletopleft.png')
                if value[2] == '4':
                    obstacle.image = pg.image.load('obstacletopright.png')
                if value[2] == '5':
                    obstacle.image = pg.image.load('obstacletopleft.png')
                    obstacle.hiden = True
                if value[2] == '6':
                    obstacle.image = pg.image.load('obstacletopright.png')
                    obstacle.hiden = True


                # pg.draw.rect(window, (10, 123, 23), obstacle.hitbox.move(-camera_x, 0))
                obstacles.append(obstacle)
            if value[0] == '3':
                endoflevel = EndOfLevel(pixel * index_kolumna, y)
                # pg.draw.rect(window, (200, 255, 23), endoflevel.hitbox.move(-camera_x, 0))
                EndOfLevels.append(endoflevel)
            if value[0] == '4':
                enemy = Enemy(pixel * index_kolumna, y, int(value[2])*pixel, int(value[3])*pixel, int(value[4]))
                # pg.draw.rect(window, (0, 255, 23), enemy.hitbox.move(-camera_x, 0))
                Enemies.append(enemy)
            if value[0] == '5':
                coin = Coin(pixel * index_kolumna, y)
                try:
                    if value[2] == '1':
                        coin.easter = True
                    if value[2] == '2':
                        coin.mega = True
                except:
                    coin.easter = False
                # pg.draw.rect(window, (255,255,0),coin.hitbox.move(-camera_x,0))
                Coins.append(coin)
            if value[0] == '6':
                enemy = Enemy(pixel * index_kolumna, y, int(value[2])*pixel, int(value[3])*pixel, int(value[4]))
                enemy.images =  {
                    'enemy': pg.image.load('bird.png'),
                    'enemy2': pg.image.load('bird2.png')
                }
                Enemies.append(enemy)
            if value[0] == '7':
                kolec = Kolce(pixel * index_kolumna, y)
                kolce.append(kolec)
            if value[0] == '8':
                bos = Boss(pixel * index_kolumna, y)
                boss.append(bos)
    bricks[-1].width = pixel * (index_kolumna + 1)

def hidenlevel(chosen_weapon, czas_poziomu, Mario_points_poziomu, coin_counter_poziomu, lifes,clock, camera_x, _,okej,Mario_points,czy_escape,czas,slider_value):
    mario = Mario(width, height,chosen_weapon)
    if _ == 5:
        mario.jump_height = 400
    run = True
    best_time, best_coins, best_mario_points, Best_game, top_level, coin_counter, bronie = read_best_scores()  # Odczytaj najlepsze wyniki
    camera_speed = 5
    from hidenlevels import levelion
    hidenlevel = levelion
    #--------------ELEMENY W GRZE------------#
    bricks = []
    obstacles = []
    EndOfLevels = []
    Enemies = []
    Coins = []
    kolce = []
    Boss = []
    #----------------------------------------#
    generatelevel(hidenlevel, _, camera_x, bricks, obstacles, EndOfLevels, Enemies, Coins, kolce, Boss, mario)  # GENEROWAniE ŚWIATA ZALEŻNIE OD POZIOMU
    if _ < top_level:
        Coins = []
    while run:
        #-----------------PODSTAWA------------------#
        pg.display.set_caption(f"Mario Syndrom Adventure - {int(clock.get_fps())} fps")
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                czy_escape = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_f:
                    pg.display.toggle_fullscreen()
                if event.key == pg.K_ESCAPE:
                    run = False
                    czy_escape = True
        #------------------------------------------#

        #--------------Sekcja odpowiedzialana za kamerę---------------#
        target_camera_x = mario.x - (width / 2 - mario.hitbox.width / 2)
        camera_x += (target_camera_x - camera_x) / camera_speed

        if camera_x < 0:
            camera_x = 0
        elif camera_x > bricks[-1].width - width:
            camera_x = bricks[-1].width - width
        #-------------------------------------------------------------#
        #---------------TŁO-----------------------#
        window.fill((33, 33, 33))           

        #-----------------------------------------#
        
        mario.tick(bricks, czas, window) #Tick postaci odpowiedzialny za przemieszczanie postaci
        czas += clock.get_time() / 1000 #liczenie czasu
        czas_poziomu += clock.get_time() / 1000
        #-----------------------------SEKCJA ODPOWIEDZIALNA ZA POKAZYWANIE RZECZY NA EKRANIE------------------#

        for bullet in mario.bullets:
            # pg.draw.rect(window, (165, 42, 42), bullet.hitbox.move(-camera_x,0))
            window.blit(bullet.image , (bullet.x - camera_x, bullet.y))
            for brick in bricks:
                if bullet.hitbox.colliderect(brick.hitbox):
                    mario.bullets.remove(bullet)
                    break
            for obstacle in obstacles:
                if bullet.hitbox.colliderect(obstacle.hitbox):
                    mario.bullets.remove(bullet)
                    break
            for enemy in Enemies:
                if bullet.hitbox.colliderect(enemy.hitbox):
                    mario.bullets.remove(bullet)
                    Enemies.remove(enemy)
                    kill_sfx.play()
                    Mario_points += 100
                    Mario_points_poziomu +=100
                    if Mario_points % 1000 == 0:
                        mario.invincible_time = 300
                    break

        for kolec in kolce :
            window.blit(kolec.image, (kolec.x-camera_x, kolec.y))
            if kolec.hitbox.colliderect(mario.hitbox) and mario.invincible_time <= 0:
                lifes-=1
                mario.invincible_time = 50
                minushp_sfx.play()

        for brick in bricks:   # Spwanuje cegły
            # pg.draw.rect(window, (165, 42, 42), brick.hitbox.move(-camera_x, 0))
            window.blit(brick.image, (brick.x-camera_x, brick.y))
            if (mario.x + mario.hitbox.width + mario.speed > brick.x and
                mario.x - mario.speed <= brick.x + brick.width and
                mario.y + mario.height - mario.speed > brick.y and
                mario.y + mario.speed< brick.y + brick.height):
                if mario.x + mario.hitbox.width<= brick.x + (brick.width // 2):
                    mario.x = brick.x - mario.speed - mario.hitbox.width
                else:
                    mario.x = brick.x + mario.speed + brick.width
            elif (mario.y - mario.speed < brick.y + brick.height and
                mario.y >= brick.y + (brick.height // 2) - mario.speed and
                mario.x + mario.hitbox.width >= brick.x and
                mario.x <= brick.x + brick.width):

                mario.y = brick.y + brick.height + mario.speed - 1
            # elif mario.hitbox.colliderect(brick.hitbox) and mario.x + mario.hitbox.width >= brick.x and mario.x <= brick.x + brick.width:
            elif (mario.hitbox.colliderect(brick.hitbox) and
                mario.y + mario.height + mario.speed <= brick.y + (brick.height // 2) - mario.speed and
                mario.x + mario.hitbox.width >= brick.x and
                mario.x <= brick.x + brick.width):

                mario.y = brick.y - mario.height - mario.speed + 1
                mario.initial_y = mario.y
                mario.jump = False    
                keys = pg.key.get_pressed()
                if keys[key_bindings["jump"]] and not mario.jump:
                    skok_sfx.play()
                    mario.jump = True
                    mario.jump_distance = 0
                    mario.initial_y = mario.y 
                if mario.jump:
                    if mario.jump_distance < mario.jump_height:
                        mario.y -= mario.speed
                        mario.jump_distance += mario.speed
                    else:
                        mario.jump = False
                else:
                    if mario.y < mario.initial_y - mario.height:
                        mario.y += mario.speed
                    if mario.y > mario.initial_y - mario.height: 
                        mario.y = mario.initial_y
                

        for endoflevel in EndOfLevels: # spwanuje punkty konca poziomu
            # pg.draw.rect(window, (200, 255, 23), endoflevel.hitbox.move(-camera_x, 0))
            window.blit(endoflevel.image , (endoflevel.x - camera_x, endoflevel.y))
            if mario.hitbox.colliderect(endoflevel.hitbox):
                run = False
        
        for enemy in Enemies: # Spwanuje Przeciwników którzy po wskoczeniu na nich znikają 
            # pg.draw.rect(window, (0, 255, 23), enemy.hitbox.move(-camera_x, 0))
            window.blit(enemy.image , (enemy.x - camera_x, enemy.y))
            enemy.tick(czas)
            if mario.hitbox.colliderect(enemy.hitbox) and mario.y + mario.height - (mario.speed*2) <= enemy.y and mario.invincible_time <=0:
                Enemies.remove(enemy)
                Mario_points += 100
                Mario_points_poziomu +=100
                if Mario_points % 1000 == 0:
                    mario.invincible_time = 300
                kill_sfx.play()
            elif mario.hitbox.colliderect(enemy.hitbox) and mario.invincible_time <= 0:
                lifes -= 1
                mario.invincible_time = 50
                minushp_sfx.play()

        for obstacle in obstacles:  # Spwanuje Tuby mario na których można skakać i nie można w nie wejść 
            # pg.draw.rect(window, (10, 123, 23), obstacle.hitbox.move(-camera_x, 0))
            window.blit(obstacle.image , (obstacle.x - camera_x, obstacle.y))
            if mario.hitbox.colliderect(obstacle.hitbox) and mario.x + mario.hitbox.width >= obstacle.x and mario.x <= obstacle.x + obstacle.width:
                mario.y = obstacle.y - mario.height - mario.speed + 1
                mario.initial_y = mario.y 
                keys = pg.key.get_pressed()
                if keys[key_bindings["jump"]] and not mario.jump:
                    skok_sfx.play()
                    mario.jump = True
                    mario.jump_distance = 0
                    mario.initial_y = mario.y 
                if mario.jump:
                    if mario.jump_distance < mario.jump_height:
                        mario.y -= mario.speed
                        mario.jump_distance += mario.speed
                    else:
                        mario.jump = False
                else:
                    if mario.y < mario.initial_y - mario.height:
                        mario.y += mario.speed
                    if mario.y > mario.initial_y - mario.height: 
                        mario.y = mario.initial_y
                if keys[key_bindings["use"]] and mario.x + mario.width >= 3904 and mario.x <= 3968 and _ == 2:
                    run = False
                    if top_level < _+1:
                        top_level = _ + 1
                    write_best_scores(best_time, best_coins, best_mario_points, Best_game, top_level, coin_counter, bronie)
                    main(_+2, chosen_weapon, czas, Mario_points,slider_value)
                    break
                elif keys[key_bindings["use"]] and mario.x + mario.width >= 3904 and mario.x <= 3968:
                    run = False
                    subprocess.call('WIN_GAME.bat', shell=True)
                    start_screen(chosen_weapon,slider_value)
                    
                    
            elif mario.x + mario.hitbox.width + mario.speed > obstacle.x and mario.x - mario.speed <= obstacle.x + obstacle.width and mario.y + mario.height - 1 > obstacle.y:
                if mario.x + mario.hitbox.width<= obstacle.x + obstacle.width // 2:
                    mario.x = obstacle.x - mario.speed - mario.hitbox.width
                else:
                    mario.x = obstacle.x + mario.speed + obstacle.width

        for coin in Coins:
            # pg.draw.rect(window, (10, 123, 23), coin.hitbox.move(-camera_x, 0))
            window.blit(coin.img , (coin.x - camera_x, coin.y))
            if coin.hitbox.colliderect(mario.hitbox):
                if coin.easter:
                    monetkaegg_sfx.play()
                else:
                    monetka_sfx.play()
                Coins.remove(coin)
                if coin.mega:
                    coin_counter += 100
                    coin_counter_poziomu += 100
                else:
                    coin_counter += 1
                    coin_counter_poziomu += 1
    

        if mario.invincible_time > 0:
            opacity = 128
        else:
            opacity = 255
        mario.image.set_alpha(opacity)
        # pg.draw.rect(window, (255, 0, 0), mario.hitbox.move(-camera_x, 0))            
        window.blit(mario.image, (mario.hitbox.x - camera_x, mario.hitbox.y))


            #------------NAPISY------------------#
                #------------------CZAS------------------#
        x = f"TIME\n{str(int(czas)).zfill(6)}"
        shadow_color = (50, 50, 50)
        shadow_offst = (2, 2)
        shadow_text = fon.render(x, False, shadow_color)
        window.blit(shadow_text, (width - (width//4) + shadow_offst[0], 1 + shadow_offst[1]))
        Time = fon.render(x, False, (230, 230, 230))
        window.blit(Time, (width - (width//4), 1))
                #----------------------------------------#
                #---------------ŚWIAT_-------------------#
        y = f"{str(_+1)} LEVEL"
        shadow_text = fon.render(y, False, shadow_color)
        window.blit(shadow_text, (width - (width//2) + shadow_offst[0], 1 + shadow_offst[1]))
        Time = fon.render(y, False, (230, 230, 230))
        window.blit(Time, (width - (width//2), 1))
                #----------------------------------------#
                #---------------LICZNIK COINÓW-----------#
        z = f"COINS\n{coin_counter}"
        shadow_text = fon.render(z, False, shadow_color)
        window.blit(shadow_text, (width - (width//1.4) + shadow_offst[0], 1 + shadow_offst[1]))
        Time = fon.render(z, False, (230, 230, 230))
        window.blit(Time, (width - (width//1.4), 1))
                #----------------------------------------#
                #---------------MARIO POINTS-----------#
        ź = f"Mario\n{str(Mario_points).zfill(10)}"
        shadow_text = fon.render(ź, False, shadow_color)
        window.blit(shadow_text, (10 + shadow_offst[0], 1 + shadow_offst[1]))
        Time = fon.render(ź, False, (230, 230, 230))
        window.blit(Time, (10, 1))
                #--------------------------------------#
                #---------------ŻYCIA------------------#

        serca = [serce_zlamane] * 3

        for i in range(lifes):
            serca[i] = serce_OKEJ
        for index, serce in enumerate(serca):
            window.blit(serce, (10 + index * (serce.get_width() + 10), height - 100))

                #--------------------------------------#
            #-------------------------------------#

        #------------------------------------------------------------------------------#
        if lifes <= 0:
            run = False
            start_screen(chosen_weapon,slider_value)
        pg.display.update()
        clock.tick(60)

        if mario.invincible_time > 0:
            mario.invincible_time -= 1
        
        #-------------------------ZAPIASYWANIE NAJLEPSZYCH WYNIKÓW----------------------#
        try:
            if coin_counter > best_coins:
                best_coins = coin_counter
            if Mario_points > best_mario_points:
                best_mario_points = Mario_points     
        except TypeError:
            best_coins = coin_counter
            best_mario_points = Mario_points
        if not czy_escape:
            write_best_scores(best_time, best_coins, best_mario_points, Best_game, top_level, coin_counter, bronie)
        #------------------------------------------------------------------------------#
    
        if czy_escape:
            run = False
            start_screen(chosen_weapon,slider_value)
        try:
            if (int(czas_poziomu) <= int(Best_game[1]) or int(Best_game[1]) == 0) and coin_counter_poziomu >= int(Best_game[4]) and Mario_points_poziomu >= int(Best_game[7]):
                Best_game = [int(czas_poziomu), coin_counter_poziomu, Mario_points_poziomu, _+1]
            if int(czas_poziomu) < best_time or best_time == 0:
                best_time = int(czas_poziomu)
            if _ + 1 > top_level:
                top_level = _ + 1
        except ValueError:
            best_time = int(czas_poziomu)
            Best_game = [int(czas_poziomu), coin_counter_poziomu, Mario_points_poziomu, _+1]
            top_level = _ + 1
        if not czy_escape:
            write_best_scores(best_time, best_coins, best_mario_points, Best_game, top_level, coin_counter, bronie)
    return Mario_points
def main(level, chosen_weapon, czas, Mario_points,slider_value):
    mario_sound.stop()
    mario_sound.play(-1)
    Mariusz_sfx.stop()
    camera_speed = 5 # PRĘDKOŚĆ KAMERY 
    run = True #OGÓLNA PĘTLA GRY
    best_time, best_coins, best_mario_points, Best_game, top_level, coin_counter, bronie = read_best_scores()  # Odczytaj najlepsze wyniki
    level -=1
    for _ in range(level , len(levels)):   # PĘTLA POZIOMÓW
        czas_poziomu = 0
        Mario_points_poziomu = 0
        coin_counter_poziomu = 0
        skok_sfx.stop()
        lifes = 3
        run2 = True  # RUN ODPOWIEDZIALNY ZA POZIOM
        clock = pg.time.Clock()
        mario = Mario(width, height, chosen_weapon)   #POSTAĆ 
        if _ == 2 or _ == 4:
            mario.x = 2*pixel
        if _ == 4:
            if not bronie:
                run2 = False
                run = False
                bron_brak()
                start_screen(chosen_weapon,slider_value)
            else:
                mario_sound.stop()
                boss_sounds.play(-1)
        else:
            boss_sounds.stop()
        prawdapoziom5 = True
        camera_x = mario.x - (width / 2 - mario.hitbox.width / 2)   #KAMERA 
        #--------------ELEMENY W GRZE------------#
        bricks = []
        obstacles = []
        EndOfLevels = []
        Enemies = []
        Coins = []
        kolce = []
        Boss = []
        #----------------------------------------#
        generatelevel(levels, _, camera_x, bricks, obstacles, EndOfLevels, Enemies, Coins, kolce,Boss, mario)  # GENEROWAniE ŚWIATA ZALEŻNIE OD POZIOMU
        # if _ <= top_level:
        #     Coins = []
        while run and run2:   #pętla główna (gry)
            czy_escape = False
            #-----------------PODSTAWA------------------#
            pg.display.set_caption(f"Mario Syndrom Adventure - {int(clock.get_fps())} fps")
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                    run2 = True
                    czy_escape = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_f:
                        pg.display.toggle_fullscreen()
                    if event.key == pg.K_ESCAPE:
                        run = False
                        run2 = False
                        czy_escape = True
                        boss_sounds.stop()
                        mario_sound.stop()
            #------------------------------------------#

            #--------------Sekcja odpowiedzialana za kamerę---------------#
            target_camera_x = mario.x - (width / 2 - mario.hitbox.width / 2)
            camera_x += (target_camera_x - camera_x) / camera_speed

            if camera_x < 0:
                camera_x = 0
            elif camera_x > bricks[-1].width - width:
                camera_x = bricks[-1].width - width
            #-------------------------------------------------------------#
            #---------------TŁO-----------------------#
            if _ != 5:
                window.fill((255, 255, 255))           
                window.blit(background, (0 - camera_x * 0.5, 0))
                window.blit(background, (background.get_width() - camera_x * 0.5, 0))
                window.blit(background, ((background.get_width()*2) - camera_x * 0.5, 0))
            else:
                window.fill((255, 255, 255))           
                window.blit(background_special, (0 - camera_x * 0.5, 0))
                window.blit(background_special, (background_special.get_width() - camera_x * 0.5, 0))
                window.blit(background_special, ((background_special.get_width()*2) - camera_x * 0.5, 0))

            #-----------------------------------------#

            mario.tick(bricks, czas, window) #Tick postaci odpowiedzialny za przemieszczanie postaci
            czas += clock.get_time() / 1000 #liczenie czasu
            czas_poziomu += clock.get_time() / 1000

            #-----------------------------SEKCJA ODPOWIEDZIALNA ZA POKAZYWANIE RZECZY NA EKRANIE------------------#

            for bullet in mario.bullets:

                # pg.draw.rect(window, (165, 42, 42), bullet.hitbox.move(-camera_x,0))
                window.blit(bullet.image , (bullet.x - camera_x, bullet.y))
                for Bos in Boss:
                    if bullet.hitbox.colliderect(Bos.hitbox):
                        mario.bullets.remove(bullet)
                        if Bos.lifes != 0:
                            Bos.lifes -= 1
                            hpminus.play()
                            if Bos.lifes == 0:
                                Boss.remove(Bos)
                                Mario_points += 10000
                                Mario_points_poziomu +=10000
                                congrats()
                                
                            break
                    for bulletb in Bos.bullets:
                        if bulletb.hitbox.colliderect(bullet.hitbox):
                            mario.bullets.remove(bullet)
                            Bos.bullets.remove(bulletb)
                if bullet.x >=bullet.startx + 600 or bullet.x <= bullet.startx - 600:
                    mario.bullets.remove(bullet)
                    break
                for brick in bricks:
                    if bullet.hitbox.colliderect(brick.hitbox):
                        mario.bullets.remove(bullet)
                        break
                for obstacle in obstacles:
                    if bullet.hitbox.colliderect(obstacle.hitbox):
                        mario.bullets.remove(bullet)
                        break
                for enemy in Enemies:
                    if bullet.hitbox.colliderect(enemy.hitbox):
                        if bullet.life != 0:
                            bullet.life-=1
                            if bullet.life == 0:
                                mario.bullets.remove(bullet)
                        Enemies.remove(enemy)
                        kill_sfx.play()
                        Mario_points += 100
                        Mario_points_poziomu +=100
                        if Mario_points % 1000 == 0:
                            mario.invincible_time = 300
                        break



            for kolec in kolce :
                window.blit(kolec.image, (kolec.x-camera_x, kolec.y))
                if kolec.hitbox.colliderect(mario.hitbox) and mario.invincible_time <= 0:
                    lifes-=1
                    mario.invincible_time = 50
                    minushp_sfx.play()

            for brick in bricks:   # Spwanuje cegły
                # pg.draw.rect(window, (165, 42, 42), brick.hitbox.move(-camera_x, 0))
                window.blit(brick.image, (brick.x-camera_x, brick.y))
                if (mario.x + mario.hitbox.width + mario.speed > brick.x and
                    mario.x - mario.speed <= brick.x + brick.width and
                    mario.y + mario.height - mario.speed > brick.y and
                    mario.y + mario.speed< brick.y + brick.height):
                    if mario.x + mario.hitbox.width<= brick.x + (brick.width // 2):
                        mario.x = brick.x - mario.speed - mario.hitbox.width
                    else:
                        mario.x = brick.x + mario.speed + brick.width
                elif (mario.y - mario.speed < brick.y + brick.height and
                    mario.y >= brick.y + (brick.height // 2) - mario.speed and
                    mario.x + mario.hitbox.width >= brick.x and
                    mario.x <= brick.x + brick.width):

                    mario.y = brick.y + brick.height + mario.speed - 1
                # elif mario.hitbox.colliderect(brick.hitbox) and mario.x + mario.hitbox.width >= brick.x and mario.x <= brick.x + brick.width:
                elif (mario.hitbox.colliderect(brick.hitbox) and
                    mario.y + mario.height + mario.speed <= brick.y + (brick.height // 2) - mario.speed and
                    mario.x + mario.hitbox.width >= brick.x and
                    mario.x <= brick.x + brick.width):

                    mario.y = brick.y - mario.height - mario.speed + 1
                    mario.initial_y = mario.y
                    mario.jump = False    
                    keys = pg.key.get_pressed()
                    if keys[key_bindings["jump"]] and not mario.jump:
                        skok_sfx.play()
                        mario.jump = True
                        mario.jump_distance = 0
                        mario.initial_y = mario.y 
                    if mario.jump:
                        if mario.jump_distance < mario.jump_height:
                            mario.y -= mario.speed
                            mario.jump_distance += mario.speed
                        else:
                            mario.jump = False
                    else:
                        if mario.y < mario.initial_y - mario.height:
                            mario.y += mario.speed
                        if mario.y > mario.initial_y - mario.height: 
                            mario.y = mario.initial_y
                    


            for endoflevel in EndOfLevels: # spwanuje punkty konca poziomu
                # pg.draw.rect(window, (200, 255, 23), endoflevel.hitbox.move(-camera_x, 0))
                window.blit(endoflevel.image , (endoflevel.x - camera_x, endoflevel.y))
                if mario.hitbox.colliderect(endoflevel.hitbox):
                    run2 = False
            
            for enemy in Enemies: # Spwanuje Przeciwników którzy po wskoczeniu na nich znikają 
                # pg.draw.rect(window, (0, 255, 23), enemy.hitbox.move(-camera_x, 0))
                window.blit(enemy.image , (enemy.x - camera_x, enemy.y))
                enemy.tick(czas)
                if mario.hitbox.colliderect(enemy.hitbox) and mario.y + mario.height - (mario.speed*2) <= enemy.y and mario.invincible_time <=0:
                    Enemies.remove(enemy)
                    Mario_points += 100
                    Mario_points_poziomu +=100
                    if Mario_points % 1000 == 0:
                        mario.invincible_time = 300
                    kill_sfx.play()
                elif mario.hitbox.colliderect(enemy.hitbox) and mario.invincible_time <= 0:
                    lifes -= 1
                    mario.invincible_time = 50
                    minushp_sfx.play()

            for obstacle in obstacles:  # Spwanuje Tuby mario na których można skakać i nie można w nie wejść 
                # pg.draw.rect(window, (10, 123, 23), obstacle.hitbox.move(-camera_x, 0))
                window.blit(obstacle.image , (obstacle.x - camera_x, obstacle.y))
                if mario.hitbox.colliderect(obstacle.hitbox) and mario.x + mario.hitbox.width >= obstacle.x and mario.x <= obstacle.x + obstacle.width:
                    mario.y = obstacle.y - mario.height - mario.speed + 1
                    mario.initial_y = mario.y 
                    keys = pg.key.get_pressed()
                    if keys[key_bindings["jump"]] and not mario.jump:
                        skok_sfx.play()
                        mario.jump = True
                        mario.jump_distance = 0
                        mario.initial_y = mario.y 
                    if mario.jump:
                        if mario.jump_distance < mario.jump_height:
                            mario.y -= mario.speed
                            mario.jump_distance += mario.speed
                        else:
                            mario.jump = False
                    else:
                        if mario.y < mario.initial_y - mario.height:
                            mario.y += mario.speed
                        if mario.y > mario.initial_y - mario.height: 
                            mario.y = mario.initial_y
                    if _ == 2 and mario.x + mario.width >= 1792 and mario.x  <= 1856 and keys[key_bindings["use"]]:
                        run = False
                        run2 = False
                        Mario_points += hidenlevel(chosen_weapon, czas_poziomu, Mario_points_poziomu, coin_counter_poziomu, lifes,clock, camera_x,_,mario,Mario_points,czy_escape,czas,slider_value)
                        break
                    if _ == 5 and mario.x + mario.width >= 3968 and mario.x  <= 4032 and keys[key_bindings["use"]]:
                        run = False
                        run2 = False
                        Mario_points += hidenlevel(chosen_weapon, czas_poziomu, Mario_points_poziomu, coin_counter_poziomu, lifes,clock, camera_x,_,mario,Mario_points,czy_escape,czas,slider_value)
                        break
                     
                elif mario.x + mario.hitbox.width + mario.speed > obstacle.x and mario.x - mario.speed <= obstacle.x + obstacle.width and mario.y + mario.height - 1 > obstacle.y:
                    if mario.x + mario.hitbox.width<= obstacle.x + obstacle.width // 2:
                        mario.x = obstacle.x - mario.speed - mario.hitbox.width
                    else:
                        mario.x = obstacle.x + mario.speed + obstacle.width

            for coin in Coins:
                # pg.draw.rect(window, (10, 123, 23), coin.hitbox.move(-camera_x, 0))
                window.blit(coin.img , (coin.x - camera_x, coin.y))
                if coin.hitbox.colliderect(mario.hitbox):
                    if coin.easter:
                        monetkaegg_sfx.play()
                    else:
                        monetka_sfx.play()
                    Coins.remove(coin)
                    if coin.mega:
                        coin_counter += 100
                        coin_counter_poziomu += 100
                    else:
                        coin_counter += 1
                        coin_counter_poziomu += 1
        
            for Bos in Boss:
                window.blit(Bos.image, (Bos.x - camera_x, Bos.y))
                Bos.update(mario)
                text = fon.render(f"Life {str(Bos.lifes).zfill(2)}%", False, (255,255,255), (255,0,0))
                window.blit(text, (Bos.x - camera_x + text.get_width()//4, Bos.y - text.get_height()))
                if mario.hitbox.colliderect(Bos.hitbox):
                    mario.x -= mario.speed
                # Aktualizacja i rysowanie pocisków
                for bullet in Bos.bullets:
                    bullet.update()
                    if bullet.hitbox.colliderect(mario.hitbox):
                        lifes -= 1
                        Bos.bullets.remove(bullet)
                        off_sfx.play()
                    window.blit(bullet.image, (bullet.x - camera_x, bullet.y))

            if mario.invincible_time > 0:
                opacity = 128
            else:
                opacity = 255
            mario.image.set_alpha(opacity)
            # pg.draw.rect(window, (255, 0, 0), mario.hitbox.move(-camera_x, 0))            
            window.blit(mario.image, (mario.hitbox.x - camera_x, mario.hitbox.y))
            if _ == 4 and prawdapoziom5:
                prawdapoziom5 = False
                hugoboss()

            if _ != 5:
                    #------------NAPISY------------------#
                        #------------------CZAS------------------#
                x = f"TIME\n{str(int(czas)).zfill(6)}"
                shadow_color = (50, 50, 50)
                shadow_offst = (2, 2)
                shadow_text = fon.render(x, False, shadow_color)
                window.blit(shadow_text, (width - (width//4) + shadow_offst[0], 1 + shadow_offst[1]))
                Time = fon.render(x, False, (230, 230, 230))
                window.blit(Time, (width - (width//4), 1))
                        #----------------------------------------#
                        #---------------ŚWIAT_-------------------#
                y = f"{str(_+1)} LEVEL"
                shadow_text = fon.render(y, False, shadow_color)
                window.blit(shadow_text, (width - (width//2) + shadow_offst[0], 1 + shadow_offst[1]))
                Time = fon.render(y, False, (230, 230, 230))
                window.blit(Time, (width - (width//2), 1))
                        #----------------------------------------#
                        #---------------LICZNIK COINÓW-----------#
                z = f"COINS\n{coin_counter}"
                shadow_text = fon.render(z, False, shadow_color)
                window.blit(shadow_text, (width - (width//1.4) + shadow_offst[0], 1 + shadow_offst[1]))
                Time = fon.render(z, False, (230, 230, 230))
                window.blit(Time, (width - (width//1.4), 1))
                        #----------------------------------------#
                        #---------------MARIO POINTS-----------#
                ź = f"Mario\n{str(Mario_points).zfill(10)}"
                shadow_text = fon.render(ź, False, shadow_color)
                window.blit(shadow_text, (10 + shadow_offst[0], 1 + shadow_offst[1]))
                Time = fon.render(ź, False, (230, 230, 230))
                window.blit(Time, (10, 1))
                        #--------------------------------------#
                        #---------------ŻYCIA------------------#

                serca = [serce_zlamane] * 3

                for i in range(lifes):
                    serca[i] = serce_OKEJ
                for index, serce in enumerate(serca):
                    window.blit(serce, (10 + index * (serce.get_width() + 10), height - 100))

                        #--------------------------------------#
                    #-------------------------------------#

            #------------------------------------------------------------------------------#

                

            if lifes <= 0:
                run2 = False
                run = False
                boss_sounds.stop()
                mario_sound.stop()
                start_screen(chosen_weapon,slider_value)
            pg.display.update()
            clock.tick(60)

            if mario.invincible_time > 0:
                mario.invincible_time -= 1
            
            #-------------------------ZAPIASYWANIE NAJLEPSZYCH WYNIKÓW----------------------#
            try:
                if coin_counter > best_coins:
                    best_coins = coin_counter
                if Mario_points > best_mario_points:
                    best_mario_points = Mario_points     
            except TypeError:
                best_coins = coin_counter
                best_mario_points = Mario_points
            if not czy_escape:
                write_best_scores(best_time, best_coins, best_mario_points, Best_game, top_level, coin_counter, bronie)
            #------------------------------------------------------------------------------#
        
            if czy_escape:
                run = False
                run2 = False
                boss_sounds.stop()
                mario_sound.stop()
                start_screen(chosen_weapon,slider_value)
        try:
            if (int(czas_poziomu) <= int(Best_game[1]) or int(Best_game[1]) == 0) and coin_counter_poziomu >= int(Best_game[4]) and Mario_points_poziomu >= int(Best_game[7]):
                Best_game = [int(czas_poziomu), coin_counter_poziomu, Mario_points_poziomu, _+1]
            if int(czas_poziomu) < best_time or best_time == 0:
                best_time = int(czas_poziomu)
            if _ + 1 > top_level:
                top_level = _ + 1
        except (ValueError, IndexError):
            best_time = int(czas_poziomu)
            Best_game = [int(czas_poziomu), coin_counter_poziomu, Mario_points_poziomu, _+1]
            top_level = _ + 1
        if not czy_escape:
            write_best_scores(best_time, best_coins, best_mario_points, Best_game, top_level, coin_counter, bronie)

            



    if not run2 and run:
        run = False
        start_screen(chosen_weapon,slider_value)

if __name__ == '__main__':
    Mariusz_sfx.play()
    start_screen(chosen_weapon,0.5)