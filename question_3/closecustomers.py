"""Filters a set of customers by distance.

Reads in a list of customers from a JSON file, then determines which of the
customers are located within a predefined range (RANGE_IN_KM) of the Intercom
office.
"""

import collections
import json
import logging
import math
import sys

logging.basicConfig(filename='closecustomers.log', level=logging.DEBUG)

Coordinate = collections.namedtuple('Coordinate', ['latitude', 'longitude'])
Customer = collections.namedtuple('Customer', ['name', 'user_id', 'location'])

EARTH_RADIUS_IN_KM = 6371.0
RANGE_IN_KM = 100.0
DUBLIN_OFFICE = Coordinate(53.3381985, -6.2592576)
INPUT_FILE = 'customers.json'
EXPECTED_KEYS = set(['name', 'user_id', 'latitude', 'longitude'])


def get_file_contents(filename):
    """Reads in the file as a list of strings.

    If the file cannot be read, the program is exited after logging the
    exception.

    Args:
        filename: str.

    Returns:
        A list of all lines of the file.
    """
    try:
        opened_file = open(filename, 'r')
    except IOError:
        logging.exception("Could not open file %s", filename)
        sys.exit(1)
    file_contents = opened_file.readlines()
    opened_file.close()
    return file_contents


def parse_customer_data(all_customers_json):
    """Parses all valid JSON into a list of Customer objects.

    If the data for a customer does not include all the keys in EXPECTED_KEYS,
    that customer is not included in the returned list.

    Args:
        all_customers_json: A list of JSON encoded strings, where each string
        represents a customer.

    Returns:
        A list of customer objects where each customer has a name, a user_id,
        and location of type Coordinate which contains a latitude and longitude,
        both in radians.
    """
    customers = []
    for customer_json in all_customers_json:
        try:
            customer_data = json.loads(customer_json)
        except ValueError as errormsg:
            logging.warning("Error while parsing customer data: %s", errormsg)
            continue

        if not validate_customer(customer_data):
            continue

        location = Coordinate(float(customer_data['latitude']),
                              float(customer_data['longitude']))
        customer = Customer(customer_data['name'],
                            customer_data['user_id'],
                            location)
        customers.append(customer)
    return customers


def validate_customer(customer):
    """Determines if the given customer contains all necessary information and
    valid latitude and longitude values.

    Args:
        customer: A dictionary representing information about a customer.

    Returns:
        True if the customer has all valid information, False if information is
        missing or the Latitude/Longitude values are invalid.
    """
    customer_has_required_keys = all(key in customer for key in EXPECTED_KEYS)
    if not customer_has_required_keys:
        missing_keys = EXPECTED_KEYS - set(customer)
        logging.warning(("Customer missing keys:\n"
                         "    The input string was: %s\n"
                         "    The missing keys were: %s"),
                        str(customer), " ".join(missing_keys))
        return False

    try:
        float(customer['latitude'])
    except ValueError:
        logging.warning("Could not parse latitude: %s.", customer['latitude'])
        return False

    try:
        float(customer['longitude'])
    except ValueError:
        logging.warning("Could not parse longitude: %s.", customer['longitude'])
        return False

    return True


def distance(coord1, coord2):
    """Calcualtes the great-circle distance between the given coordinates.

    Uses the spherical law of cosines to give the distance between two points
    on the surface of a sphere (such as Earth!). Converts the given coordinates
    to degrees.

    See: https://en.wikipedia.org/wiki/Great-circle_distance

    Args:
        coord1: Coordinate. Should be in degrees.
        coord2: Coordinate. Should be in degrees.

    Returns:
        The distance as a float in kilometers.
    """
    # Convert coordinates to radians
    coord1 = Coordinate(math.radians(coord1.latitude),
                        math.radians(coord1.longitude))
    coord2 = Coordinate(math.radians(coord2.latitude),
                        math.radians(coord2.longitude))
    # Calculate distance
    sine_of_latitudes = math.sin(coord1.latitude) * math.sin(coord2.latitude)
    cos_of_latitudes = math.cos(coord1.latitude) * math.cos(coord2.latitude)
    abs_longitude_difference = abs(coord1.longitude - coord2.longitude)
    central_angle = math.acos(sine_of_latitudes
                              + (cos_of_latitudes
                                 * math.cos(abs_longitude_difference)))
    return EARTH_RADIUS_IN_KM * central_angle


def get_customers_in_range(customers):
    """Determines which customers are within RANGE_IN_KM of DUBLIN_OFFICE.

    Args:
        customers: list(Customer).

    Returns:
        A list of customers that are located within the specified range of the
        DUBLIN_OFFICE location.
    """
    customers_in_range = []
    for customer in customers:
        if distance(customer.location, DUBLIN_OFFICE) <= RANGE_IN_KM:
            customers_in_range.append(customer)
    return customers_in_range


def format_customers(customers):
    """ Creates a string containing the user ids and names of given customers.

    The customers are sorted by user id.

    Args:
        customers: list(Customer).

    Returns:
        A formatted string containing the user id and name of all given
        customers, sorted by user id.
    """
    sorted_customers = sorted(customers, key=lambda customer: customer.user_id)
    result = []
    for customer in sorted_customers:
        result.append("{}: {}".format(customer.user_id, customer.name))
    if result:
        return "\n".join(result)
    return "No customers within {} km.".format(RANGE_IN_KM)


def main():
    customer_file_contents = get_file_contents(INPUT_FILE)
    customers = parse_customer_data(customer_file_contents)
    customers_in_range = get_customers_in_range(customers)
    print format_customers(customers_in_range)

if __name__ == "__main__":
    main()
