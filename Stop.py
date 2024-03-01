from datetime import *


class Stop:
    def __init__(self, package_id, address_index):
        self.package_id = package_id
        self.address_index = address_index
        self.travel_time = timedelta(0)

