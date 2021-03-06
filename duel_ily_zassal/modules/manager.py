'''
The brain of project. Handle all events
'''
from modules import gui, charges, fields, menu, background, pause, fighters, final, guide
import pygame as pg

RED = (255, 0, 0)
GREEN = (158, 209, 48)


class Manager():

    def __init__(self, screen, screensize):
        '''

        Args:
            screen: screen to show objects
            screensize: width and high of the screen
        '''
        self.screen = screen
        self.screensize = screensize
        self.done = False
        self.game = False
        self.pause = False
        self.guide_crutch = False
        self.t_reload = 60
        self.attempts = 3
        self.group1 = pg.sprite.Group()
        self.group2 = pg.sprite.Group()
        self.pause_window = pause.Pause(self.screen, self.screensize)
        self.charges = []
        self.d_charges = []
        self.field = fields.Field((0, 0, 0), (0, 0, 0))
        self.quit_button = gui.Button('quit', (350, 275), self.screen, (100, 50), (375, 285))
        self.menu = menu.Menu(self.screen, self.screensize)
        self.back = background.Background(self.screen, self.screensize)
        self.guide = guide.Guide(self.screen, self.screensize)
        self.dantes = fighters.Dantes(self.screen, self.screensize, 'dantes.png')
        self.group2.add(self.dantes)
        self.pushkin = fighters.Pushkin(screen, screensize)
        self.p_hp = gui.Progress_bar((int(screensize[0]/70), 40), (int(screensize[0]/2.5), 20),
                                   self.pushkin.hp, screen, "Pushkin", GREEN)
        self.d_hp = gui.Progress_bar((int(screensize[0]/1.7), 40), (int(screensize[0]/2.5), 20),
                                   self.dantes.hp, screen, "Dantes", RED)
        self.win = final.Win(self.screen, self.screensize)
        self.loose = final.Lose(self.screen, self.screensize)
        self.field.field_type = True

    def process(self, events):
        '''
        Create objects handle their interactions
        Args:
            events: pg.events

        Returns:
            True if game was finished
        '''

        if self.pause:
            self.pause_window.set_pause(self.screen, self.screensize)
            
        if not self.game:
            self.menu.set_menu(self.screen, self.screensize)

        if self.guide_crutch:
            self.guide.set_guide_window()
        
        if self.pause == False and self.game == True:

            if self.dantes.hp > 0 and self.pushkin.hp > 0:

                self.back.set_background()
                self.d_hp.draw()
                self.p_hp.draw()
                self.group2.draw(self.screen)
                self.group1.draw(self.screen)
                self.group2.update(self.pushkin)
                self.pushkin.mouse_gun()
                self.dantes.check_dantes_hp(self.screen, self.screensize)
                self.field.change_field()
                self.field.calculate_force(self.charges)
                self.d_hp.level = self.dantes.hp
                self.p_hp.level = self.pushkin.hp
                self.field.draw(self.screen, self.screensize)
                
                f = pg.font.SysFont('garamondполужирный', 36)
                text = f.render(str(self.attempts) + '/3', 0, (255, 0, 0))
                self.screen.blit(text, (577, 30))

                if self.attempts == 0:
                    f = pg.font.SysFont('garamondполужирный', 26)
                    text = f.render("Relouding...", 0, (255, 0, 0))
                    self.screen.blit(text, (self.screensize[0]/2.2, self.screensize[1]/1.4))
                    if self.t_reload > 0:
                        self.t_reload -= 1
                    if self.t_reload == 0:
                        self.attempts = 3

                if self.dantes.hp > 0:
                    self.dantes.move()

                for charge in self.charges:
                    charge.move(0.01)
                
                if len(self.d_charges) == 0 and self.dantes.hp > 0:

                    self.d_charges.append(charges.D_charge(0, 1, self.screen, (255, 255, 255), self.screensize, self.dantes.coords))
                    self.group2.add(self.d_charges[-1])

                for i, charge in enumerate(self.charges):
                    if charge.size < 5 and not self.pause:
                        self.charges.remove(charge)
                        self.group1.remove(charge)
                    if charge.coord.z > charge.ground:
                        self.charges.remove(charge)
                        self.group1.remove(charge)
                    if charge.coord.y <= 5:
                        self.charges.remove(charge)
                        self.group1.remove(charge)
                    if charge.disappear():
                        self.charges.remove(charge)
                        self.group1.remove(charge)
                    dead = charge.update(self.dantes, self.group2)
                    if dead[0]:
                        for d in dead[1]:
                            self.d_charges.remove(d)
                            self.group2.remove(d)
                        self.charges.remove(charge)
                        self.group1.remove(charge)

                for d_charge in self.d_charges:
                    if d_charge.coord.y <= 5:
                        self.d_charges.remove(d_charge)
                        self.group2.remove(d_charge)
                    d_charge.move(0.01)

            else:
                if self.pushkin.hp <= 0:
                    self.loose.duel_loser(self.screen, self.screensize)
                else:
                    self.win.duel_winner(self.screen, self.screensize)

        done = self.event_handler(events)

        return done

    def event_handler(self, events):
        '''
        Control all events
        Args:
            events: pg.events

        Returns:
            True if game was finished
        '''
        done = False
        for event in events:

            if event.type == pg.QUIT:
                done = True

            if self.menu.guide_button.activated and not self.game:
                self.menu.guide_button.click(events, self.open_help)

            if self.guide.back_button.activated and not self.game:
                self.guide.back_button.click(events, self.close_help)

            if self.loose.restart_button.activated and self.pushkin.hp <= 0:
                self.loose.restart_button.click(events, self.restart)

            if self.win.restart_button.activated and self.dantes.hp <=0:
                self.win.restart_button.click(events, self.restart)

            if self.menu.quit_button.activated and not self.game:
                self.menu.quit_button.click(events, self.quit_b)
                done = self.done

            if self.loose.quit_button.activated and self.pushkin.hp <= 0:
                self.loose.quit_button.click(events, self.quit_b)
                done = self.done

            if self.win.quit_button.activated and self.dantes.hp <=0:
                self.win.quit_button.click(events, self.quit_b)
                done = self.done

            if self.pause_window.quit_button.activated and self.pause:
                self.pause_window.quit_button.click(events, self.quit_b)
                done = self.done

            if not self.pause and self.game:

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.pause_g()
                    elif event.key == pg.K_RIGHT:
                        self.field.change = True
                        self.field.dir = 'r'
                    elif event.key == pg.K_LEFT:
                        self.field.change = True
                        self.field.dir = 'l'
                    elif event.key == pg.K_UP:
                        self.field.change = True
                        self.field.dir = 'u'
                    elif event.key == pg.K_DOWN:
                        self.field.change = True
                        self.field.dir = 'd'
                if event.type == pg.KEYUP:
                    if event.key == pg.K_f:
                        self.field.field_type = not self.field.field_type
                    if event.key == pg.K_RIGHT:
                        self.field.change = False
                        self.field.E.x = 0
                        self.field.B.y = 0
                    elif event.key == pg.K_LEFT:
                        self.field.change = False
                        self.field.E.x = 0
                        self.field.B.y = 0
                    elif event.key == pg.K_UP:
                        self.field.change = False
                        self.field.E.z = 0
                        self.field.B.z = 0
                    elif event.key == pg.K_DOWN:
                        self.field.change = False
                        self.field.E.z = 0
                        self.field.B.z = 0

                if self.attempts > 0:
                    self.t_reload = 60
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            pos = (self.screensize[0] / 2, 425)
                            self.add_charge(pos)
                            self.attempts -= 1

            if self.pause_window.continue_button.activated and self.pause:
                for charge in self.charges:
                    charge.became()
                self.pause_window.continue_button.click(events, self.resume)
                
            if self.menu.play_button.activated and not self.game:
                self.menu.play_button.click(events, self.play)
                   
        return done

    def quit_b(self):
        '''
        Click of quit button
        Returns:
            None
        '''
        self.done = True

    def play(self):
        '''
        Star of game
        Returns:
            None
        '''
        self.game = True

    def pause_g(self):
        '''
        Put game on pause
        Returns:
            None
        '''
        for charge in self.charges:
            charge.hide()
        self.pause = True

    def resume(self):
        '''
        Resume game
        Returns:
            None
        '''
        self.pause = False

    def add_charge(self, pos):
        '''
        Create a charge with needed properties
        Args:
            pos: position x and z of a charge

        Returns:
            None

        '''
        self.charges.append(charges.Charge(0, 10, self.screen, (pos[0], 5, pos[1]), (255, 255, 255), self.screensize))
        self.group1.add(self.charges[-1])

    def restart(self):
        '''
        Restart the game. Put all variables on their initial values
        Returns:
            None
        '''
        self.game = False
        self.pushkin.hp = 60
        self.dantes.hp = 100
        self.charges = []
        self.d_charges = []
        self.group1 = []
        self.group2 = []
        self.group1 = pg.sprite.Group()
        self.group2 = pg.sprite.Group()
        self.group2.add(self.dantes)
        self.attempts = 3
        self.field.field_type = True

    def open_help(self):
        '''
        Open help on help button click
        Returns:
            None
        '''
        self.guide_crutch = True

    def close_help(self):
        '''
        CLose help on back button click
        Returns:
            None
        '''
        self.guide_crutch = False


if __name__ == "__main__":
    print("This module is not for direct call!")
