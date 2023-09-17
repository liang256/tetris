import curses
import time
import sys
import copy

def main(stdscr):
    width = 20
    height = 20
    speed = 5 # move down per 'speed' * 0.01 sec
    timer = 0
    shape_i = 0

    shapes = [
        [
            '...',
            'XX.',
            'XX.'
        ],
        [
            '...',
            'X..',
            'X..',
            'XX.'
        ],
        [
            '...',
            'X..',
            'XX.',
            '.X.'
        ],
        [
            '...',
            'X..',
            'XX.',
            'X..'
        ],
        [
            'X..',
            'X..',
            'X..',
            'X..'
        ],
    ]

    field = [['.'] * width for _ in range(height)]
    rerender(stdscr, field)

    px = py = 0 # current position of the current shape
    while 1:
        if px == 0 and py == 0 and is_collide(field, shapes[shape_i], px, py):
            s = copy.deepcopy(shapes[shape_i])
            while s and is_collide(field, s, px, py):
                s = s[1:]

            lock_shape(field, s, px, py)
            rerender(stdscr, field)
            stdscr.addstr(height + 2, 0, 'Game Over')
            break

        if is_collide(field, shapes[shape_i], px, py + 1):
            # lock_shape and init position
            lock_shape(field, shapes[shape_i], px, py)

            # init position and iterate to the next shape
            px = py = 0
            shape_i = 0 if shape_i + 1 == len(shapes) else shape_i + 1

            continue

        time.sleep(0.01)
        timer += 1
        
        # force go down
        if timer % speed == 0:
            py += 1

        buf = copy.deepcopy(field)
        for i in range(len(shapes[shape_i])):
            for j in range(len(shapes[shape_i][0])):
                buf[i + py][j + px] = 'X' if shapes[shape_i][i][j] == 'X' else buf[i + py][j + px]
        rerender(stdscr, buf)

    stdscr.getch() # hit any key to exit the game

def lock_shape(field, shape, px, py):
    """Merge shape into the field"""
    for i in range(len(shape)):
        for j in range(len(shape[0])):
            if shape[i][j] != '.':
                field[i + py][j + px] = shape[i][j]

def is_collide(field: list[list[str]], shape: list[list[str]], px: int, py: int) -> bool:
    """Check if the shape in given position is collided to the field"""
    rows, cols = len(field), len(field[0])
    for i in range(len(shape)):
        for j in range(len(shape[0])):
            if i + py < 0 or i + py >= rows or j + px < 0 or j + px >= cols:
                return True
                
            if shape[i][j] == 'X' and field[i + py][j + px] == shape[i][j]:
                return True

    return False

def rerender(stdscr, field: list[list[str]]):
    """Re-render the field to the console
    
    It will automatically add a width 1 border when rendering
    """
    h, w = len(field), len(field[0])
    stdscr.clear()
    stdscr.addstr('#' * (w + 2))
    for r in range(h):
        stdscr.addstr(r + 1, 0, '#{}#'.format(''.join(field[r])))
    stdscr.addstr(h + 1, 0, '#' * (w + 2))
    stdscr.refresh()

if __name__ == '__main__':
    curses.wrapper(main)
    sys.exit(0)