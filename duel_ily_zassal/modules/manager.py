from modules import gui, charges, fields, menu
import pygame as pg
import easygui

SCREEN_SIZE = (800, 600)
class Manager():

    def __init__(self, screen):
        self.screen = screen
        self.done = False
        self.game = False
        self.charges = []
        self.field = fields.Field((10, 10, 10), (10, 10, 10))
        self.quit_button = gui.Button('quit', (350, 275), self.screen, (100, 50), (375, 285))
        self.fire_button = gui.Button('fire', (500, 500), self.screen, (100, 50), (525, 510))
        self.menu = menu.Menu(self.screen, SCREEN_SIZE)
    def process(self, events):
        if self.game is not True:
            self.menu.set_menu(self.screen, SCREEN_SIZE)
        if self.game == True:
            self.fire_b()
        self.field.calculate_force(self.charges)
        for charge in self.charges:
            charge.create()
            charge.move(0.01)

        done = self.event_handler(events)

        return done

    def event_handler(self, events):
        done = False
        for event in events:
            if event.type == pg.QUIT:
                done = True
            if self.menu.quit_button.activated:
                self.menu.quit_button.click(events, self.quit_b)
                done = self.done
            if self.menu.play_button.activated:
                self.menu.play_button.click(events, self.fire_b)
            if self.fire_button.activated:
                self.fire_button.click(events, self.add_charge)
        return done

    def quit_b(self):
        self.done = True

    def fire_b(self):
        self.fire_button.create()
        self.fire_button.active()
        self.game = True

    def add_charge(self):
        self.charges.append(charges.Charge(1, 1, self.screen, (200, 10, 200), (255, 255, 255)))

if __name__ == "__main__":
    print("This module is not for direct call!")

