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
        self.bonded_package_dictionary = dict()
        self.address_package_dictionary = dict()
        self.failed_package_dictionary = dict()
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
                note = note.replace(',', ' ')
                string_list = note.split()
                if current_package.get_id() not in self.bonded_package_dictionary:
                    self.bonded_package_dictionary[current_package.get_id()] = set()
                self.bonded_package_dictionary[current_package.get_id()].add(string_list[4])
                self.bonded_package_dictionary[current_package.get_id()].add(string_list[5])
                for package_id in self.bonded_package_dictionary[current_package.get_id()]:
                    if package_id not in self.bonded_package_dictionary:
                        self.bonded_package_dictionary[package_id] = set()
                    self.bonded_package_dictionary[package_id].add(current_package.get_id())
                    if package_id == string_list[4]:
                        self.bonded_package_dictionary[package_id].add(string_list[5])
                    else:
                        self.bonded_package_dictionary[package_id].add(string_list[4])
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
        self.find_routes(anytime_package_list, Route([Stop(None, 0)]))

    # find a 15 package route for truck
    def find_routes(self, package_list, current_route):

        # find the shortest route for 40 package without check any conditions
        while len(package_list) > 0:
            self.get_shortest_next_stop(current_route, package_list)
        # adding hub stop when all packages are assigned
        self.adding_hub_stop(current_route)
        self.validating_routes(current_route)
        while len(self.failed_package_dictionary) > 0:
            self.fix_fail_stop(current_route)
            self.validating_routes(current_route)
        return current_route

    # calculate loading time for each route
    def validating_routes(self, current_route):
        travel_time_truck_1 = datetime.strptime(str(date.today()) + ' ' + '08:00 AM', '%Y-%m-%d %I:%M %p')
        travel_time_truck_2 = datetime.strptime(str(date.today()) + ' ' + '08:00 AM', '%Y-%m-%d %I:%M %p')
        count = 1
        for route in current_route.get_route_breakdown():
            available_package_list = set()
            # adding all package into set
            for stop in route:
                if stop.address_index == 0:
                    continue
                available_package_list.add(stop.package_id)
            if count % 2 == 1:
                start_time = travel_time_truck_1
            else:
                start_time = travel_time_truck_2
            current_time = start_time
            loading_time = start_time
            previous_address_index = 0
            for stop in route:
                # not to loop up package if current stop is hub
                if stop.address_index != 0:
                    current_package = self.package_hashtable.lookup(stop.package_id)
                    # don't update current time if package is in the same address
                    if stop.address_index != previous_address_index:
                        current_time = current_time + stop.travel_time
                else:
                    current_time = current_time + stop.travel_time
                    continue
                # check loading time for package:
                if current_package.load_time is not None and loading_time < current_package.available_time:
                    self.add_failed_package(stop.package_id, 'package can\'t be loaded')
                # check rush package
                if current_package.deadline < current_time:
                    self.add_failed_package(stop.package_id, 'failed delivery by deadline')
                # check bonding delivery packages
                if current_package.id in self.bonded_package_list:
                    if not self.bonded_package_dictionary[current_package.id].issubset(available_package_list):
                        self.add_failed_package(stop.package_id,
                                                'failed delivery by bonding package')
                # check truck 2 only packages
                if current_package.id in self.truck2_package_list:
                    if count % 2 == 1:
                        self.add_failed_package(stop.package_id,
                                                'failed delivery by truck 2')
                previous_address_index = stop.address_index
            if count % 2 == 1:
                travel_time_truck_1 = current_time
            else:
                travel_time_truck_2 = current_time
            count += 1

    def add_failed_package(self, package_id, reason):
        if package_id not in self.failed_package_dictionary:
            self.failed_package_dictionary[package_id] = []
        self.failed_package_dictionary[package_id].append(reason)

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

    def fix_fail_stop(self, current_route):
        available_package = set()
        truck_1_route_list = []
        truck_2_route_list = []
        count = 1
        for route in current_route.get_route_breakdown():
            if count % 2 == 1:
                truck_1_route_list.append(route)
            else:
                truck_2_route_list.append(route)

        sorted_fail_package = self.get_sorted_fail_package()
        # removing wrong assigning packages from truck 1 route
        for package_id in sorted_fail_package['failed delivery by truck 2']:
            for route in truck_1_route_list:
                for stop
                if stop.package_id is None:
                    continue
                else:
                    if stop.package_id == package_id
                        route.remove(package_id)
                        available_package.add(package_id)
                    break
        for route in truck_2_route_list:
            for package_id in route


    # group failed package by its fail reason
    def get_sorted_fail_package(self):
        sorted_fail_package = dict()
        for key, value in self.failed_package_dictionary.items():
            for reason in value:
                if reason not in sorted_fail_package:
                    sorted_fail_package[reason] = set()
                else:
                    sorted_fail_package[reason].add(key)
        return sorted_fail_package
