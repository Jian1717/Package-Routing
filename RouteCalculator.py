from PackageHashTable import *
from Truck import *
from DistanceTable import *
from datetime import *

class RouteCalculator:
    def __init__(self,distance_table:DistanceTable,package_hashtable:PackageHashTable,truck_list:list()):
        self.disance_table=distance_table
        self.package_hashtable=package_hashtable
        self.truck_list=truck_list
        self.task_list=[[],[]]
        self.bonded_package_dictionary=dict()

    
    #update the package on package_hashtable base on their special
    def check_special_notes(self):
        special_notes_list=self.package_hashtable.get_special_notes_list()
        for speical_request_package in special_notes_list:
            current_package=self.package_hashtable.lookup(speical_request_package)
            note=current_package.get_notes()
            #load package to truck 2
            if note == 'Can only be on truck 2':
                self.task_list[1].append(current_package.get_id())
            #set avaliable time to 9:05 am
            elif note == 'Delayed on flight---will not arrive to depot until 9:05 am':
                current_package.set_avaliable_time(datetime.strptime(str(date.today())+' '+'09:05 AM','%Y-%m-%d %I:%M %p'))
                self.package_hashtable.insert(current_package.get_id(),current_package)
            #set address for package 9 to correct address and update the avaliable time
            elif note == 'Wrong address listed':
                current_package.set_avaliable_time(datetime.strptime(str(date.today())+' '+'10:20 AM','%Y-%m-%d %I:%M %p'))
                current_package.set_address('410 S State St')
                self.package_hashtable.insert(current_package.get_id(),current_package)
            elif 'Must be delivered with' in note:
                note.replace(',',' ')
                string_list=note.split()
                self.bonded_package_dictionary[current_package.get_id()]=[]
                self.bonded_package_dictionary[current_package.get_id()].append(string_list[4])
                self.bonded_package_dictionary[current_package.get_id()].append(string_list[5])
        
    
    def calculate_routes(self):
        list_avaliable_package=set()
        self.check_special_notes()
        for bucket in self.package_hashtable.table:
            for package in bucket:
                list_avaliable_package.add(package[1].get_id())
                package[1].print_package_detail()
        return []
        