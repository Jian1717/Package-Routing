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
        self.updated_min_distance_table = dict()
        self.best_route_dictionary = dict()
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
                self.delay_package_list.add(current_package.get_id())
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
        # find the shortest route between two point with multiple stop in consideration instead of direct travel
        self.get_shortest_route_dictionary()
        # assign delay package to truck 2
        truck_2_package = self.delay_package_list
        # assign truck 2 only package to truck 2
        truck_2_package = truck_2_package.union(self.truck2_package_list)
        # assign same address to truck base on exiting package assignment
        truck_2_package = self.add_same_address_package(truck_2_package)
        # assign rush package that are required to be delivery with other packages to truck 1
        truck_1_package = self.rush_package_list.intersection(self.bonded_package_list)
        # find its bonded package and assign them to truck 1
        for package_id in truck_1_package:
            if package_id in self.bonded_package_dictionary:
                truck_1_package = truck_1_package.union(self.bonded_package_dictionary[package_id])
        truck_1_package = truck_1_package.union(self.delay_package_list)
        address_for_truck_1 = self.find_address_index_by_package_id(truck_1_package)
        truck_1_package = self.add_same_address_package(truck_1_package)
        best_route_for_truck_1 = self.get_least_distance_travel_between_stops(address_for_truck_1, ([0], 0), ([0], 140))
        '''
        truck_1_package = self.add_same_address_package(truck_1_package)
        package_list.difference_update(truck_1_package)
        package_list.difference_update(truck_2_package)
        left_over_rush_package = package_list.intersection(self.rush_package_list)
        package_list.difference_update(left_over_rush_package)
        address_for_truck_1 = self.find_address_index_by_package_id(truck_1_package)
        address_for_truck_2 = self.find_address_index_by_package_id(truck_2_package)
        best_test = self.get_least_distance_travel_between_stops(
            {3, 15, 24, 20, 21, 6, 4, 17, 26, 22, 3, 10, 23, 13, 7}, ([0], 0), ([0], 140))
        best_route_for_truck_1 = self.get_least_distance_travel_between_stops(address_for_truck_1, ([0], 0), ([0], 140))
        best_route_for_truck_2 = self.get_least_distance_travel_between_stops(address_for_truck_2, ([0], 0), ([0], 140))
        truck_1_package = self.assign_package(best_route_for_truck_1, package_list_2)
        package_list_2.difference_update(truck_1_package)
        truck_2_package = self.assign_package(best_route_for_truck_2, package_list_2)
        package_list_2.difference_update(truck_2_package)
        best_route_for_left_over_package = self.get_least_distance_travel_between_stops(
            self.find_address_index_by_package_id(package_list_2), ([0], 0), ([0], 140))
        truck_left_over_package = self.assign_package(best_route_for_left_over_package, package_list_2)
        '''
        # set default value
        global best_distance_travel
        best_distance_travel = 140
        best_optimal_route = ([], set(), set(), 140)
        address_needs_to_travel = set()
        count = 1
        while len(address_needs_to_travel) < 27:
            address_needs_to_travel.add(count)
            count += 1

    def assign_package(self, address_list, package_list):
        package_assigned = set()
        for address_index in address_list[0]:
            if address_index == 0:
                continue
            for package_id in self.address_package_dictionary[address_index]:
                if package_id in package_list:
                    package_assigned.add(package_id)
        return package_assigned

    def get_least_distance_travel_between_stops(self, address_needs_visit, current_route_detail, best_route_detail):
        start_point = current_route_detail[0][-1]
        # exit condition
        # if all address are visited.  Check the total distance traveled
        if len(address_needs_visit) == 0:
            next_route_detail = self.best_route_dictionary[start_point][0]
            if current_route_detail[1] + next_route_detail[1] > best_route_detail[1]:
                return best_route_detail
            else:
                new_route = current_route_detail[0].copy()
                if start_point == 0:
                    best_route_detail = (new_route, current_route_detail[1])
                else:
                    new_route.extend(next_route_detail[0][1:])
                    best_route_detail = (new_route, current_route_detail[1] + next_route_detail[1])
                return best_route_detail

        for address_index in address_needs_visit:
            next_route_detail = self.best_route_dictionary[start_point][address_index]
            if current_route_detail[1] + next_route_detail[1] > best_route_detail[1]:
                return best_route_detail
            else:
                new_address_needs_visit = address_needs_visit.copy()
                new_route = current_route_detail[0].copy()
                new_route.extend(next_route_detail[0][1:])
                new_current_route_detail = (new_route, current_route_detail[1] + next_route_detail[1])
                new_address_needs_visit.remove(address_index)
                best_route_detail = self.get_least_distance_travel_between_stops(new_address_needs_visit,
                                                                                 new_current_route_detail,
                                                                                 best_route_detail)

        return best_route_detail

    # check route assignment for the truck
    def check_route(self, truck, travel_time):
        start_time = travel_time
        truck.calculate_package_list()
        available_package_list = truck.package_list
        loading_time = start_time
        previous_address_index = 0
        current_time = start_time
        for i, stop in enumerate(truck.route.route):
            # not to loop up package if current stop is hub
            if stop.address_index != 0:
                current_package = self.package_hashtable.lookup(stop.package_id)
                # don't update current time if package is in the same address
                if stop.address_index != previous_address_index:
                    current_time = current_time + stop.travel_time
            else:
                if i == 0:
                    continue
                self.calculate_travel_time(stop, truck.route.route[i - 1])
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
            if truck.id == 1:
                if current_package.id in self.truck2_package_list:
                    self.add_failed_package(stop.package_id,
                                            'failed delivery by truck 2')
                previous_address_index = stop.address_index
            start_time = current_time

    def add_failed_package(self, package_id, reason):
        if package_id not in self.failed_package_dictionary:
            self.failed_package_dictionary[package_id] = []
        self.failed_package_dictionary[package_id].append(reason)

    def calculate_travel_time(self, current_stop, next_stop):
        next_stop.distance = self.get_distance_between(next_stop.address_index, current_stop.address_index)
        next_stop.travel_time = timedelta(
            hours=next_stop.distance / 18)

    def get_distance_between(self, current_address_id, next_address_id):

        try:
            value = self.distance_table[next_address_id][current_address_id]
        except:
            value = self.distance_table[current_address_id][next_address_id]

        return float(value)

    # group failed package by its fail reason
    def get_sorted_fail_package(self):
        sorted_fail_package = dict()
        for key, value in self.failed_package_dictionary.items():
            for reason in value:
                if reason not in sorted_fail_package:
                    sorted_fail_package[reason] = set()
                    sorted_fail_package[reason].add(key)
                else:
                    sorted_fail_package[reason].add(key)
        return sorted_fail_package

    # get best route get from any point to any point
    def get_best_route_between_two(self, from_address_index, to_address_index):

        best_route_detail = (
            [from_address_index, to_address_index], self.get_distance_between(from_address_index, to_address_index))
        # create a dictionary to hold all the next address that needs to check
        address_needs_to_check = dict()
        # adding any hub point that travel distance are less than direct travel
        min_distance_detail = self.min_distance_table[from_address_index]
        for address_index, distance in min_distance_detail:
            # skip self
            if address_index == from_address_index:
                continue
            # do not check to_address_index for first time we check for the best route
            # we used it as default value for best route
            if address_index == to_address_index:
                break
            # check if any other point has less mile travel than direct travel
            if distance < best_route_detail[1]:
                total_distance = distance
                route = [from_address_index, address_index]
                address_needs_to_check[address_index] = (route, total_distance)
        for check_point in address_needs_to_check.values():
            best_route_detail = self.get_shortest_route(check_point[0], check_point[1], best_route_detail,
                                                        to_address_index)

        return best_route_detail

    def get_shortest_route(self, current_route, total_distance, best_route_detail, to_address_index):
        min_distance_detail = self.min_distance_table[current_route[-1]]
        for address_index, distance in min_distance_detail:
            if address_index in current_route:
                continue
            if distance + total_distance < best_route_detail[1]:
                new_route = current_route.copy()
                new_route.append(address_index)
                if address_index == to_address_index:
                    if distance + total_distance == best_route_detail[1]:
                        best_route_detail[0].extend(new_route)
                        return best_route_detail
                    else:
                        best_route_detail = (new_route, total_distance + distance)
                        return best_route_detail
                else:
                    if distance + total_distance < best_route_detail[1]:
                        best_route_detail = self.get_shortest_route(new_route, distance + total_distance,
                                                                    best_route_detail, to_address_index)
            else:
                return best_route_detail

    def get_shortest_route_dictionary(self):
        count = 0
        while count < len(self.distance_dictionary):
            for address_index in self.distance_dictionary.values():
                if count not in self.best_route_dictionary:
                    self.best_route_dictionary[count] = dict()
                    self.best_route_dictionary[count][address_index] = self.get_best_route_between_two(count, address_index)
                else:
                    self.best_route_dictionary[count][address_index] = self.get_best_route_between_two(count, address_index)
            count += 1

    def get_updated_min_distance_table(self):
        updated_min_distance_table = dict()
        for key in self.best_route_dictionary.keys():
            updated_min_distance_table[key] = []
            count = 0
            while count < len(self.best_route_dictionary):
                if count == 0:
                    updated_min_distance_table[key].append(self.best_route_dictionary[key][count])
                else:
                    is_insert = False
                    index = 0
                    # compare current term to entire list
                    for item in updated_min_distance_table[key]:
                        if float(item[1]) > float(self.best_route_dictionary[key][count][1]):
                            updated_min_distance_table[key].insert(index, self.best_route_dictionary[key][count])
                            is_insert = True
                            break
                        index += 1
                    # adding the address to end of list if it's farthest
                    if not is_insert:
                        updated_min_distance_table[key].append(self.best_route_dictionary[key][count])
                count += 1
        return updated_min_distance_table

    def get_point_must_visit(self):
        best_route_detail_from_hub = self.best_route_dictionary[0]
        address_index = 1
        address_must_visit = set()
        while len(self.best_route_dictionary) >= address_index:
            address_must_visit.add(address_index)
            address_index += 1
        for value in best_route_detail_from_hub.values():
            if len(value[0]) > 2:
                route = value[0][1:-1]
                for stop in route:
                    if stop in address_must_visit:
                        address_must_visit.remove(stop)

        return address_must_visit

    def add_same_address_package(self, available_package_truck):
        for package_id in available_package_truck:
            current_package = self.package_hashtable.lookup(package_id)
            if self.distance_dictionary[current_package.address] in self.address_package_dictionary:
                available_package_truck = available_package_truck.union(
                    self.address_package_dictionary[self.distance_dictionary[current_package.address]])
        return available_package_truck

    def find_address_index_by_package_id(self, package_id_list):
        address_needs_visit = set()
        for package_id in package_id_list:
            package = self.package_hashtable.lookup(package_id)
            address_index = self.distance_dictionary[package.address]
            if address_index not in address_needs_visit:
                address_needs_visit.add(address_index)
        return address_needs_visit
