# display menu for package routing program
from datetime import datetime, date


def print_time_frame_look_up_menu():
    print('****************************************')
    print('please enter a time in following format HH:MM AM/PM')
    print('****************************************')


class Console:
    def __init__(self, work_log, truck_list):
        self.work_log = work_log
        self.truck_list = truck_list

    # display main menu
    def print_main_menu(self):
        print('****************************************')
        print('1. Print All Package Status and Total Mileage')
        print('2. Get a Single Package Status with a Time ')
        print('3. Get All Package Status with a Time ')
        print('4. Exit the Program')
        print('****************************************')
        print('')

    # prompt for user input
    def ask_user_input(self, prompt_string):
        return input(prompt_string)

    # display greeting message
    def print_greeting_message(self):
        print('****************************************')
        print('***Welcome to Package Routing Program***')
        print('****************************************')
        print('')

    def print_package_status_and_total__mileage_menu(self):
        print('')
        print('****************************************')
        print('****Package Status And Total Mileage****')
        print('****************************************')
        print('')

    def print_sigle_package_status_with_time_menu(self):
        print('')
        print('****************************************')
        print('*********Package Status Look Up*********')
        print('****************************************')
        print('')

    def print_time_frame_search_menu(self):
        print('')
        print('****************************************')
        print('******Search All Packages By Time*******')
        print('****************************************')
        print('')

    # print error message when user enter incorrect input

    # print all packages status
    def print_all_package_status_and_miles(self):
        print('')
        print('-----------------Packages_Status-----------------')
        count = 1
        while count <= len(self.work_log):
            for status_detail in self.work_log[str(count)]:
                print(status_detail[1])
            count += 1
        print('')
        print('-------------------Total_Miles-------------------')
        total_miles = 0
        for truck in self.truck_list:
            print('Distance traveled by truck ' + str(truck.id) + ' : ' + "%.2f" % truck.total_delivery_mileage)
            total_miles = total_miles + truck.total_delivery_mileage
        print('Total miles traveled: ' + "%.2f" % total_miles)
        print('')

    # look for single package status with given time frame
    def get_package_status_with_a_time(self, package_id, time):
        time = datetime.strptime(str(date.today()) + ' ' + time, '%Y-%m-%d %I:%M %p')
        most_recent_status = None
        for status_detail in self.work_log[package_id]:
            if time >= status_detail[0]:
                most_recent_status = status_detail
            else:
                break
        print('')
        print('-----------------Packages_Status-----------------')
        print('Time: ' + time.strftime('%I:%M %p'))
        print('Status: ' + most_recent_status[1])
        print('')

    # look for all packages status by a target time
    def time_frame_search(self, time):
        time = datetime.strptime(str(date.today()) + ' ' + time, '%Y-%m-%d %I:%M %p')
        most_recent_status = None
        print('')
        print('Time: ' + time.strftime('%I:%M %p'))
        print('')
        print('-----------------Packages_Status-----------------')
        count = 1
        while count <= len(self.work_log):
            for status_detail in self.work_log[str(count)]:
                if time >= status_detail[0]:
                    most_recent_status = status_detail
                else:
                    print(most_recent_status[1])
                    break
            count += 1
        print('')

    # look for all loaded packages status by a time frame.  This function won't appear in GUI.
    def time_frame_loaded_packages_check(self, start, end, title):
        start_time = datetime.strptime(str(date.today()) + ' ' + start, '%Y-%m-%d %I:%M %p')
        end_time = datetime.strptime(str(date.today()) + ' ' + end, '%Y-%m-%d %I:%M %p')
        print('')
        print('-----------------'+title+'-----------------')
        count = 1
        for truck in self.truck_list:
            print('Truck_'+str(truck.id)+'_Package_status: ')
            for package_id in truck.package_list:
                is_print=False
                if start_time <= truck.departure_time <= end_time:
                    print(self.work_log[str(package_id)][0][1])
                for status_detail in self.work_log[str(package_id)]:
                    if start_time <= status_detail[0] <= end_time:
                        print(status_detail[1])
                        is_print=True
                if not is_print:
                    if end_time < truck.departure_time:
                        print(self.work_log[str(package_id)][0][1])
                    else:
                        print(self.work_log[str(package_id)][-1][1])
        print('')
