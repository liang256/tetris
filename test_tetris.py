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

if __name__ == '__main__':
    unittest.main()