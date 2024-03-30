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
        self.best_route_dictionary = dict
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
        # find the shortest route for 40 package without check any conditions
        package_list.difference_update(self.delay_package_list)
        rush_bonded_package = self.rush_package_list.intersection(self.bonded_package_list)
        available_package_for_truck_1 = set()
        available_package_for_truck_2 = self.delay_package_list
        # adding bonded rush package into available list
        self.add_bonded_package(available_package_for_truck_1, package_list)
        # adding same address package into list
        self.add_same_address_package(available_package_for_truck_1, package_list)
        self.add_same_address_package(available_package_for_truck_2, package_list)
        test = Route([Stop(None, 0)])
        while len(available_package_for_truck_1) > 0:
            self.get_shortest_next_stop(test, available_package_for_truck_1)
        best_route_detail = self.get_best_route_between_two(0, 16)
        print(best_route_detail)
        is_insert = False
        while len(package_list) > 0:
            if not is_insert and current_route.last_hub_index[-1] > 1:
                package_list = package_list.union(self.delay_package_list)
                is_insert = True
            self.get_shortest_next_stop(current_route, package_list)
        travel_time_truck_1 = datetime.strptime(str(date.today()) + ' ' + '08:00 AM', '%Y-%m-%d %I:%M %p')
        # truck 2 will wait for delay package and departure from Hub at 9:05 am
        travel_time_truck_2 = datetime.strptime(str(date.today()) + ' ' + '09:05 AM', '%Y-%m-%d %I:%M %p')
        breakdown_list = current_route.get_route_breakdown()
        truck_1_route = Route([])
        truck_2_route = Route([])
        count = 1
        # break down route assignment for truck 1 and 2
        for route in breakdown_list:
            if count % 2 == 1:
                for stop in route:
                    truck_1_route.route.append(stop)
            else:
                for stop in route:
                    truck_2_route.route.append(stop)
            count += 1
        self.truck_list[0].route = truck_1_route
        self.truck_list[1].route = truck_2_route
        self.truck_list[0].calculate_total_distance_travel()
        self.truck_list[1].calculate_total_distance_travel()
        total_distance = self.truck_list[0].total_delivery_mileage + self.truck_list[1].total_delivery_mileage
        # initial check for route assignment
        self.check_route(self.truck_list[0], travel_time_truck_1)
        self.check_route(self.truck_list[1], travel_time_truck_2)

        # continue route adjustment until all route pass the validation
        while len(self.failed_package_dictionary) > 0:
            self.check_fail_step(self.get_sorted_fail_package(), self.truck_list)
            # reset failed_package_dictionary before the validation
            self.failed_package_dictionary.clear()
            # revalidate the route assignment after route adjustment
            self.check_route(self.truck_list[0], travel_time_truck_1)
            b_breakdown = self.truck_list[1].route.get_route_breakdown()
            self.truck_list[1].route.route = b_breakdown[1] + b_breakdown[0]
            self.check_route(self.truck_list[1], travel_time_truck_2)
            list_a = self.truck_list[0].route.get_route_package_list()
            list_b = self.truck_list[1].route.get_route_package_list()
            self.truck_list[0].calculate_total_distance_travel()
            self.truck_list[1].calculate_total_distance_travel()
            total_distance = self.truck_list[0].total_delivery_mileage + self.truck_list[1].total_delivery_mileage

            print('i am here')
        '''''
        while len(self.failed_package_dictionary) > 0:
            self.fix_fail_stop(current_route)
            self.validating_routes(current_route)
        return current_route
        '''

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

    def adding_hub_stop(self, current_route):
        current_stop = current_route.route[-1]
        next_stop = Stop(None, 0)
        next_stop.distance = self.get_distance_between(next_stop.address_index, current_stop.address_index)
        next_stop.travel_time = timedelta(
            hours=next_stop.distance / 18)
        current_route.route.append(next_stop)
        current_route.last_hub_index.append(len(current_route.route))

    def calculate_travel_time(self, current_stop, next_stop):
        next_stop.distance = self.get_distance_between(next_stop.address_index, current_stop.address_index)
        next_stop.travel_time = timedelta(
            hours=next_stop.distance / 18)

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
                            next_stop.distance = distance
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
            # adding hub stop when all packages are assigned
            if len(package_list) == 0:
                self.adding_hub_stop(current_route)

    def get_distance_between(self, current_address_id, next_address_id):

        try:
            value = self.distance_table[next_address_id][current_address_id]
        except:
            value = self.distance_table[current_address_id][next_address_id]

        return float(value)

    def check_fail_step(self, sorted_failed_package_list, truck_list):
        truck_1 = truck_list[0]
        truck_2 = truck_list[1]
        truck_1.calculate_package_list()
        truck_2.calculate_package_list()
        available_package_truck_1 = truck_1.package_list
        available_package_truck_2 = truck_2.package_list
        while len(sorted_failed_package_list) > 0:
            if 'failed delivery by truck 2' in sorted_failed_package_list:
                available_package_truck_1.difference_update(sorted_failed_package_list['failed delivery by truck 2'])
                available_package_truck_2 = available_package_truck_2.union(sorted_failed_package_list['failed '
                                                                                                       'delivery by '
                                                                                                       'truck 2'])
                truck_1_route = Route([Stop(None, 0)])
                truck_2_route = Route([Stop(None, 0)])
                # recalculate best route for truck 1
                while len(available_package_truck_1) > 0:
                    self.get_shortest_next_stop(truck_1_route, available_package_truck_1)
                # recalculate best route for truck 2
                while len(available_package_truck_2) > 0:
                    self.get_shortest_next_stop(truck_2_route, available_package_truck_2)
                truck_1.route = truck_1_route
                truck_2.route = truck_2_route
                break

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

    def add_same_address_package(self, available_package_truck, package_list):
        for package_id in available_package_truck:
            current_package = self.package_hashtable.lookup(package_id)
            if self.distance_dictionary[current_package.address] in self.address_package_dictionary:
                if self.address_package_dictionary[self.distance_dictionary[current_package.address]].issubset(
                        package_list):
                    available_package_truck = available_package_truck.union(
                        self.address_package_dictionary[self.distance_dictionary[current_package.address]])
        package_list.difference_update(available_package_truck)

    def add_bonded_package(self, available_package_truck, package_list):
        for package_id in available_package_truck:
            if package_id in self.bonded_package_list:
                available_package_truck = available_package_truck.union(self.bonded_package_dictionary[package_id])
            package_list.difference_update(available_package_truck)

    # get best route get from any point to hub
    def get_best_route_between_two(self, from_address_index, to_address_index):
        best_route_detail = (
            [from_address_index, to_address_index], self.get_distance_between(from_address_index, to_address_index))
        # create a dictionary to hold all the next address that needs to check
        address_needs_to_check = dict()
        # adding any hub point that travel distance are less than direct hub return
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
                route = [address_index, from_address_index]
                address_needs_to_check[address_index] = (route, total_distance)
        for check_point in address_needs_to_check.values():
            self.get_shortest_route(check_point[0],
                                    check_point[1],
                                    best_route_detail,
                                    to_address_index)

        return best_route_detail

    def get_shortest_route(self, current_route, total_distance, best_route_detail, to_address_index):
        min_distance_detail = self.min_distance_table[current_route[0]]
        for address_index, distance in min_distance_detail:
            if address_index in current_route:
                continue
            if distance + total_distance < best_route_detail[1]:
                current_route.insert(0, address_index)
                if address_index == to_address_index:
                    if distance + total_distance == best_route_detail[1]:
                        best_route_detail[0].extend(current_route)
                    else:
                        best_route_detail = (current_route, total_distance + distance)
                    return
                else:
                    # to check if there is room for minimum distance return to to_address
                    if distance + total_distance + self.min_distance_table[to_address_index][1][1] < best_route_detail[1]:
                        self.get_shortest_route(current_route, distance + total_distance, best_route_detail,
                                            to_address_index)
                    current_route.pop(0)
            else:
                continue
