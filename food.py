import pos
import params
import pygame

class Food:
    def __init__(self, posX, posY, start_energy, energy_variance):
        self._pos = pos.Pos(posX, posY)
        self.start_energy = start_energy
        self._energy = start_energy

        if params.ENABLE_GRAPHICS:
            self.sprite = Food_Sprite(self)

    def __repr__(self):
        s = "-FOOD-\n"
        s += "pos = {:.3f}, {:.3f}\n".format(self.pos.x, self.pos.y)
        s += "energy = {:.3f}\n".format(self.energy)
        s += "-----"
        return s

    @property
    def pos(self):
        return self._pos

    @property
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, value):
        self._energy = value
        
class Food_Sprite(pygame.sprite.Sprite):
    def __init__(self, food):
        super(Food_Sprite, self).__init__()
        self.food = food

    def draw(self, screen, fish_map, food_obj):
        if(self.food.energy <= 0):
            fish_map.food_list.remove(food_obj)

        start_energy = getattr(self.food, "start_energy")
        eat_amount = 1 - self.food.energy / start_energy # closer to 1 the closer to zero energy the fish is
        color = (255 - 255*(1-eat_amount), 255 - 255*eat_amount, 0)
        color = tuple([min(max(x, 0), 255) for x in color])
        pygame.draw.circle(screen, color, (self.food.pos.x, self.food.pos.y), self.food.energy//5)
        