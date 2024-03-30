# create class to hold distance table and address look up list
class DistanceTable:
    def __init__(self, distance_table, address_dictionary: dict[str, int]):
        self.distance_table = distance_table
        self.address_dictionary = address_dictionary

    def get_distance_table(self):
        return self.distance_table

    def get_address_dictionary(self):
        return self.address_dictionary

    # Sort distance table base on distance between point A to B(from near to far).
    def get_min_distance_table(self):
        min_distance_table = list()
        current_address = 0
        while current_address < len(self.distance_table):
            next_address = 0
            min_distance_table.append(list())
            while next_address < len(self.distance_table):
                distance = self.get_distance_between(current_address, next_address)
                # adding the address to empty list
                if len(min_distance_table[current_address]) == 0:
                    min_distance_table[current_address].append((next_address, distance))
                else:
                    is_insert = False
                    index = 0
                    # compare current term to entire list
                    for item in min_distance_table[current_address]:
                        if float(item[1]) > float(distance):
                            min_distance_table[current_address].insert(index, (next_address, distance))
                            is_insert = True
                            break
                        index += 1
                    # adding the address to end of list if it's farthest
                    if not is_insert:
                        min_distance_table[current_address].append((next_address, distance))
                next_address += 1
            current_address += 1
        return min_distance_table

    # get the distance between two address
    def get_distance_between(self, current_address_id, next_address_id):

        try:
            value = self.distance_table[next_address_id][current_address_id]
        except:
            value = self.distance_table[current_address_id][next_address_id]

        return float(value)


