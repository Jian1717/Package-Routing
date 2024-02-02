from ScanCSVFile import *
from RouteCalculator import *
from PackageHashTable import *
from DistanceTable import *
from Console import *
from Truck import *



#program strat from here
def main():
    package_hashtable = load_package_file()
    distance_table = load_distance_table()
    route_calculator= RouteCalculator(distance_table,package_hashtable,[Truck(1,'driver 1'),Truck(2,'driver 2')])
    task_list=route_calculator.calculate_routes()
    print(task_list)
if __name__ == '__main__':
    main()