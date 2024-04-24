from Package import Package
from datetime import *


class Truck:
    def __init__(self, truck_id):
        self.route = None
        self.id = truck_id
        self.package_list = set()
        self.total_delivery_mileage = 0
        self.departure_time = None
        self.work_log = None

    def calculate_total_distance_travel(self):
        self.total_delivery_mileage = 0
        is_first_stop = True
        previous_address_index = 0
        for stop in self.route.route:
            if is_first_stop:
                is_first_stop = False
                continue
            else:
                if previous_address_index == stop.address_index:
                    continue
                else:
                    self.total_delivery_mileage += stop.distance
                    previous_address_index = stop.address_index

    # update worklog and log truck activity
    def deploy_package(self, package_hashtable, delay_package_list):
        self.work_log = dict()
        load_time = self.departure_time
        current_time = self.departure_time
        # update the status of package when package is at_hub, delayed, loaded to truck and out for delivery
        for package_id in self.package_list:
            self.work_log[package_id] = list()
            current_package = package_hashtable.lookup(package_id)
            # add status for each package before loaded to truck
            if package_id in delay_package_list:
                status = 'Delayed'
            else:
                status = 'AtHub'
            package_detail = current_package.package_detail(status)
            self.work_log[package_id].append((
                datetime.strptime(str(date.today()) + ' ' + '12:00 AM', '%Y-%m-%d %I:%M %p'), package_detail))
            # update status when packages are loaded to truck
            status = 'InRoute by Truck-' + str(self.id) + ', ' + self.departure_time.strftime('%I:%M %p')
            package_detail = current_package.package_detail(status)
            self.work_log[package_id].append((load_time, package_detail))
            # update the address for package 9 when it's 10:20 am
            if package_id == '9':
                current_package.address = '410 S State St'
                current_package.city = 'Salt Lake City'
                current_package.zip_code = 84111
                package_hashtable.insert(package_id, current_package)
                package_detail = current_package.package_detail(status)
                self.work_log[package_id].append(
                    (datetime.strptime(str(date.today()) + ' ' + '11:20 AM', '%Y-%m-%d %I:%M %p'), package_detail))
        # update the status of package when package is delivered
        for stop in self.route.route:
            current_time = current_time + stop.travel_time
            if stop.package_id is not None:
                current_package = package_hashtable.lookup(stop.package_id)
                status = 'delivered by Truck-' + str(self.id) + ', ' + current_time.strftime('%I:%M %p')
                package_detail = current_package.package_detail(status)
                self.work_log[stop.package_id].append((current_time, package_detail))
