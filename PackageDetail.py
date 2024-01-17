from datetime import datetime 
class PackageDetail:
    def __init__(self,id:int, address:str, deadline:datetime, city:str, zip_code:int,weight:int,notes:str,status:str):
        self.id=id
        self.address =address
        self.deadline=deadline
        self.city=city
        self.zip_code=zip_code
        self.weight=weight
        self.notes=notes
        self.status=status
    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id
        
    def get_address(self):
        return self.address

    def set_address(self, value):
        self.address = value

    def get_deadline(self):
        return self.deadline

    def set_deadline(self, value):
        self.deadline = value

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
        self.notes=value
        
    def get_status(self):
        return self.status

    def set_status(self, value):
        self.status = value

 
        