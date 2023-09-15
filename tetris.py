import curses
import time
import sys
import copy

def main(stdscr):
    width = 20
    height = 20
    speed = 20 # move down per 'speed' * 0.01 sec
    timer = 0

    field = [['.'] * width for _ in range(height)]
    rerender(stdscr, field)

    shape = [
        'XXX',
        'XXX',
        'XXX'
    ]

    px = py = 0 # current position of the current shape
    while 1:
        if is_collide(field, shape, px, py + 1):
            # lock_shape and init position
            lock_shape(field, shape, px, py)
            px = py = 0

            if is_collide(field, shape, px, py):
                lock_shape(field, shape, px, py)
                rerender(stdscr, field)
                stdscr.addstr(height + 2, 0, 'Game Over')
                break

            continue

        time.sleep(0.01)
        timer += 1
        
        # force go down
        if timer % speed == 0:
            py += 1

        buf = copy.deepcopy(field)
        for i in range(len(shape)):
            for j in range(len(shape[0])):
                buf[i + py][j + px] = 'X' if shape[i][j] == 'X' else buf[i + py][j + px]
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
                
            if field[i + py][j + px] == shape[i][j]:
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