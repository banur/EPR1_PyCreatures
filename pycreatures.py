""" PyCreatures

TODO:
birth on corn space
check eat next to corn
input: help, quit, insert, ...

"""

from random import choice


class World():

    """  """

    world_map = []
    world_ref = {}
    world_size = []
    empty_symbol = "."
    scheduled_actions = []

    def __init__(self, size_x=79, size_y=29):
        """  """
        input("Change boardsize? ")
        self.world_size = [size_x, size_y]
        self.insert_new((10, 5), Mouse)
        self.insert_new((15, 11), Corn)
        self.insert_new((16, 10), Mouse)
        self.insert_new((10, 7), Corn)
        self.build_world()
        self.start_sim()

    def start_sim(self):
        """  """
        while True:
            input("next..")
            self.compute_life_cycle()
            self.build_world()

    def insert_new(self, position, element):
        """ Insert new object of type 'element' on 'position' to reference. """
        self.world_ref[position] = element()
        self.world_ref[position].world = self

    def delete(self, position):
        """ Delete the object on that position from the reference. """
        try:
            self.world_ref.pop(position)
        except KeyError:
            pass

    def build_world(self):
        """ Build empty world, insert all elements, call print world. """
        self.world_map = []
        for size_y in range(self.world_size[1]):
            self.world_map.append([])
            for size_x in range(self.world_size[0]):
                self.world_map[-1] += self.empty_symbol
        for position in self.world_ref:
            pos_x = position[0]
            pos_y = position[1]
            symbol = self.world_ref[position].get_symbol()
            self.world_map[pos_y][pos_x] = symbol
        self.print_world()

    def fix_pos(self, position):
        """ Make the world round. """
        fixed_x = position[0] % self.world_size[0]
        fixed_y = position[1] % self.world_size[1]
        return (fixed_x, fixed_y)

    def print_world(self):
        """ Output the world to console. """
        line = ""
        for row in self.world_map:
            for element in row:
                line += element
            line += "\n"
        print(line, end="")

    def compute_life_cycle(self):
        """  """
        self.scheduled_actions = []
        for position in self.world_ref:
            element = self.world_ref[position]
            pos_x, pos_y = position[0], position[1]
            self.scheduled_actions.append(element.perform_action(pos_x, pos_y))
        self.run_actions()

    def run_actions(self):
        """ Check consistency and run actions. """
        for action in self.scheduled_actions:
            try:
                if action[0] == "delete":
                    self.delete(self.fix_pos(action[1]))
                elif action[0] == "insert":
                    self.insert_new(self.fix_pos(action[1]), action[2])
                elif action[0] == "move":
                    fixed_pos = ()
                    fixed_pos = self.fix_pos(action[2])
                    self.world_ref[fixed_pos] = self.world_ref.pop(action[1])
            except TypeError:
                pass

    def check_surroundings(self, pos_x, pos_y, surroundings):
        """ Return object type of position, None if empty. """
        objects = [[], {}]
        position = ()
        for direction in surroundings:
            pos_x += direction[0]
            pos_y += direction[1]
            position = self.fix_pos((pos_x, pos_y))
            if position in self.world_ref:
                objects[1][
                    self.world_ref[position].__class__.__name__] = position
            else:
                objects[0].append(direction)
        return objects[0], objects[1]


class Thing():

    """  """
    symbol = "t"
    age = 0
    surroundings = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    empty_surrounding = []
    surrounding_obj = {}
    world = None

    def perform_action(self):
        """  """
        pass

    def get_symbol(self):
        """ Return the objects world representation. """
        return self.symbol

    def get_surroundings(self, pos_x, pos_y):
        """ Fetch surrounding objects. """
        self.empty_surrounding, self.surrounding_obj = \
            self.world.check_surroundings(pos_x, pos_y, self.surroundings)


class Plant(Thing):

    """ Plant class. """
    seed_cycle = None

    def perform_action(self, pos_x, pos_y):
        """ Check action conditions. """
        self.age += 1
        if self.age % self.seed_cycle == 0:
            self.get_surroundings(pos_x, pos_y)
            return self.grow(pos_x, pos_y)

    def grow(self, pos_x, pos_y):
        """ Insert a new object. """
        if self.empty_surrounding:
            direction = choice(self.empty_surrounding)
            new_pos_x = pos_x + direction[0]
            new_pos_y = pos_y + direction[1]
            insert_position = (new_pos_x, new_pos_y)
            return ("insert", insert_position, self.__class__)


class Creature(Thing):

    """ Creature class. """
    offspring_cycle = None
    starving = 0
    max_starving = 0
    max_age = 0
    edible = []

    def perform_action(self, pos_x, pos_y):
        """ Check action conditions. """
        self.age += 1
        self.starving += 1
        starving = self.starving >= self.max_starving
        dying = self.age >= self.max_age
        self.get_surroundings(pos_x, pos_y)
        if dying or starving:
            return self.die(pos_x, pos_y)
        elif self.age % self.offspring_cycle == 0:
            return self.grow(pos_x, pos_y)
        for food in self.edible:
            if food in self.surrounding_obj:
                return self.eat(pos_x, pos_y)
        return self.move(pos_x, pos_y)

    def die(self, pos_x, pos_y):
        """ Delete the object. """
        return ("delete", (pos_x, pos_y))

    def grow(self, pos_x, pos_y):
        """ Insert a new object. """
        if self.empty_surrounding:
            direction = choice(self.empty_surrounding)
            new_pos_x = pos_x + direction[0]
            new_pos_y = pos_y + direction[1]
            insert_position = (new_pos_x, new_pos_y)
            return ("insert", insert_position, self.__class__)

    def eat(self, pos_x, pos_y):
        """ Feast upon food. """
        for food in self.edible:
            food_choice = []
            if food in self.surrounding_obj:
                food_choice.append(self.surrounding_obj[food])
            position = choice(food_choice)
            return("delete", (position[0], position[1]))

    def move(self, pos_x, pos_y):
        """ Relocate the object. """
        if self.empty_surrounding:
            direction = choice(self.empty_surrounding)
            new_pos_x = pos_x + direction[0]
            new_pos_y = pos_y + direction[1]
            new_position = (new_pos_x, new_pos_y)
            return ("move", (pos_x, pos_y), new_position)


class Corn(Plant):

    """  """
    symbol = "§"
    seed_cycle = 6


class Mouse(Creature):

    """  """
    symbol = "M"
    offspring_cycle = 2
    max_starving = 15
    max_age = 5
    edible = ["Corn"]

new_sim = World()
