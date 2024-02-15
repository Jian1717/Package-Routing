#create class to hold distance table and address look up list
class DistanceTable:
    def __init__(self,distance_table:list[list[float]],address_dicitonary:dict[str,int]):
        self.distance_table=distance_table
        self.address_dicitonary=address_dicitonary

    def get_distance_table(self):
        return self.distance_table
    
    def get_address_dicitonary(self):
        return self.address_dicitonary

