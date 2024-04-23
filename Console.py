class Console:
    def __init__(self):
        pass

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

    def print_single_package_look_up_menu(self):
        print('****************************************')
        package_id=self.ask_user_input('please enter a package ID')
        try:
            int(package_id)
        except:
            self.print_error_message('invalid user input')
        time = self.ask_user_input('please enter a time')
        try:
            target_time= datetime.strptime(str(date.today()) + ' ' + time, '%Y-%m-%d %I:%M %p')
        except:
            self.print_error_message('invalid user input')
        print('****************************************')

    def print_time_frame_look_up_menu(self):
        print('****************************************')
        print('please enter a time in following format HH:MM AM/PM')
        print('****************************************')
    # print error message when user enter incorrect input
    def print_error_message(self,message):
        print(message)
        print('please try again')