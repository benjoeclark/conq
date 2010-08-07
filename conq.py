#!/usr/bin/env python

import pygame
import random
import sys
import math

BLACK = (0, 0, 0)
ATMOSPHERE = (30, 30, 30)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
FPS = 30

def dist(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def angle(pos1, pos2):
    return math.atan2(pos2[1] - pos1[1], pos2[0] - pos1[0])

class Player(object):
    def __init__(self, name=None, color=WHITE, reaction=150):
        self.name = name
        self.color = color
        self.planets = []
        self.reaction = reaction
        self.reaction_count = 0
        self.dead = False

    def check_pulse(self, game):
        if len(self.planets) == 0:
            self.dead = True
            for fleet in game.fleets:
                if fleet.owner == self:
                    self.dead = False

    def update(self, game):
        self.check_pulse(game)
        if self.dead:
            return []
        self.reaction_count += 1
        if self.reaction_count >= self.reaction and len(self.planets) > 0:
            self.reaction_count = 0
            largest_source = self.planets[0]
            for planet in self.planets[1:]:
                if planet.garrison > largest_source.garrison:
                    largest_source = planet
            other_planets = []
            for planet in game.planets:
                if planet not in self.planets:
                    other_planets.append(planet)
            if len(other_planets) == 0:
                return []
            closest_target = other_planets[0]
            closest_dist = dist(largest_source.position, closest_target.position)
            for planet in other_planets[1:]:
                d = dist(planet.position, largest_source.position)
                if closest_dist > d:
                    closest_target = planet
                    closest_dist = d
            return [largest_source.get_fleet(closest_target, 0.5)]
        return []
        

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
        int_pos = (int(self.position[0]), int(self.position[1]))
        pygame.draw.circle(self.target.screen, self.owner.color, int_pos, int(self.size), 0)
        

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

    def get_fleet_percent_by_angle(self, pos):
        selected_angle = angle(self.position, pos)
        if selected_angle < 0.:
            selected_angle += 2. * math.pi
        return selected_angle / (2. * math.pi)

    def get_fleet_percent(self, pos):
        selected_dist = dist(self.position, pos)
        if selected_dist < 1:
            selected_dist = 1
        return selected_dist / self.radius

    def invade(self, fleet):
        if self.owner.name is None:
            self.owner = fleet.owner
            self.owner.planets.append(self)
            self.garrison += fleet.size
        elif self.owner == fleet.owner:
            self.garrison += fleet.size
        else:
            if fleet.size > self.garrison:
                self.owner.planets.remove(self)
                self.owner = fleet.owner
                self.owner.planets.append(self)
                self.garrison = fleet.size - self.garrison
            else:
                self.garrison -= fleet.size
        if self.garrison >= self.radius - self.size - 5:
            self.garrison = self.radius - self.size - 5

    def update(self):
        pygame.draw.circle(self.screen, ATMOSPHERE, self.position, self.radius, 0)
        if self.owner.name is not None:
            if self.garrison < self.radius - self.size - 5:
                self.garrison += self.size / 1000.
                if self.garrison < 0:
                    self.garrison = 0
            pygame.draw.arc(self.screen, self.owner.color, self.rect,
                            0., 2.*math.pi, int(self.garrison))
        pygame.draw.circle(self.screen, self.owner.color, self.position, self.size, 0)

class Game(object):
    def __init__(self, width=800, height=600, background=BLACK):
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
        self.award_planet(self.planets[0], self.player)
        self.npcs = []
        self.npcs.append(Player('npc', RED, 150))
        self.award_planet(self.planets[1], self.npcs[-1])
        self.npcs.append(Player('npc', GREEN, 100))
        self.award_planet(self.planets[2], self.npcs[-1])
        self.npcs.append(Player('npc', PURPLE, 450))
        self.award_planet(self.planets[3], self.npcs[-1])
        self.npcs.append(Player('npc', YELLOW, 100))
        self.award_planet(self.planets[4], self.npcs[-1])
        self.fleet_percent = 0.
        self.fleet_source = None
        self.play()

    def award_planet(self, planet, player):
        previous_owner = planet.owner
        planet.owner = player
        player.planets.append(planet)
        if previous_owner.name is not None:
            previous_owner.planets.remove(planet)

    def generate_planets(self, planet_count=20):
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
        self.player.check_pulse(self)
        if self.player.dead:
            print 'game over, you lose'
            self.done = True
            return
        all_dead = True
        for npc in self.npcs:
            if not npc.dead:
                all_dead = False
                self.fleets.extend(npc.update(self))
        if all_dead:
            print 'game over, you win'
            self.done = True
            return
        self.screen.fill(BLACK)
        for planet in self.planets:
            planet.update()
        to_remove = []
        for fleet in self.fleets:
            if not fleet.reached_target:
                fleet.update()
            else:
                to_remove.append(fleet)
        for fleet in to_remove:
            self.fleets.remove(fleet)
        pygame.display.update()

    def play(self):
        while not self.done:
            self.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for planet in self.planets:
                        if planet.collision(event.pos, 0):
                            if planet.owner == self.player:
                                self.fleet_percent = planet.get_fleet_percent(event.pos)
                                self.fleet_source = planet
                elif event.type == pygame.MOUSEBUTTONUP:
                    for planet in self.planets:
                        if planet.collision(event.pos, 0):
                            if self.fleet_percent > 0.:
                                if self.fleet_source != planet:
                                    self.fleets.append(self.fleet_source.get_fleet(planet, self.fleet_percent))
                    self.fleet_percent = 0.
                    self.fleet_source = None
            msElapsed = self.clock.tick(FPS)
        

def main():
    game = Game()

if __name__ == '__main__':
    main()
