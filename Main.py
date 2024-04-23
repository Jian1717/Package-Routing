from ScanCSVFile import *
from RouteCalculator import *
from PackageHashTable import *
from DistanceTable import *
from Console import *
from Truck import *

# Student_ID 010346276
# Jianxin Wang
# program start from here
def main():
    # loading package hashtable from WGUPS Package File
    package_hashtable = load_package_file()
    # loading distance table from WGUPS Distance Table
    distance_table = load_distance_table()
    route_calculator = RouteCalculator(distance_table, package_hashtable, [Truck(1), Truck(2)])
    route_calculator.calculate_routes()
    print('program ends')


if __name__ == '__main__':
    main()
