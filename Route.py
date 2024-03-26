class Route:
    def __init__(self, route):
        self.route = route
        self.last_hub_index = [1]

    # break entire route assignment into individual route
    def get_route_breakdown(self):
        breakdown_list = []
        truck_1_route_list = []
        truck_2_route_list = []
        count = 1
        previous_index = 1
        for hub_index in self.last_hub_index:
            if hub_index == 1:
                continue
            else:
                if count%2 ==1:
                    truck_1_route_list.append(self.route[previous_index-1:hub_index])
                else:
                    truck_2_route_list.append(self.route[previous_index - 1:hub_index])
                previous_index = hub_index
                count += 1
        breakdown_list.append(truck_1_route_list)
        breakdown_list.append(truck_2_route_list)
        return breakdown_list
