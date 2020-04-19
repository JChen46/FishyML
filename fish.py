import math
import random
import pos

#traits:
#   * search radius
#   * roaming speed
#   * seeking speed
#   * fish size
class Fish:
    def __init__(self, energy, traits):
        self.pos = pos.Pos(random.uniform(0, 100), random.uniform(0, 100))
        self.dir = random.uniform(-math.pi, math.pi)
        self.traits = traits
        self.state = 'roaming'
        self.speed = self.traits.roaming_speed
        self.rotation_speed = 0.05
        self.energy = energy
        self.food = None

    def move(self):
        self.pos.x = (self.pos.x + self.speed * math.cos(self.dir)) % 100
        self.pos.y = (self.pos.y + self.speed * math.sin(self.dir)) % 100
        self.dir = (self.dir + math.pi + self.rotation_speed * random.random()) % 2*math.pi - math.pi
        self.energy

    def act(self):
        if self.energy <= 0
        if self.state == 'eating':

        food_found, food_direction = search_for_food(self.traits.search_radius)
        if food_found:
            self.state = 'seeking'
            self.speed = self.traits.seeking_speed
            self.dir = food_direction
        else:
            