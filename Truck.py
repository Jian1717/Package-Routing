from Package import Package
from datetime import *


class Truck:
    def __init__(self, truck_id):
        self.route = None
        self.id = truck_id
        self.package_list = set()
        self.total_delivery_mileage = 0
        self.departure_time = datetime.strptime(str(date.today()) + ' ' + '08:00 AM', '%Y-%m-%d %I:%M %p')
        self.work_log = []

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

    def calculate_package_list(self):
        if self.route is not None:
            self.package_list.clear()
            for stop in self.route.route:
                if stop.address_index == 0:
                    continue
                else:
                    self.package_list.add(stop.package_id)

    '''    
    #dispatched all the packages that load on this truck and update the work_log
    def delivery(self,address_dictionary:dict[str,int]):
        self.work_log.append('Truck #'+self.id+' is out for delivery with '+self.driver+'as assigned driver   '+self.time)
        for task in self.task_list:
    '''
