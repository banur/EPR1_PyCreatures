"""
PyCreatures
blah
"""


class World():

    """ World class """

    __turn = 0
    __empty_symbol = "."

    def __init__(self):
        """ Setup the world. """
        __world_map = []  # mouse1, None, corn : M.Y
        __world_ref = {}  # mouse1: x/y, corn1: x/y
        __scheduled_actions = []

    def __compute_life_cycle(self):
        for element in self.__world_ref:
            self.__scheduled_actions = element.perform_action()
        for action in self.__scheduled_actions:
            action


class Thing():

    """Thing class"""

    __age = 0
    __surroundings = [[1, 0], [-1, 0], [0, 1], [-1, 0]]

    def __perform_action(self):
        pass

    def __check_surroundings(self):
        free_space = []
        for position in self.__surroundings:
            surrounding_position = self.__world_ref{self.__name__} + position
            if surrounding_position == empty_smybol:
                free_space = surrounding_position
        return free_space

    def __insert_new(self, element, position):
        self.__world_ref.extend{element, position}


class Plant(Thing):

    """ Plant class """

    __seed_cycle = None

    def __perform_action(self):
        if self.__age % self.__seed_cycle = 0:
            self.__grow()

    def __grow(self):
        area = self.__check_surroundings()
        if area:
            free_space = self.__world_ref(self) + random.choice(area)
            new_thing = Thing()  # not correct
            self.__insert_new(new_thing, position)


class Creature(Thing):

    """ Creature class """

    __offspring_cycle = None

    def __perform_action(self):
        if self.__age >= self.__max_age:
            self.__die()
        elif self.__age % self.__offspring_cycle == 0:
            self.__grow()
        move()


class Corn(Plant):

    """ Corn class """

    self.__seed_cycle = 6


class Mouse(Creature):

    """ Mouse class """

    self.__offspring_cycle = 12
