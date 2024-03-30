class Route:
    def __init__(self, route):
        self.route = route
        self.last_hub_index = [1]

    # break entire route assignment into individual route
    def get_route_breakdown(self):
        breakdown_list = []
        previous_index = 1
        for hub_index in self.last_hub_index:
            if hub_index == 1:
                continue
            else:
                breakdown_list.append(self.route[previous_index - 1:hub_index])
                previous_index = hub_index
        return breakdown_list

    def calculate_last_hub_index(self):
        self.last_hub_index.clear()
        for i, stop in enumerate(self.route):
            if stop.address_index == 0:
                self.last_hub_index.append(i + 1)

    # for troubleshooting use only
    def get_route_package_list(self):
        package_list = []
        for stop in self.route:
            if stop.address_index == 0:
                package_list.append(0)
            else:
                package_list.append(stop.package_id)
        return package_list
