import math
import random
import pos
import params
import fish_map

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
        self.rotation_speed = 0.05
        self.eating_speed = 1
        self.energy_consumption = 1
        self.eat_proximity = 10
        self.energy = energy
        self.food = None
        

    def set_state(self, new_state):
        if self.state == new_state:
            return
        self.state = new_state
        if new_state == 'roaming':
            self.speed = self.traits.roaming_speed
        elif new_state == 'seeking':
            self.speed = self.traits.seeking_speed

    def seek(self):
        self.pos.x = (self.pos.x + self.speed * math.cos(self.dir)) % fish_map.MAP.size_x
        self.pos.y = (self.pos.y + self.speed * math.sin(self.dir)) % fish_map.MAP.size_y
        food_dir, _dist = pos.get_dir_dist(self, self.food)
        faster_dir = pos.closer_to_zero(food_dir - self.dir, food_dir - self.dir - 2 * math.pi)
        rotate_amount = math.copysign(self.rotation_speed, faster_dir)
        # make sure it stays within -pi through pi
        self.dir = ((self.dir + rotate_amount + math.pi) % (2 * math.pi)) - math.pi
        self.energy -= self.energy_consumption * self.traits.size

    def roam(self):
        self.pos.x = (self.pos.x + self.speed * math.cos(self.dir)) % fish_map.MAP.size_x
        self.pos.y = (self.pos.y + self.speed * math.sin(self.dir)) % fish_map.MAP.size_y
        rotate_amount = self.rotation_speed * random.random()
        # make sure it stays within -pi - pi
        self.dir = ((self.dir + rotate_amount + math.pi) % (2 * math.pi)) - math.pi
        self.energy -= self.energy_consumption * self.traits.size

    def get_pos(self):
        return (self.pos.x, self.pos.y, self.dir)

    # state priority:
    #   * dead (do nothing)
    #   * eating (eat until food gone)
    #   * seeking (move towards food)
    #   * roaming (roam randomly until food is found)
    def act(self):
        # if dead, stay dead
        if self.state == 'dead':
            return
        # if no energy, become dead
        if self.energy <= 0:
            self.set_state('dead')
            return

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
                self.seek()

        if self.state == 'roaming':
            food_found, food = self.search_for_food()
            if food_found:
                _dir, dist = pos.get_dir_dist(self, food)
                if dist <= self.traits.search_radius:
                    self.food = food
                    self.set_state('seeking')
                    return
            self.roam()
            
    # searches for food using the fish_map.MAP and pos.get_dir_dist
    # returns <is food found?>, <food object>
    # food will not be found if outside traits.search_radius
    def search_for_food(self):
        food_gen = fish_map.MAP.get_food()
        closest_food = next(food_gen)
        _dir, closest_food_dist = pos.get_dir_dist(self, closest_food)
        for next_food in food_gen:
            _dir, next_food_dist = pos.get_dir_dist(self, next_food)
            if next_food_dist < closest_food_dist:
                closest_food, closest_food_dist = next_food, next_food_dist
        if closest_food_dist <= self.traits.search_radius:
            return True, closest_food
        else:
            return False, None