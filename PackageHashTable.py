# C950 - Webinar-1 - Let’s Go Hashing
# W-1_ChainingHashTable_zyBooks_Key-Value.py
# Ref: zyBooks: Figure 7.8.2: Hash table using chaining.
 
# HashTable class using chaining.
from Package import Package

class PackageHashTable:
    # Constructor with optional initial capacity parameter.
    # Assigns all buckets with an empty list.
    def __init__(self, initial_capacity=10):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        # list of all package that has special notes
        self.special_notes_list = []
        for i in range(initial_capacity):
            self.table.append([])
      
    # Inserts a new item into the hash table.
    def insert(self, package_id:int, package:Package): #  does both insert and update 
        # get the bucket list where this item will go.
        bucket = hash(package_id) % len(self.table)
        bucket_list = self.table[bucket]
 
        # update package_id if it is already in the bucket
        for kv in bucket_list:
          if kv[0] == package_id:
            kv[1] = package
            return True
    
        # if not, insert the item to the end of the bucket list.
        key_value = [package_id, package]
        bucket_list.append(key_value)
        return True
 
    # Searches for an item with matching package_id in the hash table.
    # Returns the item if found, or None if not found.
    def lookup(self, package_id:int):
        # get the bucket list where this package_id would be.
        bucket = hash(package_id) % len(self.table)
        bucket_list = self.table[bucket]
 
        # search for the package_id in the bucket list
        for kv in bucket_list:
          if kv[0] == package_id:
            return kv[1] # target package
        return None
 
    # Removes an item with matching key from the hash table.
    def remove(self, package_id:int):
        bucket = hash(package_id) % len(self.table)
        bucket_list = self.table[bucket]
 
        # remove the item from the bucket list if it is present.
        for kv in bucket_list:
          if kv[0] == package_id:
              bucket_list.remove([kv[0],kv[1]])
    
    def get_special_notes_list(self):
        return self.special_notes_list
 
    def set_special_notes_list(self,value):
        self.special_notes_list=value