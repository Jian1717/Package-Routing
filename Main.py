from ScanCSVFile import *
from RouteCalculator import *
from PackageHashTable import *
from DistanceTable import *
from Console import *
from Truck import *



#program strat from here
def main():
    print('hi')
    package_hashtable = load_package_file()
    print('hi')
    distance_table = load_distance_table()
    print('hi')
    route_calculator= RouteCalculator(distance_table,package_hashtable,[Truck(1,'driver 1'),Truck(2,'driver 2')])
    print('hi')
    task_list=route_calculator.calculate_routes()



if __name__ == '__main__':
    main()