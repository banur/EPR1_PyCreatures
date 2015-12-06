"""
PyCreatures
blah
"""


class World():

    """ World class """

    __turn = 0
    __world_map = []  # mouse1, None, corn : M.Y
    __world_ref = {}  # (x,y): mouse1, (x,y): corn1
    __scheduled_actions = []
    __empty_symbol = "."
    __rules = {}
    __world_size = [0, 0]

    def __init__(self):
        """ Setup the world. """
        self.__create_world()
        self.__populate_world()
        self.__print_world()
        self.__start_sim()

    def __create_world(self):
        self.__world_size[0] = 20  # int(input("width: "))
        self.__world_size[1] = 10  # int(input("height: "))

    def __start_sim(self):
        while True:
            player_input = input("action: ")
            if player_input.isdigit():
                for i in player_input:
                    self.__compute_life_cycle()
            elif player_input == "insert":
                position = [0, 0]
                # element_input = input("thing ")
                # if element_input == "thing":
                element_input = Thing()
                position[0] = 15  # input("pos_x ")
                position[1] = 0  # input("pos_y ")
                position_t = tuple(position)
                self.insert_new(position_t, element_input)
            else:
                self.__compute_life_cycle()
            self.__populate_world()
            self.__print_world()

    def __compute_life_cycle(self):
        self.__scheduled_actions = []
        for position in self.__world_ref:
            element = self.__world_ref[position]
            pos_x, pos_y = position[0], position[1]  # refine
            self.__scheduled_actions.append(element.perform_action)
        for action in self.__scheduled_actions:
            # check consistency(action)
            action(15, 0)  # (pos_x, pos_y)

    def get_rules(self, position_self, surroundings):
        """ todo """
        self_type = self.__world_ref[position_self]
        for direction in surroundings:
            positions = tuple(position_self + direction)
            try:
                class_type = self.__world_ref[positions].__class__.__name__
            except KeyError:
                pass

    def insert_new(self, position, element):
        self.__world_ref = {position: element}

    def delete(self, position):
        del self.__world_ref[position]

    def get_position(self, position):
        element = None
        try:
            element = self.__world_ref[position]
        except KeyError:
            pass
        return element

    def __populate_world(self):
        self.__world_map = []
        for size_y in range(self.__world_size[1]):
            self.__world_map.append([])
            for size_x in range(self.__world_size[0]):
                self.__world_map[-1] += self.__empty_symbol
        for position in self.__world_ref:
            pos_x = position[0]
            pos_y = position[1]
            symbol = self.__world_ref[position].get_symbol()
            self.__world_map[pos_y][pos_x] = symbol

    def __print_world(self):
        line = ""
        for row in self.__world_map:
            for element in row:
                line += element
            line += "\n"
        print(line, end="")


class Thing():

    """Thing class"""

    __age = 0
    __symbol = "t"
    # right, left, up, down
    __surroundings = [[1, 0], [-1, 0], [0, 1], [-1, 0]]

    def perform_action(self, pos_x, pos_y):
        print("nada")

    def __check_surroundings(self, pos_x, pos_y):
        """ Check for free space. Return as list. """
        free_space = []
        for position in self.__surroundings:
            surrounding_position = [pos_x, pos_y] + position
            # nope
            if World.get_pos(surrounding_position) == self.__empty_smybol:
                free_space = surrounding_position
        return free_space

    def get_symbol(self):
        return self.__symbol


class Plant(Thing):

    """ Plant class """

    __seed_cycle = None
    # __surroundings.extend([2, 0], [-2, 0], [0, 2], [-2, 0])

    def perform_action(self, pos_x, pos_y):
        if self.__age % self.__seed_cycle == 0:
            self.__grow(pos_x, pos_y)

    def __grow(self, pos_x, pos_y):
        area = self.__check_surroundings(pos_x, pos_y)
        if area:
            free_space = self.__world_ref(self) + random.choice(area)
            new_plant = Plant()  # not correct
            self.__insert_new(new_plant, position)


class Creature(Thing):

    """ Creature class """

    __offspring_cycle = None
    __max_starving = None
    __starving = None
    __max_age = None
    __age = None

    def perform_action(self, pos_x, pos_y):
        starving = self.__starving >= self.__max_starving
        dying = self.__age >= self.__max_age
        if dying or starving:
            self.__die(pos_x, pos_y)
        elif self.__age % self.__offspring_cycle == 0:
            self.__grow(pos_x, pos_y)
        else:
            self.__move(pos_x, pos_y)

    def __die(self, pos_x, pos_y):
        pass

    def __grow(self, pos_x, pos_y):
        pass

    def __move(self, pos_x, pos_y):
        pass


class Corn(Plant):

    """ Corn class """

    __seed_cycle = 6
    __symbol = "§"


class Mouse(Creature):

    """ Mouse class """

    __offspring_cycle = 12
    __symbol = "M"

new_sim = World()
