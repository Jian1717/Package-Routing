from Package import Package
from datetime import *
class Truck:
    def __init__(self,id:int,driver:str):
        self.loaded_package_list=[Package]
        self.task_list=list()
        self.id=id
        self.driver=driver
        self.total_delivery_milage=0
        self.time=datetime.strptime(str(date.today())+' '+'08:00 AM','%Y-%m-%d %I:%M %p')
        self.worklog=[]
    
    #add new package to loaded_package_list
    def load_package(self,package:Package):
        self.loaded_package_list.append(package)
    
    #remove target package from loaded_package_list
    def remove_package(self,package:Package):
        for pk in self.loaded_package_list:
            if pk.get_id() ==package.get_id():
                 self.loaded_package_list.remove(pk)
                 return True
        return False         
    #assign a driver to truck
    def assign_driver(self,driver:str):
        self.driver=driver
    '''    
    #dispatched all the packages that load on this truck and update the worklog
    def delivery(self,address_dicitonary:dict[str,int]):
        self.worklog.append('Truck #'+self.id+' is out for delivery with '+self.driver+'as assigned driver   '+self.time)
        for task in self.task_list:
    '''        
            