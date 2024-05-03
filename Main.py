import copy
from ScanCSVFile import *
from RouteCalculator import *
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
    truck_list = [Truck(1), Truck(2), Truck(3)]
    route_calculator = RouteCalculator(distance_table, copy.copy(package_hashtable), truck_list)
    # get delay package list
    delay_package_list = route_calculator.delay_package_list
    # to calculate and validate route assignment
    if route_calculator.calculate_routes():
        # reset package_hashtable
        package_hashtable = load_package_file()
        work_log = dict()
        # deploy the package
        for truck in truck_list:
            truck.deploy_package(package_hashtable, delay_package_list)
            # merge worklog for all three trucks
            work_log = work_log | truck.work_log
        console = Console(work_log, truck_list)
        console.print_greeting_message()
        menu_option = ''
        # core function for GUI
        while menu_option != '5':
            console.print_main_menu()
            menu_option = input('please choose a menu option:')
            # print out all status for all packages
            if menu_option == '1':
                console.print_package_status_and_total__mileage_menu()
                console.print_all_package_status_and_miles()
            # print out most recent status for a target package on a target time
            elif menu_option == '2':
                try:
                    console.print_sigle_package_status_with_time_menu()
                    package_id = input('please enter a package id: ')
                    target_time = input('please enter a time in following format HH:MM AM/PM: ')
                    target_time.upper()
                    console.get_package_status_with_a_time(package_id, target_time)
                except:
                    print('invalid Data Entry, please try again')
            # print out most recent status for all packages on a target time
            elif menu_option == '3':
                console.print_time_frame_search_menu()
                try:
                    target_time = input('please enter a time in following format HH:MM AM/PM: ')
                    target_time.upper()
                    console.time_frame_search(target_time)
                except:
                    print('invalid Data Entry, please try again')
            elif menu_option == '4':
                try:
                    target_start_time = input('please enter start time in following format HH:MM AM/PM: ')
                    target_start_time.upper()
                    target_end_time = input('please enter end time in following format HH:MM AM/PM: ')
                    target_end_time.upper()
                    console.time_frame_loaded_packages_check(target_start_time, target_end_time, 'Status Check Between '+target_start_time+' and '+target_end_time)
                except:
                    print('invalid Data Entry, please try again')
            # run the phrase check won't have display menu
            elif menu_option == 'run phrase check':
                console.time_frame_loaded_packages_check('8:35 AM','9:25 AM','First Status Check')
                console.time_frame_loaded_packages_check('9:35 AM', '10:25 AM', 'Second Status Check')
                console.time_frame_loaded_packages_check('12:03 PM', '1:12 PM', 'Third Status Check')
    else:
        print('Please manually re-assign packages.  Current assignment doesn\'t pass validations')
    print('program ends')
    quit()


if __name__ == '__main__':
    main()
