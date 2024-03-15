from PackageHashTable import *
from Truck import *
from DistanceTable import *
from datetime import *
from Stop import *
from Route import *


class RouteCalculator:
    def __init__(self, distance_table: DistanceTable, package_hashtable: PackageHashTable, truck_list):
        self.distance_dictionary = distance_table.get_address_dictionary()
        self.distance_table = distance_table.get_distance_table()
        self.min_distance_table = distance_table.get_min_distance_table()
        self.package_hashtable = package_hashtable
        self.truck_list = truck_list
        self.truck2_package_list = set()
        self.task_list = [[0], [0]]
        self.all_possible_routes = []
        self.bonded_package_dictionary = dict()
        self.address_package_dictionary = dict()
        self.package_failed_index = dict()
        self.bonded_package_list = set()
        self.rush_package_list = set()
        self.delay_package_list = set()
        self.early_deadline = datetime.strptime(str(date.today()) + ' ' + '10:30 AM', '%Y-%m-%d %I:%M %p')

    # update the package on package_hashtable base on their special notes
    def check_special_notes(self):
        special_notes_list = self.package_hashtable.get_special_notes_list()
        for special_request_package in special_notes_list:
            current_package = self.package_hashtable.lookup(special_request_package)
            note = current_package.get_notes()
            # load package to truck 2
            if note == 'Can only be on truck 2':
                self.truck2_package_list.add(current_package.get_id())
            # set available time and load_time to 9:05 am
            elif note == 'Delayed on flight---will not arrive to depot until 9:05 am':
                current_package.set_available_time(
                    datetime.strptime(str(date.today()) + ' ' + '09:05 AM', '%Y-%m-%d %I:%M %p'))
                current_package.load_time = datetime.strptime(str(date.today()) + ' ' + '09:05 AM', '%Y-%m-%d %I:%M %p')
                self.package_hashtable.insert(current_package.get_id(), current_package)
            # set address for package 9 to correct address and update the available time
            elif note == 'Wrong address listed':
                current_package.set_available_time(
                    datetime.strptime(str(date.today()) + ' ' + '10:20 AM', '%Y-%m-%d %I:%M %p'))
                current_package.set_address('410 S STATE ST')
                self.package_hashtable.insert(current_package.get_id(), current_package)
            elif 'Must be delivered with' in note:
                note.replace(',', ' ')
                string_list = note.split()
                self.bonded_package_dictionary[current_package.get_id()] = []
                self.bonded_package_dictionary[current_package.get_id()].append(string_list[4])
                self.bonded_package_dictionary[current_package.get_id()].append(string_list[5])
                # adding all three packages into set
                self.bonded_package_list.add(current_package.get_id())
                self.bonded_package_list.add(string_list[4])
                self.bonded_package_list.add(string_list[5])

    def calculate_routes(self):
        anytime_package_list = set()
        start_time = datetime.strptime(str(date.today()) + ' ' + '08:00 AM', '%Y-%m-%d %I:%M %p')
        end_of_day = datetime.strptime(str(date.today()) + ' ' + '11:59 PM', '%Y-%m-%d %I:%M %p')
        self.check_special_notes()
        # load packages in package hashtable into a list
        for bucket in self.package_hashtable.table:
            for package in bucket:
                # adding all packages into anytime_package_list
                anytime_package_list.add(package[1].get_id())
                # adding rush package into rush_package_list
                if package[1].deadline < end_of_day:
                    self.rush_package_list.add(package[1].get_id())
                # putting same address packages together
                if self.address_package_dictionary.get(self.distance_dictionary[package[1].address]) is None:
                    # creating new list entry if there is no existing address
                    self.address_package_dictionary[self.distance_dictionary[package[1].address]] = set()
                    self.address_package_dictionary[self.distance_dictionary[package[1].address]].add(
                        package[1].get_id())
                else:
                    self.address_package_dictionary.get(self.distance_dictionary[package[1].address]).add(
                        package[1].get_id())
        # finding all delivery routes
        current_route = self.find_routes(anytime_package_list, Route([Stop(None, 0)]), 1, start_time, start_time)
        # planning the best route for rush package
        return

    # find a 15 package route for truck
    def find_routes(self, package_list, current_route, route_count: int, current_time_truck_1,
                    current_time_truck_2):

        # find the shortest route for 40 package without check any conditions
        while len(package_list) > 0:
            self.get_shortest_next_stop(current_route, package_list)
        # adding hub stop when all packages are assigned
        self.adding_hub_stop(current_route)
        is_validated = False

        return current_route

    # find the distance between two address
    def check_rush_package(self, current_route):

        is_found = False
        for package_id in self.rush_package_list:
            for stop in current_route.route:
                if stop.package_id == package_id:
                    is_found = True
            if not is_found:
                return False
            is_found = False
        return True

    def adding_hub_stop(self, current_route):
        current_stop = current_route.route[-1]
        next_stop = Stop(None, 0)
        next_stop.travel_time = timedelta(
            hours=self.get_distance_between(next_stop.address_index, current_stop.address_index) / 18)
        current_route.route.append(next_stop)
        current_route.last_hub_index.append(len(current_route.route))

    def get_shortest_next_stop(self, current_route, package_list):
        # check if there is 16 packages assigned to the route and adding hub stop
        if len(current_route.route) - current_route.last_hub_index[-1] == 16:
            self.adding_hub_stop(current_route)
        else:
            current_stop = current_route.route[-1]
            current_address_index = current_stop.address_index
            current_address_distance_detail = self.min_distance_table[current_address_index]
            is_add = False
            for item in current_address_distance_detail:
                address_index = item[0]
                distance = item[1]
                # skip if the address_index are point to hub or itself
                if address_index == 0 or address_index == current_address_index:
                    continue
                num_same_address_package = len(self.address_package_dictionary[address_index])
                # check the address_package_dictionary to see if there is any package with that address
                # and find the packages are available in package_list
                available_packages = self.address_package_dictionary[address_index].intersection(package_list)
                if len(available_packages) > 0:
                    # check if there is enough to add all package to current route.
                    if len(available_packages) - current_route.last_hub_index[-1] + len(
                            current_route.route) < 17 and len(
                        available_packages) < 17:
                        # adding all same address package to current route
                        for package_id in available_packages:
                            next_stop = Stop(package_id, address_index)
                            next_stop.travel_time = timedelta(
                                hours=distance / 18)
                            current_route.route.append(next_stop)
                            package_list.remove(package_id)
                            is_add = True
                        if is_add:
                            break
            # adding hub stop to route in case remaining spot for package is not enough for all available packages
            if not is_add:
                self.adding_hub_stop(current_route)

    def get_distance_between(self, current_address_id, next_address_id):

        try:
            value = self.distance_table[next_address_id][current_address_id]
        except:
            value = self.distance_table[current_address_id][next_address_id]

        return float(value)
