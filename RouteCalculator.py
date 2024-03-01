from PackageHashTable import *
from Truck import *
from DistanceTable import *
from datetime import *
from Stop import *


class RouteCalculator:
    def __init__(self, distance_table: DistanceTable, package_hashtable: PackageHashTable, truck_list):
        self.distance_table = distance_table.get_distance_table()
        self.distance_dictionary = distance_table.get_address_dictionary()
        self.package_hashtable = package_hashtable
        self.truck_list = truck_list
        self.truck2_package_list = set()
        self.task_list = [[0], [0]]
        self.all_possible_routes = []
        self.bonded_package_dictionary = dict()
        self.package_failed_index = dict()
        self.rush_package_list = set()
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
            # set available time to 9:05 am
            elif note == 'Delayed on flight---will not arrive to depot until 9:05 am':
                current_package.set_available_time(
                    datetime.strptime(str(date.today()) + ' ' + '09:05 AM', '%Y-%m-%d %I:%M %p'))
                self.package_hashtable.insert(current_package.get_id(), current_package)
                self.rush_package_list.add(current_package.get_id())
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

    def calculate_routes(self):
        anytime_package_list = list()
        start_time = datetime.strptime(str(date.today()) + ' ' + '08:00 AM', '%Y-%m-%d %I:%M %p')
        self.check_special_notes()
        # load packages in package hashtable into a list
        for bucket in self.package_hashtable.table:
            for package in bucket:
                anytime_package_list.append(package[1].get_id())
                self.package_failed_index[package[1].get_id()] = 50
        # finding all delivery routes 
        self.find_routes(anytime_package_list, [Stop(None, 0)], 1, start_time, start_time)
        # planning the best route for rush package

        return self.all_possible_routes

    # find a 15 package route for truck
    def find_routes(self, package_list: list[int], current_route, route_count: int, current_time_truck_1,
                    current_time_truck_2):
        route_count = route_count
        if route_count % 2 == 0:
            current_time = current_time_truck_2
        else:
            current_time = current_time_truck_1

        # exit condition for recursion function -- all the package is assigned to a route
        if len(package_list) == 0:
            # add returning to hub when all packages are assigned
            hub_stop = Stop(None, 0)
            hub_stop.travel_time = timedelta(hours=self.get_distance_between(current_route[-1].address_index, 0) / 18)
            current_route.append(hub_stop)
            # adding the time for returning back to hub
            self.all_possible_routes.append(current_route)
            return

        if len(package_list) > 0:
            available_package = package_list.copy()
            for package_id in available_package:
                if package_id in self.truck2_package_list and route_count % 2 == 1:
                    continue
                if self.package_failed_index[package_id] > len(current_route):
                    next_package = self.package_hashtable.lookup(package_id)
                    if next_package.available_time <= current_time:
                        current_stop = current_route[-1]
                        next_stop = Stop(package_id, self.distance_dictionary[next_package.get_address()])
                        next_stop.travel_time = timedelta(
                            hours=self.get_distance_between(next_stop.address_index, current_stop.address_index) / 18)
                        future_time = current_time + next_stop.travel_time
                        if future_time <= next_package.get_deadline():
                            current_route.append(next_stop)
                            package_list.remove(package_id)
                            # check if 15 package is assigned a route
                            if len(current_route) % 16 == 0:
                                # adding the time for returning back to hub
                                hub_stop = Stop(None, 0)
                                hub_stop.travel_time = timedelta(
                                    hours=self.get_distance_between(next_stop.address_index, 0) / 18)
                                current_route.append(hub_stop)
                                future_time = future_time + hub_stop.travel_time
                                # increment route_count for next Truck's route assignment
                                route_count += 1
                            # recursion call for Truck 2 route assignment
                            if route_count % 2 == 0:
                                self.find_routes(package_list, current_route, route_count, current_time_truck_1,
                                                 future_time)
                            # recursion call for Truck 1 route assignment
                            else:
                                self.find_routes(package_list, current_route, route_count, future_time,
                                                 current_time_truck_2)
                            if current_route[-1].address_index == 0 and len(current_route) > 1:
                                current_route.pop()
                                route_count -= 1
                            package_list.append(next_stop.package_id)
                            current_route.pop()
                        else:
                            self.package_failed_index[next_stop.package_id] = len(current_route)
                            break
                    else:
                        continue

                    # find the distance between two address

    def get_distance_between(self, current_truck_address_id, next_destination_address_id):
        try:
            value = self.distance_table[next_destination_address_id][current_truck_address_id]
        except:
            value = self.distance_table[current_truck_address_id][next_destination_address_id]

        return float(value)

    def check_rush_package(self, current_route, current_time_truck_1, current_time_truck_2):
        return
