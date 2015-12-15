""" PyCreatures

TODO:
help text

"""

from random import choice, randint
from os import system


class World():

    """ Hold the dictionary of all objects and provide control functions. """

    world_map = []
    world_ref = {}
    world_size = []
    empty_symbol = "."
    scheduled_actions = []
# TODO help text
    help_text = "TODO"

    def __init__(self):
        """  """
        size_x, size_y = self.prompt_startup()
        self.world_size = [size_x, size_y]
        self.build_world()
        self.start_sim()

    def prompt_startup(self):
        system("cls")
        change = "Change boardsize from standard {0}x{1}? [y/n] "
        size_x = 79
        size_y = 29
        change = input(change.format(size_x, size_y))
        if change == "y":
            size_x = input("new x: ")
            while not size_x.isdigit():
                size_x = input("invalid number, retry: ")
            size_y = input("new y: ")
            while not size_y.isdigit():
                size_y = input("invalid number, retry: ")
            size_x = int(size_x)
            size_y = int(size_y)
        return size_x, size_y

    def start_sim(self):
        """  """
        while True:
            self.prompt_turn()

    def help(self):
        """ Print game commands. """
        system("cls")
        input(self.help_text)
        self.build_world()

    def quit(self):
        """ Clear screen and exit. """
        system("cls")
        exit()

    def prompt_turn(self):
        player_input = []
        prompt_text = "Type commands, q to quit or h for help: "
        player_input += input(prompt_text).lower().split()
        possible_commands = [{"spawn": self.insert_new,
                              "kill": self.delete,
                              "clear": "",
                              "check": self.check_surroundings},
                             {"help": self.help, "h": self.help,
                              "quit": self.quit, "q": self.quit}]
        possible_objects = {"thing": Thing, "mouse": Mouse, "corn": Corn}
        if not player_input == []:
            if player_input[0].isdigit():
                self.compute_life_cycle(int(player_input[0]))
            elif player_input[0] in possible_commands[1]:
                command = possible_commands[1][player_input[0]]
                command()
            elif player_input[0] in possible_commands[0]:
                if player_input[0] == "spawn":
                    try:
                        command = possible_commands[0][player_input[0]]
                        condition = (player_input[2] in possible_objects) and (
                            player_input[1].isdigit())
                        if condition:
                            position = None
                            try:
                                position = (
                                    int(player_input[3]), int(player_input[4]))
                            except:
                                pass
                            command(possible_objects[player_input[2]],
                                    position,
                                    int(player_input[1]))
                        self.build_world()
                    except:
                        print("Usage: spawn <n> <obj> [<x pos> <y pos>]")
                elif player_input[0] == "kill":
                    try:
                        command = possible_commands[0][player_input[0]]
                        command((int(player_input[1]), int(player_input[2])))
                        self.build_world()
                    except:
                        print("Usage: kill <x pos> <y pos>")
                elif player_input[0] == "clear":
                    self.world_ref = {}
                elif player_input[0] == "check":
                    try:
                        command = possible_commands[0][player_input[0]]
                        objects = command(
                            int(player_input[1]), int(player_input[2]),
                            [[int(player_input[3]), int(player_input[4])]])
                        self.build_world()
                        print("Milestone I", objects)
                    except:
                        print("Usage: check <x pos> <y pos> <x direction>",
                              "<y direction>")
        else:
            self.compute_life_cycle()

    def insert_new(self, element, position=None, repeat=1):
        """ Insert new object of type 'element' on 'position' to world_ref. """
        world = self.world_size[0] * self.world_size[1]
        if repeat > world - len(self.world_ref) + 1:
            repeat = world - len(self.world_ref)
        for _ in range(repeat):
            new_position = position
            if new_position is None:
                free_position = False
                while not free_position:
                    pos_x = randint(0, self.world_size[0] - 1)
                    pos_y = randint(0, self.world_size[1] - 1)
                    new_position = (pos_x, pos_y)
                    if new_position not in self.world_ref:
                        free_position = True
            self.world_ref[new_position] = element()
            self.world_ref[new_position].world = self

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
        system("cls")
        line = ""
        for row in self.world_map:
            for element in row:
                line += element
            line += "\n"
        print(line, end="")

    def compute_life_cycle(self, repeat=1):
        """ First fetch all actions, then execute them. """
        for _ in range(repeat):
            self.scheduled_actions = []
            for position in self.world_ref:
                element = self.world_ref[position]
                pos_x, pos_y = position[0], position[1]
                self.scheduled_actions.append(
                    element.perform_action(pos_x, pos_y))
            self.run_actions()

    def run_actions(self):
        """ Check consistency and run actions. """
        while None in self.scheduled_actions:
            self.scheduled_actions.remove(None)
        for action in self.scheduled_actions:
            try:
                if action[0] == "delete":
                    self.delete(self.fix_pos(action[1]))
                    if len(action) > 2:
                        fixed_pos = ()
                        fixed_pos = self.fix_pos(action[1])
                        self.world_ref[
                            fixed_pos] = self.world_ref.pop(action[2])
                elif action[0] == "insert" and action[2] is Corn:
                    self.insert_new(action[2], self.fix_pos(action[1]))
                elif action[0] == "move":
                    fixed_pos = ()
                    fixed_pos = self.fix_pos(action[2])
                    self.world_ref[fixed_pos] = self.world_ref.pop(action[1])
            except TypeError:
                pass
        for action in self.scheduled_actions:
            if action[0] == "insert":
                if action[2] is Mouse:
                    self.insert_new(action[2], self.fix_pos(action[1]))
        self.build_world()

    def check_surroundings(self, pos_x, pos_y, surroundings):
        """ Return object type of position, None if empty. """
        objects = [[], {}]
        position = ()
        for direction in surroundings:
            changed_pos_x = pos_x + direction[0]
            changed_pos_y = pos_y + direction[1]
            position = self.fix_pos((changed_pos_x, changed_pos_y))
            if position in self.world_ref:
                objects[1][self.world_ref[position]] = position
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

    def perform_action(self, pos_x, pos_y):
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
        """ Insert a new object of the same type. """
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
            for food_object in self.surrounding_obj:
                if food == food_object.__class__.__name__:
                    self.starving = 0
                    return self.eat(pos_x, pos_y)
        return self.move(pos_x, pos_y)

    def die(self, pos_x, pos_y,):
        """ Delete the object. """
        return ("delete", (pos_x, pos_y))

    def grow(self, pos_x, pos_y):
        """ Insert a new object of the same type. """
        insert_position = False
        for food in self.edible:
            if food in self.surrounding_obj:
                self.empty_surrounding.append(
                    [self.surrounding_obj[food][0] - pos_x,
                     self.surrounding_obj[food][0] - pos_y])
        if self.empty_surrounding:
            direction = choice(self.empty_surrounding)
            new_pos_x = pos_x + direction[0]
            new_pos_y = pos_y + direction[1]
            insert_position = (new_pos_x, new_pos_y)
        if insert_position:
            return ("insert", insert_position, self.__class__)

    def eat(self, pos_x, pos_y):
        """ Feast upon food. """
        food_choice = []
        for food in self.edible:
            for food_object in self.surrounding_obj:
                if food == food_object.__class__.__name__:
                    food_choice.append(self.surrounding_obj[food_object])
        position = choice(food_choice)
        return("delete", (position[0], position[1]), (pos_x, pos_y))

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
    offspring_cycle = 12
    max_starving = 7
    max_age = 25
    edible = ["Corn"]

new_sim = World()
