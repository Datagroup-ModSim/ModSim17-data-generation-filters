import unittest

from src.density.gaussian import gaussian_pdf, get_gaussian_grid,\
    add_pedestrian_density, calculate_density_timeseries

class TestGaussian(unittest.TestCase):
    
    def test_always_pass(self):
        self.assertEquals(1, 1)

if __name__ == '__main__':
    unittest.main()
