# create class to hold distance table and address look up list
class DistanceTable:
    def __init__(self, distance_table, address_dictionary: dict[str, int]):
        self.distance_table = distance_table
        self.address_dictionary = address_dictionary

    def get_distance_table(self):
        return self.distance_table

    def get_address_dictionary(self):
        return self.address_dictionary
