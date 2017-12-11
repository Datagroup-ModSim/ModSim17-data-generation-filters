import unittest
import numpy

class test_gaussian(unittest.TestCase):

    # load a scenario for testing purposes
    def setUp(self):
        OBSERVATION_AREA = [20, 5, 10, 10]
        TIME_STEP_BOUNDS = (40, 80)
        file = 'postvis.trajectories'
        data_raw = read_trajectory_file(file)
        #  convert to numeric data
        data_numeric = convert_data(data_raw)
        # extract data from a specified observation area
        data_observation = extract_observation_area(data_numeric, OBSERVATION_AREA)
        # sort time steps chronological
        data_chronological = sort_chronological(data_observation)
        # extract observation period
        global data_period
        data_period = extract_period_from_to(data_chronological, TIME_STEP_BOUNDS)

    # density value at given distance are below given tol
    def test_gaussian_pdf(self):
        print(len(data_period))
        pass

    # test of grid
    def test_get_gaussian_grid_size(self):
        start = -2
        stop = 2
        res = 0.1
        sigma = 0.7
        grid_size = get_gaussian_grid(start, stop, res, sigma).size
        self.assertEqual(grid_size, ((stop+res)/res)**2 )

    def test_get_gaussian_grid_tol_at_border(self):
        pass

    # time_step increases monotonious
    def test_calculate_density_timeseries(self):
        pass

    # density of n pedestrians are equal sum(gaussian) * n
    def test_add_pedestrian_density(self):
        pass

if __name__ == '__main__':
    unittest.main()