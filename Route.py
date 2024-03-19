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
                breakdown_list.append(self.route[previous_index-1:hub_index])
                previous_index = hub_index
        return breakdown_list
