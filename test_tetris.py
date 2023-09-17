import unittest
import tetris


class TestTetris(unittest.TestCase):

    def test_is_collide(self):
        shape = [
            'XXX',
            'XXX',
            'XXX'
        ]
        field = [
            '...',
            '...',
            '...',
            '...',
        ]
        self.assertEqual(tetris.is_collide(field, shape, 0, 0), False)

        shape = [
            'XXX',
            'XXX',
            'XXX'
        ]
        field = [
            '...',
            '...',
            '.X.',
            '...',
        ]
        self.assertEqual(tetris.is_collide(field, shape, 0, 0), True)

        shape = [
            'XXX',
            'XXX',
            'XXX'
        ]
        field = [
            '...',
            '...',
            '...',
            '...',
        ]
        self.assertEqual(tetris.is_collide(field, shape, 2, 0), True)

        shape = [
            '.X.',
            '.X.',
            '.X.',
            '.X.',
        ]
        field = [
            '...',
            'XXX',
            '...',
            '...',
        ]
        self.assertEqual(tetris.is_collide(field, shape, 0, 0), True)

        shape = [
            'X..',
            'X..',
            'X..',
            'XXX'
        ]
        field = [
            '.....',
            '.....',
            '.....',
            '.....',
            '.....',
            '.....'
        ]
        self.assertEqual(tetris.is_collide(field, shape, 0, 0), False)

        shape = [
            'X..',
            'X..',
            'X..',
        ]
        field = [
            '..',
            '..',
            '..'
        ]
        self.assertEqual(tetris.is_collide(field, shape, 0, 0), False)

    def test_lock_shape(self):
        shape = [
            '.XX',
            'X.X',
            'XXX'
        ]
        field = [
            list('A..'),
            list('A..'),
            list('A..'),
            list('A..'),
        ]
        expected = [
            list('AXX'),
            list('X.X'),
            list('XXX'),
            list('A..')
        ]
        tetris.lock_shape(field, shape, 0, 0)
        self.assertEqual(field, expected)

    def test_get_full_rows(self):
        filed = [
            list('XXX'),
            list('X..'),
            list('XXX'),
            list('...')
        ]
        self.assertEqual(tetris.get_full_rows(filed), [0, 2])

    def test_rotate_90_clockwise(self):
        m = [
            [1,1,1],
            [0,1,0]
        ]
        expected = [
            [0,1],
            [1,1],
            [0,1]
        ]
        self.assertEqual(tetris.rotate_90_clockwise(m), expected)

if __name__ == '__main__':
    unittest.main()