#! /usr/bin/env python

import curses
import random


def main():
    scr, dims = init_curses()
    field = init_field(dims)
    mainloop(scr, field, dims)
    curses.endwin()


def mainloop(scr, field, dims):
    cursor = [0, 0]
    while True:
        scr.clear()
        print_field(scr, field, dims)
        scr.move(cursor[0], cursor[1])
        scr.refresh()
        i = user_input(scr)
        if i == 'move up':
            if cursor[0]:
                cursor[0] -= 1
        elif i == 'move down':
            if cursor[0] < dims[0]-1:
                cursor[0] += 1
        elif i == 'move right':
            if cursor[1] < dims[1]-1:
                cursor[1] += 1
        elif i == 'move left':
            if cursor[1]:
                cursor[1] -= 1
        elif i == 'set':
            if field[cursor[0]][cursor[1]]:
                field[cursor[0]][cursor[1]] = 0
            else:
                field[cursor[0]][cursor[1]] = 1
        elif i == 'random':
            field = random_field(field, dims)
        elif i == 'clear':
            field = init_field(dims)
        elif i == 'start':
            field = game_loop(scr, field, dims)
        elif i == 'quit':
            return field
    
    
def init_curses():
    scr = curses.initscr()
    curses.noecho()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
    dims = scr.getmaxyx()
    return [scr, dims]


def init_field(dims):
    field = []
    for y in xrange(0, dims[0]):
        row = []
        for x in xrange(0, dims[1]):
            row.append(0)
        field.append(row)
    return field


def game_loop(scr, field, dims):
    try:
        while True:
            scr.clear()
            field = update_field(field, dims)
            print_field(scr, field, dims)
            scr.move(dims[0]-1, dims[1]-1)
            scr.refresh()
    except KeyboardInterrupt:
        return field


def print_field(scr, field, dims):
    for y in xrange(0, dims[0]):
        for x in xrange(0, dims[1]):
            if field[y][x]:
                try:
                    scr.addstr(y, x, ' ', curses.color_pair(1))
                except curses.error:
                    pass


def random_field(field, dims):
    for y in xrange(0, dims[0]):
        for x in xrange(0, dims[1]):
            field[y][x] = random.randint(0, 1)
    return field


def update_field(field, dims):
    new_field = init_field(dims)
    for y in xrange(0, dims[0]):
        for x in xrange(0, dims[1]):
            neighbours = get_neighbours(field, dims, y, x)
            if not field[y][x]:
                if neighbours == 3:
                    new_field[y][x] = 1
            else:
                if neighbours in [2, 3]:
                    new_field[y][x] = 1
    return new_field


def get_neighbours(field, dims, y, x):
    num = 0
    if y:
        num += field[y-1][x]
    if x:
        num += field[y][x-1]
    if y and x:
        num += field[y-1][x-1]
    if y < dims[0] - 2:
        num += field[y+1][x]
    if x < dims[1] - 2:
        num += field[y][x+1]
    if y < dims[0] - 2 and x < dims[1] - 2:
        num += field[y+1][x+1]
    if y and x < dims[1] - 2:
        num += field[y-1][x+1]
    if y < dims[0] - 2 and x:
        num += field[y+1][x-1]
    return num


def user_input(scr):
    i = scr.getch()
    if i == 27:
        s1 = scr.getch()
        s2 = scr.getch()
        if s1 == 91:
            if s2 == 65:
                return 'move up'
            elif s2 == 66:
                return 'move down'
            elif s2 == 67:
                return 'move right'
            elif s2 == 68:
                return 'move left'
    elif i == ord('s'):
        return 'set'
    elif i == ord('r'):
        return 'random'
    elif i == ord('c'):
        return 'clear'
    elif i == ord(' '):
        return 'start'
    elif i == ord('q'):
        return 'quit'
    return None

if __name__ == '__main__':
    main()
