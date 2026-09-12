import unittest

from pipal.gaze import choose_face, normalized_center, smooth


class GazeTests(unittest.TestCase):
    def test_center_and_orientation(self):
        self.assertEqual(normalized_center((140, 100, 40, 40), 320, 240), (0, 0))
        left = normalized_center((0, 0, 40, 40), 320, 240)
        mirrored = normalized_center((0, 0, 40, 40), 320, 240, True)
        self.assertLess(left[0], 0)
        self.assertLess(left[1], 0)
        self.assertEqual(mirrored, (-left[0], left[1]))

    def test_clamps_outside_frame(self):
        self.assertEqual(normalized_center((-1000, 1000, 20, 20), 320, 240), (-1, 1))

    def test_smoothing_is_frame_rate_independent(self):
        single = smooth((0, 0), (1, -1), 1)
        repeated = (0, 0)
        for _ in range(30):
            repeated = smooth(repeated, (1, -1), 1 / 30)
        self.assertAlmostEqual(single[0], repeated[0])
        self.assertAlmostEqual(single[1], repeated[1])
        self.assertTrue(0 < single[0] < 1)

    def test_selection_keeps_nearby_face(self):
        small = (10, 10, 30, 30)
        large = (180, 100, 80, 80)
        self.assertEqual(choose_face([small, large]), large)
        self.assertEqual(choose_face([small, large], (12, 10, 30, 30)), small)
        self.assertIsNone(choose_face([]))


if __name__ == '__main__':
    unittest.main()
