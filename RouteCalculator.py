from PackageHashTable import *
from Truck import *
from DistanceTable import *
from datetime import *

class RouteCalculator:
    def __init__(self,distance_table:DistanceTable,package_hashtable:PackageHashTable,truck_list:list()):
        self.disance_table=distance_table.get_distance_table()
        self.distace_dicitionary=distance_table.get_address_dicitonary()
        self.package_hashtable=package_hashtable
        self.truck_list=truck_list
        self.truck2_package_list=set()
        self.task_list=[[0],[0]]
        self.all_possible_routes=[]
        self.bonded_package_dictionary=dict()
        self.rush_package_list=set()
    
    #update the package on package_hashtable base on their special notes
    def check_special_notes(self):
        special_notes_list=self.package_hashtable.get_special_notes_list()
        for speical_request_package in special_notes_list:
            current_package=self.package_hashtable.lookup(speical_request_package)
            note=current_package.get_notes()
            #load package to truck 2
            if note == 'Can only be on truck 2':
                self.truck2_package_list.add(current_package.get_id())
            #set avaliable time to 9:05 am
            elif note == 'Delayed on flight---will not arrive to depot until 9:05 am':
                current_package.set_avaliable_time(datetime.strptime(str(date.today())+' '+'09:05 AM','%Y-%m-%d %I:%M %p'))
                self.package_hashtable.insert(current_package.get_id(),current_package)
                self.rush_package_list.add(current_package.get_id())
            #set address for package 9 to correct address and update the avaliable time
            elif note == 'Wrong address listed':
                current_package.set_avaliable_time(datetime.strptime(str(date.today())+' '+'10:20 AM','%Y-%m-%d %I:%M %p'))
                current_package.set_address('410 S STATE ST')
                self.package_hashtable.insert(current_package.get_id(),current_package)
            elif 'Must be delivered with' in note:
                note.replace(',',' ')
                string_list=note.split()
                self.bonded_package_dictionary[current_package.get_id()]=[]
                self.bonded_package_dictionary[current_package.get_id()].append(string_list[4])
                self.bonded_package_dictionary[current_package.get_id()].append(string_list[5])
        
    
    def calculate_routes(self):
        anytime_package_list=list() 
        start_time=datetime.strptime(str(date.today())+' '+'08:00 AM','%Y-%m-%d %I:%M %p')
        self.check_special_notes()
        for bucket in self.package_hashtable.table:
            for package in bucket:
                anytime_package_list.append(package[1].get_id())
        #finding all delivery routes for 
        self.find_routes(anytime_package_list,[0],1,start_time,start_time)
        #planning the best route for rush package
                
                
        return self.all_possible_routes
    
    
    #find a 15 package route for truck
    def find_routes(self,package_list:list[int], current_route:list[int], route_count:int, current_time_truck_1,current_time_truck_2):
        print(route_count)
        print('current route: ')
        print(current_route)
        #returning to hub when 15 packages is assigned to one route
        print('current avaiable packages:')
        print(package_list)
        if route_count%2==0:
            current_time=current_time_truck_2
        else:
            current_time=current_time_truck_1
            
        if len(current_route)%16==0:
            current_route.append(0)
            #adding the time for returning back to hub
            current_time=current_time+timedelta(hours=self.get_distance_between(current_route[-1],0)/18)
            route_count +=1
            
        #exit condidition for recurrsion function -- all the package is assigned to a route
        if len(package_list) ==0:
            # add retruning to hub when all packages are assined 
            current_route.add(0)
            #adding the time for returning back to hub
            current_time=current_time+timedelta(hours=self.get_distance_between(current_route[-1],0)/18)
            print(current_route)
            self.all_possible_routes.append(current_route)
            return
        
        if(len(current_route)==1):
            #Assigning first package in truck 1 with all possible combination (excluding packages that only for truck 2)
            for package_id in package_list:
                #finding all possible delivery routes
                if package_id not in self.truck2_package_list: 
                    package_list.remove(package_id)
                    self.find_routes(package_list,[0,package_id],route_count,current_time_truck_1,current_time_truck_2)
                    package_list.append(package_id)
                print('all possiable route starting with ')
                print(package_id)
                print('are now finished')
            return
        
        if len(package_list) >0:
            avaliable_package=package_list.copy()
            for package_id in avaliable_package:
                if package_id in self.truck2_package_list and route_count%2==1:
                    continue
                next_package=self.package_hashtable.lookup(package_id)
                print(next_package.print_package_detail())
                if next_package is not None:
                    next_package_destination_address_id=self.distace_dicitionary[next_package.get_address()]
                    #if truck is in the hub assign 0 to address_id
                    if current_route[-1]==0:
                        current_truck_address_id=0
                    #look up address_id for current package
                    else:
                        current_truck_address_id=self.distace_dicitionary[self.package_hashtable.lookup(current_route[-1]).get_address()]
                    print('current stop address: '+str(current_truck_address_id))
                    distance=self.get_distance_between(current_truck_address_id,next_package_destination_address_id)
                    print('distance between: '+str(distance))
                    if distance >0:
                        print('time before delievering next package: ')
                        print(current_time)
                        current_time=timedelta(hours=distance/18)+current_time
                        print('time after delivering')
                        print(current_time)
                        if current_time<=next_package.get_deadline():
                            current_route.append(package_id)
                            print('remvoing package ID: ' +str(package_id))
                            print('current pakage list: ')
                            print(package_list)
                            try:
                                package_list.remove(package_id)
                                print('package '+ str(package_id)+ 'is found in package_list')
                            except ValueError:
                                print('package '+ str(package_id)+ 'is found in package_list')
                            #updating time for truck 2
                            print('package_list:')
                            print(package_list)
                            if route_count%2==0:
                                self.find_routes(package_list,current_route,route_count,current_time_truck_1,current_time)
                            #updating time for truck 1
                            else:
                                self.find_routes(package_list,current_route,route_count,current_time,current_time_truck_2)
                        else:
                            pass
                    else:
                        print('no path between current stop to next package')
        return 

    #find the distance between two address
    def get_distance_between(self,current_truck_address_id,next_destination_address_id):
        if current_truck_address_id<next_destination_address_id:
            value=self.disance_table[next_destination_address_id][current_truck_address_id]
        else:     
            value=self.disance_table[current_truck_address_id][next_destination_address_id]
        if value is not None:
            return float(value)
        return -1