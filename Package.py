from datetime import datetime
from datetime import *


class Package:
    def __init__(self, package_id, address: str, deadline: datetime, city: str, zip_code: int, weight: int, notes: str,
                 status: str, state: str):
        self.id = package_id
        self.address = address
        self.deadline = deadline
        self.start_delivery_time = None
        self.available_time = (datetime.strptime(str(date.today()) + ' ' + '08:00 AM', '%Y-%m-%d %I:%M %p'))
        self.load_time = None
        self.city = city
        self.zip_code = zip_code
        self.weight = weight
        self.notes = notes
        self.status = status
        self.state = state

    # getter and setter for package

    def get_id(self):
        return self.id

    def set_id(self, package_id):
        self.id = package_id

    def get_address(self):
        return self.address

    def set_address(self, value):
        self.address = value

    def get_deadline(self):
        return self.deadline

    def set_deadline(self, value):
        self.deadline = value

    def get_start_delivery_time(self):
        return self.start_delivery_time

    def set_start_delivery_time(self, value):
        self.start_delivery_time = value

    def get_available_time(self):
        return self.available_time

    def set_available_time(self, value):
        self.available_time = value

    def get_city(self):
        return self.city

    def set_city(self, value):
        self.city = value

    def get_zip_code(self):
        return self.zip_code

    def set_zip_code(self, value):
        self.zip_code = value

    def get_weight(self):
        return self.weight

    def set_weight(self, value):
        self.weight = value

    def get_notes(self):
        return self.notes

    def set_notes(self, value):
        self.notes = value

    def get_status(self):
        return self.status

    def set_status(self, value):
        self.status = value

    # generate package detail for GUI display
    def package_detail(self, status):
        package_detail = self.id + ', ' + self.address + ', ' + self.city + ', ' + self.state + ', ' + str(self.zip_code) + ', '
        end_of_day = datetime.strptime(str(date.today()) + ' ' + '11:59 PM', '%Y-%m-%d %I:%M %p')
        # print EOD if package is not rush
        if self.deadline == end_of_day:
            package_detail = str(package_detail) + 'EOD'
        else:
            package_detail = str(package_detail) + self.deadline.strftime('%I:%M %p')
        package_detail = package_detail + ', ' + str(self.weight)
        # check to see if there is any special notes
        if self.notes != '':
            package_detail = package_detail + ', ' + self.notes
        # print custom status
        package_detail = package_detail + ', ' + status
        return package_detail
