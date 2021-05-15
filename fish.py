import math
import random
import pos
import params
import fish_map
import pygame
from copy import deepcopy

import testing

# traits:
#   * search radius
#   * roaming speed
#   * seeking speed
#   * size
class Fish:
    def __init__(self, posX, posY, energy, traits):
        self.pos = pos.Pos(posX, posY)
        self.dir = random.uniform(-math.pi, math.pi)
        self.traits = traits
        # self.set_state('roaming')
        self.state = 'roaming'
        self.speed = self.traits['roaming_speed'] # Old movement method
        self.roaming_rotation_speed = 0.05
        self.seeking_rotation_speed = 2.5 * self.roaming_rotation_speed
        self.eating_speed = 1 * traits['size']
        self.energy_consumption_multiplier = 0.1 * self.traits['size'] # default 1
        self.eat_proximity = 40 * traits['size']
        self.energy = energy
        self.food = None
        self.fitness = 0

        #seek stuff
        self.kp = 10
        self.td = 0.001
        self.last_angle = 0
        self.xvel = 0
        self.yvel = 0
        self.xforce = 0
        self.yforce = 0

        self.timer = random.randint(5, 20)
        self.rotate_amount = 0

        if params.ENABLE_GRAPHICS:
            self.sprite = Fish_Sprite(self.traits['size'])

    def __repr__(self):
        s = "---FISH---\n"
        s += "state = {}\n".format(self.state)
        s += "pos = {:.3f}, {:.3f}\n".format(self.pos.x, self.pos.y)
        s += "traits = {}\n".format("{" + ", ".join(["{}: {}".format(k, str(round(v, 3))) for k, v in self.traits.items()]) + "}")
        s += "----------"
        return s

    def __deepcopy__(self, memo):
        return Fish(self.pos.x, self.pos.y, self.energy, self.traits)

    def set_state(self, new_state):
        if self.state == new_state:
            return
        self.state = new_state
        if new_state == 'roaming':
            self.speed = self.traits['roaming_speed']
        elif new_state == 'seeking':
            self.speed = self.traits['seeking_speed']

    def seek(self, dt):
        old_pos_x = self.pos.x
        old_pos_y = self.pos.y
        # kp * (xref - x) + kt * (vref - v) # currently kp and kt are hardcoded as 40 and 12
        # self.xforce = (40 * (self.food.pos.x - self.pos.x)*dt + 12 * (-self.xvel))/1000
        # self.yforce = (40 * (self.food.pos.y - self.pos.y)*dt + 12 * (-self.yvel))/1000
        self.xforce, self.yforce = tuple([(40*x*dt+12*(-self.xvel))/1000 for x in pos.get_smallest_displacement(self, self.food)]) #(40 * pos.get_smallest_displacement(self, self.food)*dt + 12 * (-self.xvel))/1000)
        # PD controller movement method
        self.pos.x = (self.pos.x + self.xforce * self.traits['seeking_speed']/10 * dt)
        self.pos.y = (self.pos.y + self.yforce * self.traits['seeking_speed']/10 * dt)
        self.xvel = (self.pos.x - old_pos_x)/dt
        self.yvel = (self.pos.y - old_pos_y)/dt
        self.pos.x = self.pos.x % params.MAP_SIZE_X
        self.pos.y = self.pos.y % params.MAP_SIZE_Y

        food_dir, _dist = pos.get_dir_dist(self, self.food)
        angle = math.atan2(math.sin(food_dir - self.dir), math.cos(food_dir - self.dir))
        rotate_amount = self.kp*self.seeking_rotation_speed*(angle + self.td*(angle - self.last_angle)/dt)
        
        #faster_dir = pos.closer_to_zero(food_dir - self.dir, food_dir - self.dir - 2 * math.pi)
        #rotate_amount = math.copysign(self.seeking_rotation_speed * dt, faster_dir)
        # make sure it stays within -pi through pi
        self.dir = ((self.dir + rotate_amount + math.pi) % (2 * math.pi)) - math.pi
        self.energy -= self.traits['seeking_speed'] * self.energy_consumption_multiplier * dt

    def roam(self, dt):
        self.pos.x = (self.pos.x + self.speed * dt * math.cos(self.dir)) % params.MAP_SIZE_X
        self.pos.y = (self.pos.y + self.speed * dt * math.sin(self.dir)) % params.MAP_SIZE_Y

        self.timer -= dt
        if (self.timer <= 0):
            self.rotate_amount = self.roaming_rotation_speed * random.randint(-1, 1)
            self.timer = random.randint(5, 20)
        # make sure it stays within -pi - pi 
        self.dir = ((self.dir + self.rotate_amount + math.pi) % (2 * math.pi)) - math.pi
        self.energy -= self.traits['roaming_speed'] * (self.traits['search_radius'] / 250) * self.energy_consumption_multiplier * dt

    def get_pos(self):
        return (self.pos.x, self.pos.y, self.dir)

    # state priority:
    #   * dead (do nothing)
    #   * eating (eat until food gone)
    #   * seeking (move towards food)
    #   * roaming (roam randomly until food is found)
    def act(self, fish_map, dt):
        if params.ENABLE_GRAPHICS:
            self.sprite.update(self.pos.x, self.pos.y, self.dir)

        # if dead, stay dead
        if self.state == 'dead':
            return
        # if no energy, become dead
        if self.energy <= 1:
            print('I died with {} energy'.format(self.energy))
            self.set_state('dead')
            if params.ENABLE_GRAPHICS:
                self.sprite.make_dead()
                self.sprite.update(self.pos.x, self.pos.y, self.dir)
                
            try:
                fish_map.move_fish(self) # calls move_fish in fish_map to transition this fish from alive to dead
            except:
                print("MOVE_FISH ERROR: fish was not moved to dead_list")
            return

        # increment fitness
        self.fitness += dt

        if self.state == 'eating':
            if self.food.energy <= 0:
                self.set_state('seeking')
            else:
                self.energy += self.eating_speed * dt
                self.food.energy -= self.eating_speed * dt
                return

        if self.state == 'seeking':
            if self.food.energy <= 0:
                self.set_state('roaming')
            else:
                _dir, dist = pos.get_dir_dist(self, self.food)
                if dist <= self.eat_proximity:
                    self.set_state('eating')
                    return
                self.seek(dt)

        if self.state == 'roaming':
            food_found, food = self.search_for_food(fish_map)
            if food_found:
                self.food = food
                self.set_state('seeking')
                return
            self.roam(dt)
            
    # searches for food using the fish_map.MAP and pos.get_dir_dist
    # returns <is food found?>, <food object>
    # food will not be found if outside traits.search_radius
    def search_for_food(self, fish_map):
        food_gen = fish_map.get_food()
        # poopy code
        #_dir, closest_food_dist = pos.get_dir_dist(self, closest_food)
        closest_food, closest_food_dist = None, float("inf")
        for next_food in food_gen:
            _dir, next_food_dist = pos.get_dir_dist(self, next_food)
            if next_food_dist < closest_food_dist:
                closest_food, closest_food_dist = next_food, next_food_dist
        if closest_food_dist <= self.traits['search_radius']:
            return True, closest_food
        else:
            return False, None

def white_to_color(img, input_color):
    for x in range(img.get_width()):
        for y in range(img.get_height()):
            color = img.get_at((x, y))
            if color == (255, 255, 255, 255):
                img.set_at((x, y), input_color)

class Fish_Sprite(pygame.sprite.Sprite):
    def __init__(self, fish_size):
        super(Fish_Sprite, self).__init__()
        # Add fish image to fish
        self.fish_size = fish_size
        self.original_image = pygame.image.load("fish.png")
        self.original_image = pygame.transform.scale(self.original_image, (int(50 * self.fish_size), int(70 * self.fish_size)))
        white_to_color(self.original_image, (round(127*(2-self.fish_size)), 255, 255, 255))
        self.fish_image = self.original_image.copy()
        #self.fish_image = self.fish_image.convert()
        self.rect = self.fish_image.get_rect()

    def update(self, x, y, new_dir):
        self.fish_image = pygame.transform.rotate(self.original_image, -180/math.pi * new_dir - 90)
        self.rect = self.fish_image.get_rect()
        self.rect.center = (x, y)

    def make_dead(self):
        self.original_image = pygame.image.load("dead_fish.png")
        self.original_image = pygame.transform.scale(self.original_image, (int(50 * self.fish_size), int(70 * self.fish_size)))
        self.fish_image = self.original_image.copy()
        #self.fish_image = self.fish_image.convert()
        self.rect = self.fish_image.get_rect()