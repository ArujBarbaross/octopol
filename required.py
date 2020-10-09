import random
import os
from subprocess import call
from time import sleep

# The base Animal class. It holds the tools for animals to interact
class Animal:
    # those parameters are class wide, since there is no difference between specimens
    power = 0
    sprite = ''
    def __init__(self):  # I had a hard time to figure what to use class for..
        self.higlighted = False
        self.alive = True
        self.active = False

    def __str__(self):  # this is purely eye candy
        if not self.alive:
            return '-'

        style = 9
        color = 9
        bg_color = 9

        if self.higlighted:
            bg_color = 2
        if self.active:
            color = 1
            style = 1
        
        return f'\x1b[{style};3{color};4{bg_color}m{self.sprite}\x1b[0m'

    def can_eat(self, other):
        other.higlighted = True
        return self.power > other.power and other.alive

    def eat(self, other):
        # there is no need for this check in this code, but we are writing a class, so...
        if self.can_eat(other):  
            other.alive = False  # so much tragedy in such a simple code
            return True  # the return values aren't used as well
        return False

# As I've said, I'm not sure why classes are needed,
# but that's my best idea to use them in a not completely ricidulus way
class Lion(Animal):
    power = 4
    sprite = 'L'

class Tiger(Animal):
    power = 3
    sprite = 'T'

class Wolf(Animal):
    power = 2
    sprite = 'W'
    
class Donkey(Animal):
    power = 1
    sprite = 'D'

# This class keeps the game state. Strictly speaking, there is no need for a class here, since
# it's the only instance
class Board:
    animals = [Donkey, Wolf, Tiger, Lion]
    def __init__(self):
        self.rows = 10
        self.columns = 10
        self.board = [[self.animals[random.randint(0, 3)]()
                       for _ in range(self.columns)]
                       for __ in range(self.rows)] 
        self.active_coord = random.randint(0, self.columns - 1), random.randint(0, self.rows - 1)
        self.get_cell(self.active_coord).active = True

    def get_cell(self, coords):
        x,y = coords
        return self.board[y][x]

    def active_neighbors(self):
        re = []
        x, y = self.active_coord
        if x > 0:
            re.append((x - 1, y))
        if x < self.columns - 1:
            re.append((x + 1, y))
        if y > 0:
            re.append((x, y - 1))
        if y < self.rows - 1:
            re.append((x, y + 1))

        return re

    @property
    def active_animal(self):
        if self.active_coord:
            return self.get_cell(self.active_coord)
        return None

    # most of this method is eye candy, :shrug:
    def print_board(self, msg=''):
        re = '\033[94m   ' 
        re += ' '.join([str(i+1) for i in range(self.columns)])
        re += '\n\033[0m'
        for i, row in enumerate(self.board):
            row_number = '\033[94m{:2d}\033[0m'.format(i + 1)
            re += row_number
            for cell in row:
                re += ' ' + str(cell)
            re += '\n'
        re += f'\nCurrently active: {self.active_animal}\n'
        re += msg

        # reprint the screen in one go
        call('clear' if os.name =='posix' else 'cls') 
        print(re)

    # recursion here was added by force, strictly speaking - using it whith a global state is... strange
    def expand(self, coords):
        target = self.get_cell(coords)
        can_expand = self.active_animal.can_eat(target)
        if target.alive:  # this part is just for drawing
            sleep(0.1)
            self.print_board(f'The {self.active_animal} tries to eat {target}')
        
        if can_expand:  # what to do if we can expand
            self.active_animal.eat(target)  # first, eat the target
            self.board[coords[1]][coords[0]] = self.active_animal  # second, take it's place
            self.board[self.active_coord[1]][self.active_coord[0]] = target  # third, put his corpse in yours
            self.active_coord = coords  # update board state
            for n in self.active_neighbors():  # try eating your new neighbords
                self.expand(n)  # recursion, wooo hooo
        else: 
            target.higlighted = False  # if we can't eat it, no reason to highlight it.


if __name__ == '__main__':
    board = Board()
    board.print_board()
    for n in board.active_neighbors():
        board.expand(n)
