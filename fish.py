import math
import random
import pos
import params
import fish_map
import pygame

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
        self.speed = self.traits['roaming_speed']
        self.rotation_speed = 0.05
        self.eating_speed = 1
        self.energy_consumption = 1
        self.eat_proximity = 10
        self.energy = energy
        self.food = None
        self.fitness = 0

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

    def set_state(self, new_state):
        if self.state == new_state:
            return
        self.state = new_state
        if new_state == 'roaming':
            self.speed = self.traits['roaming_speed']
        elif new_state == 'seeking':
            self.speed = self.traits['seeking_speed']

    def seek(self, dt):
        self.pos.x = (self.pos.x + self.speed * dt * math.cos(self.dir)) % params.MAP_SIZE_X
        self.pos.y = (self.pos.y + self.speed * dt * math.sin(self.dir)) % params.MAP_SIZE_Y
        food_dir, _dist = pos.get_dir_dist(self, self.food)
        faster_dir = pos.closer_to_zero(food_dir - self.dir, food_dir - self.dir - 2 * math.pi)
        rotate_amount = math.copysign(self.rotation_speed * dt, faster_dir)
        # make sure it stays within -pi through pi
        self.dir = ((self.dir + rotate_amount + math.pi) % (2 * math.pi)) - math.pi
        self.energy -= self.energy_consumption * self.traits['size'] * dt

    def roam(self, dt):
        self.pos.x = (self.pos.x + self.speed * dt * math.cos(self.dir)) % params.MAP_SIZE_X
        self.pos.y = (self.pos.y + self.speed * dt * math.sin(self.dir)) % params.MAP_SIZE_Y

        self.timer -= dt
        if (self.timer <= 0):
            self.rotate_amount = self.rotation_speed * random.randint(-1, 1)
            self.timer = random.randint(5, 20)
        # make sure it stays within -pi - pi 
        self.dir = ((self.dir + self.rotate_amount + math.pi) % (2 * math.pi)) - math.pi
        self.energy -= self.energy_consumption * self.traits['size'] * dt

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
        if self.energy <= 0:
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
                self.food.energy -= self.eating_speed
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
                _dir, dist = pos.get_dir_dist(self, food)
                if dist <= self.traits['search_radius']:
                    self.food = food
                    self.set_state('seeking')
                    return
            self.roam(dt)
            
    # searches for food using the fish_map.MAP and pos.get_dir_dist
    # returns <is food found?>, <food object>
    # food will not be found if outside traits.search_radius
    def search_for_food(self, fish_map):
        #food_gen = fish_map.get_food()
        return False, None

        # poopy code
        #  _dir, closest_food_dist = pos.get_dir_dist(self, closest_food)
        # for next_food in food_gen:
        #     _dir, next_food_dist = pos.get_dir_dist(self, next_food)
        #     if next_food_dist < closest_food_dist:
        #         closest_food, closest_food_dist = next_food, next_food_dist
        # if closest_food_dist <= self.traits['search_radius']:
        #     return True, closest_food
        # else:
        #     return False, None

class Fish_Sprite(pygame.sprite.Sprite):
    def __init__(self, fish_size):
        super(Fish_Sprite, self).__init__()
        # Add fish image to fish
        self.fish_size = fish_size
        self.original_image = pygame.image.load("fish.png")
        self.original_image = pygame.transform.scale(self.original_image, (int(50 * self.fish_size), int(70 * self.fish_size)))
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