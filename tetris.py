import curses
import time
import sys
import copy
import random

def main(stdscr):
    width = 10
    height = 15
    speed = 20 # move down per 'speed' * 0.01 sec
    timer = 0
    shape_i = 0
    score = 0

    # Set the input mode to non-blocking
    stdscr.nodelay(1)

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
    rerender(stdscr, field, score)

    px = py = 0 # current position of the current shape
    while 1:
        if px == 0 and py == 0 and is_collide(field, shapes[shape_i], px, py):
            s = copy.deepcopy(shapes[shape_i])
            while s and is_collide(field, s, px, py):
                s = s[1:]

            lock_shape(field, s, px, py)
            rerender(stdscr, field, score)
            stdscr.addstr(height + 2, 0, 'Game Over')
            break

        if is_collide(field, shapes[shape_i], px, py + 1):
            # lock_shape and init position
            lock_shape(field, shapes[shape_i], px, py)

            # get full rows
            full_rows = get_full_rows(field)

            # replace texture of full rows for UX
            for r in full_rows:
                field[r] = ['*'] * width

            rerender(stdscr, field, score)

            # let the full '*' rows shows for a sec
            time.sleep(0.1)

            # remove full rows
            tmp = []

            # copy all rows except full ones from field to tmp
            for i in range(height - 1, -1, -1):
                if i in full_rows:
                    continue
                tmp.append(field[i])

            # fill the tmp to height
            while len(tmp) < height:
                tmp.append(['.'] * width)

            field = tmp[::-1]

            # add scores
            score += len(full_rows)

            # init position and iterate to the next shape
            px = py = 0
            shape_i = random.randint(0, len(shapes) - 1)

            rerender(stdscr, field, score)

            continue

        time.sleep(0.01)
        timer += 1

        # keyboard event
        key = stdscr.getch()
        if key == curses.KEY_LEFT and not is_collide(field, shapes[shape_i], px - 1, py):
            px -= 1
        elif key == curses.KEY_RIGHT and not is_collide(field, shapes[shape_i], px + 1, py):
            px += 1
        elif key == curses.KEY_DOWN:
            if not is_collide(field, shapes[shape_i], px, py + 1):
                py += 1
            else:
                # lock_shape and init position
                lock_shape(field, shapes[shape_i], px, py)

                # init position and iterate to the next shape
                px = py = 0
                shape_i = random.randint(0, len(shapes) - 1)

        elif key == ord('z'):
            # rotate
            pass
        
        # force go down
        if timer % speed == 0 and py + 1 < height:
            py += 1

        # render out the current shape and field
        buf = copy.deepcopy(field)
        for i in range(len(shapes[shape_i])):
            for j in range(len(shapes[shape_i][0])):
                if i + py < 0 or i + py >= height or j + px < 0 or j + px >= width:
                    # a part of empty shape is outside the field but it's fine
                    # just not copy the cell to the field
                    continue
                buf[i + py][j + px] = 'X' if shapes[shape_i][i][j] == 'X' else buf[i + py][j + px]
        rerender(stdscr, buf, score)

    stdscr.getch() # hit any key to exit the game

def get_full_rows(field):
    rows, cols = len(field), len(field[0])
    res = []

    for r in range(rows):
        if ''.join(field[r]) == 'X' * cols:
            res.append(r)

    return res

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
                if shape[i][j] == 'X':
                    return True
                continue # cell of the shape is outside the field but is empty which is fine
                
            if shape[i][j] == 'X' and field[i + py][j + px] == shape[i][j]:
                return True

    return False

def rerender(stdscr, field: list[list[str]], score):
    """Re-render the field to the console
    
    It will automatically add a width 1 border when rendering
    """
    h, w = len(field), len(field[0])
    stdscr.clear()
    stdscr.addstr('#' * (w + 2) + '   score: ' + str(score))
    for r in range(h):
        stdscr.addstr(r + 1, 0, '#{}#'.format(''.join(field[r])))
    stdscr.addstr(h + 1, 0, '#' * (w + 2))
    stdscr.refresh()

if __name__ == '__main__':
    curses.wrapper(main)
    sys.exit(0)