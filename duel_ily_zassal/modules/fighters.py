import pygame as pg
import os
from modules import final


class Pushkin():
    def __init__(self, scr, screensize):
        '''Pushkin object class
        
        Parametrs:
        **scr** - game screen
        **screensize** - game screen
        '''
        self.scr = scr
        self.screensize = screensize
        self.hp = 60
        self.lose = final.Lose(self.scr, self.screensize)

    def mouse_gun(self):
        '''Function visualizing Pushkin's gun.
        '''
        gun_surf = pg.image.load(os.path.join("Images", "gun.png"))
        gun_rect = gun_surf.get_rect()
        pg.mouse.set_cursor(*pg.cursors.diamond)
        gun_surf = pg.transform.scale(gun_surf, (2*gun_rect[2], 2*gun_rect[3]))
        self.scr.blit(gun_surf, (self.screensize[0]/2 - gun_rect[2], self.screensize[1] - 2*gun_rect[3]))


class Dantes(pg.sprite.Sprite):

    def __init__(self, scr, scr_size, filename):
        '''Dantes object class
        
        Parametrs:
        **scr** - game screen.
        **scr_size** - game screen size.
        **filename** - Dantes image file name.
        '''
        pg.sprite.Sprite.__init__(self)
        self.filename = filename
        self.hp = 100
        self.image = pg.image.load(os.path.join("Images", self.filename))
        self.coords = [int(self.image.get_rect()[0]+scr_size[0]/2), int(self.image.get_rect()[1]+4*scr_size[1]/7)]        
        self.rect = self.coords
        self.mask = pg.mask.from_surface(self.image)
        self.win = final.Win(scr, scr_size)
        self.step = 1

        
    def check_dantes_hp(self, scr, screensize):
        '''Function that checks Dantes health points and redraw his image based on it.
        **scr** - game screen
        **screensize** - game screen size.        
        '''

        if self.hp <=100 and self.hp > 60:
            self.image = pg.image.load(os.path.join("Images", self.filename))

        if self.hp <= 60 and self.hp > 0:
            self.image = pg.image.load(os.path.join("Images", 'dantes_damage1.png'))                   

        if self.hp <= 20 and self.hp > 0:
            self.image = pg.image.load(os.path.join("Images", 'dantes_damage2.png'))

        if self.hp <= 0:
            self.image = pg.image.load(os.path.join("Images", 'dantes_damage2.png'))
            
    def move(self):
        '''Function that move Dantes.
        '''
        if self.step == 1:
            self.coords[0] -= 2
        if self.coords[0] <= 500 and self.step == 1:
            self.step = 2     
        if self.step == 2:
            self.coords[0] += 2
        if self.coords[0] >= 700 and self.step == 2:
            self.step = 1
            self.rect = self.coords         


if __name__ == "__main__":
    print("This module is not for direct call!")
