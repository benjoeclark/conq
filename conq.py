#!/usr/bin/env python

import pygame
import random
import sys
import math

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
FPS = 30

def dist(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

class Player(object):
    def __init__(self, name=None, color=WHITE):
        self.name = name
        self.color = color

class Fleet(object):
    def __init__(self, owner, size, origin, target):
        self.owner = owner
        self.size = size
        self.position = origin.position
        self.target = target
        self.velocity = .2
        self.reached_target = False

    def update(self):
        d = dist(self.position, self.target.position)
        if d <= self.target.radius:
            self.target.invade(self)
            self.reached_target = True
        pos = (self.position[0] + self.velocity * (self.target.position[0] - self.position[0]) / d, 
        self.position[1] + self.velocity * (self.target.position[1] - self.position[1]) / d)
        self.position = pos
        pygame.draw.lines(self.target.screen, WHITE, False, [self.position, self.target.position], 1)
        pygame.draw.circle(self.target.screen, self.owner.color, self.position, self.size, 0)
        

class Planet(object):
    def __init__(self, screen, pos=None, rad=None):
        self.owner = Player()
        self.garrison = 0.
        self.size = random.randint(5, rad/2)
        self.screen = screen
        self.position = pos
        self.radius = rad
        self.rect = pygame.Rect((pos[0] - rad, pos[1] - rad), (2*rad, 2*rad))

    def collision(self, pos, rad, buffer=2):
        if dist(self.position, pos) < buffer + self.radius + rad:
            return True
        return False

    def get_fleet(self, target, percent=1. ):
        fleet_size = percent * self.garrison
        self.garrison -= percent * self.garrison
        return Fleet(self.owner, fleet_size, self, target)

    def invade(self, fleet):
        if self.owner.name is None:
            self.owner = fleet.owner
        elif self.owner == fleet.owner:
            self.garrison += fleet.size
        else:
            if fleet.size > self.garrison:
                self.owner = fleet.owner
                self.garrison = fleet.size - self.garrison
            else:
                self.garrison -= fleet.size
        if self.garrison >= self.radius - self.size - 5:
            self.garrison = self.radius - self.size - 5

    def update(self):
        if self.owner.name is not None:
            if self.garrison < self.radius - self.size - 5:
                self.garrison += self.size / 1000.
            pygame.draw.arc(self.screen, self.owner.color, self.rect,
                            0., 2.*math.pi, int(self.garrison))
        pygame.draw.circle(self.screen, self.owner.color, self.position, self.size, 0)

class Game(object):
    def __init__(self, width=640, height=480, background=BLACK):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.width = width
        self.height = height
        self.background = background
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(self.background)
        pygame.display.update()
        self.done = False
        self.fleets = []
        self.planets = []
        self.generate_planets()
        self.player = Player('me', BLUE)
        self.npc = Player('npc', RED)
        self.planets[0].owner = self.player
        self.planets[1].owner = self.npc
        self.play()

    def generate_planets(self, planet_count=10):
        for count in range(planet_count):
            pos, rad = self.new_position()
            self.planets.append(Planet(self.screen, pos, rad))

    def new_position(self):
        pos = None
        rad = None
        while not self.is_valid_position(pos, rad):
            pos = (random.randint(0, self.width),
                random.randint(0, self.height))
            rad = random.randint(20, 50)
        return pos, rad

    def is_valid_position(self, pos=None, rad=None):
        if pos is None or rad is None:
            return False
        if 0 > pos[0] - rad or \
            0 > pos[1] - rad or \
            self.width < pos[0] + rad or \
            self.height < pos[1] + rad:
            return False
        for planet in self.planets:
            if planet.collision(pos, rad):
                return False
        return True

    def update(self):
        self.screen.fill(BLACK)
        to_remove = []
        for fleet in self.fleets:
            if not fleet.reached_target:
                fleet.update()
            else:
                to_remove.append(fleet)
        for fleet in to_remove:
            self.fleets.remove(fleet)
        for planet in self.planets:
            planet.update()
        pygame.display.update()

    def play(self):
        while not self.done:
            self.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for planet in self.planets[1:]:
                        if planet.collision(event.pos, 0):
                            self.fleets.append(self.planets[0].get_fleet(planet))
            msElapsed = self.clock.tick(FPS)
        

def main():
    game = Game()

if __name__ == '__main__':
    main()
