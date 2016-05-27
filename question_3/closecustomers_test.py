import closecustomers
import unittest
import math


class TestCloseCustomers(unittest.TestCase):

    def test_parse_customer_data_with_valid_and_invalid_customers(self):
        valid_input = '{"latitude": "51.92893", "user_id": 1, \
            "name": "Alice Cahill", "longitude": "-10.27699"}'
        customer_data = [valid_input, '']
        expected_location = closecustomers.Coordinate(51.92893, -10.27699)
        expected_output = [closecustomers.Customer('Alice Cahill', 1,
                                                   expected_location)]
        actual_output = closecustomers.parse_customer_data(customer_data)
        self.assertListEqual(expected_output, actual_output)

    def test_parse_customer_data_with_empty_customer_list(self):
        self.assertListEqual([], closecustomers.parse_customer_data([]))

    def test_validate_customer_missing_keys(self):
        input_missing_keys = {'name': 'Hodor'}
        self.assertFalse(closecustomers.validate_customer(input_missing_keys))

    def test_validate_customer_invalid_latitude(self):
        invalid_latitude = {'name': 'Dany Targaryen',
                                    'user_id': 1,
                                    'longitude': 'invalid',
                                    'latitude': 'invalid'}
        self.assertFalse(closecustomers.validate_customer(invalid_latitude))

    def test_validate_customer(self):
        valid_input = {'name': 'Jon Snow',
                               'user_id': 1,
                               'longitude': '53.3498',
                               'latitude': '-6.3'}
        self.assertTrue(closecustomers.validate_customer(valid_input))

    def test_distance(self):
        coord1 = closecustomers.Coordinate(40.7128, -74.0059)
        coord2 = closecustomers.Coordinate(53.3498, -6.2603)
        test_distance = closecustomers.distance(coord1, coord2)
        self.assertEqual(math.ceil(test_distance), 5115)

    def test_get_customers_in_range(self):
        customers = [
                closecustomers.Customer('Handsome Jack', 1,
                    closecustomers.Coordinate(53.3381985, -6.2592576)),
                closecustomers.Customer('Mr. Torgue', 2,
                    closecustomers.Coordinate(37.7749, -122.4194))]
        self.assertListEqual(closecustomers.get_customers_in_range(customers),
                             [customers[0]])

    def test_get_customers_in_range_empty_list(self):
        self.assertListEqual(closecustomers.get_customers_in_range([]), [])

    def test_format_customers(self):
        location = closecustomers.Coordinate(37.7749, -122.4194)
        customers = [closecustomers.Customer('Tyrion Lannister', 1, location),
                     closecustomers.Customer('Arya Stark', 2, location)]
        expected = "1: Tyrion Lannister\n2: Arya Stark"
        self.assertEqual(closecustomers.format_customers(customers), expected)

    def test_format_customers_empty_input(self):
        expected = "No customers within {} km.".format(
                                                    closecustomers.RANGE_IN_KM)
        self.assertEqual(expected, closecustomers.format_customers([]))

if __name__ == "__main__":
    unittest.main()
