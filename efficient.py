import random
import os, sys, getopt
from subprocess import call
from time import sleep
from collections import deque


sprites = {1: 'D', 2: 'W', 3: 'T', 4: 'L', 99: '-'}
sprites_decode = {v: k for k,v in sprites.items()}
TRUE_RANDOM = False
FORCED_ANIMAL = False

#getting command line parameters
argv = sys.argv[1:]
opts, args = getopt.getopt(argv, 'ta:')
if len(opts) > 1:
    print('Only one option can be passed')
    sys.exit()
for opt, arg in opts:
    if opt == '-t':
        TRUE_RANDOM = True
    if opt == '-a': 
        if arg not in sprites.values():
            print(f'Animal {arg} does not exist.')
            sys.exit()
        elif arg == '-':
            print(f'Animal {arg} does not exist. Nice try, though.')
            sys.exit()
        FORCED_ANIMAL = sprites_decode[arg]


def clear():  # clears the screen, looks better that way, trust me
    call('clear' if os.name =='posix' else 'cls') 


def get_neighbors(x, y, field):  # gets all the neighboring fields on the board
    re = []
    if x > 0:
        re.append((x - 1, y))
    if x < len(field) - 1:
        re.append((x + 1, y))
    if y > 0:
        re.append((x, y - 1))
    if y < len(field[x]) - 1:
        re.append((x, y + 1))

    return re


def get_edible_neighbors(x, y, field, power):  # checks which of the neighbors can be eaten
    neighbors = get_neighbors(x, y, field)
    return [(nx, ny) for nx, ny in neighbors if power > field[nx][ny]]


def generate_field():
    if TRUE_RANDOM:  # generated by rolling 100d4, guaranteed to be random
        return [[3, 4, 2, 4, 4, 1, 4, 3, 4, 2],
                [1, 1, 4, 1, 3, 2, 4, 1, 3, 4],
                [3, 2, 3, 3, 3, 3, 4, 4, 3, 1],
                [1, 1, 3, 4, 4, 3, 4, 2, 1, 3],
                [1, 3, 2, 1, 2, 3, 4, 2, 3, 3],
                [4, 1, 4, 2, 4, 2, 4, 4, 2, 1],
                [1, 3, 2, 2, 4, 1, 1, 3, 4, 4],
                [2, 2, 2, 3, 4, 3, 1, 2, 2, 1],
                [3, 2, 3, 2, 1, 1, 4, 2, 4, 3],
                [1, 1, 4, 2, 1, 1, 4, 1, 2, 3]]
    return [[random.randint(1, 4) for _ in range(10)] for __ in range(10)]


def print_field(field):
    # this function is not very readable, but it's not strictly part of the assignment
    clear()
    print('  \033[94m', ' '.join([str(x + 1) for x in range(len(field[0]))]))
    for i, row in enumerate(field):
        print('\033[94m{:2d}\033[0m'.format(i + 1), ' '.join([sprites[cell] for cell in row]))


def random_cell(field):
    if TRUE_RANDOM:
        return (6, 4)  # generated by rolling 2d10, guaranteed to be random
    x = random.randint(0, len(field) - 1)
    y = random.randint(0, len(field[x]) - 1)
    
    if FORCED_ANIMAL:  # changes the starting cell to an animal of the users choice. 
        field[x][y] = FORCED_ANIMAL
    return (x, y)


if __name__ == '__main__':
    # initializing the game
    edible_neighbors = deque(maxlen=100)  # a stack of potentially edible neighbors
    field = generate_field()
    cur_y, cur_x = random_cell(field)  # here x and y are not very intuitive

    # printing starting field composition
    print_field(field)
    power = field[cur_y][cur_x]
    print(f'Starting with {[cur_x + 1, cur_y + 1]} ({sprites[field[cur_y][cur_x]]})')
    sleep(1)

    # playing the game
    while True:
        field[cur_y][cur_x] = 99
        print_field(field)
        print(f'Current animal: {sprites[power]}')
        sleep(0.1)
        edible_neighbors.extend(get_edible_neighbors(cur_y, cur_x, field, power))
        if not edible_neighbors:
            break
        cur_y, cur_x = edible_neighbors.pop()
        