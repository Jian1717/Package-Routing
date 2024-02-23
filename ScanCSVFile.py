#Mannuly save xmlx file as cvs file first. 

import csv
from datetime import *
from PackageHashTable import PackageHashTable
from Package import Package
from DistanceTable import DistanceTable

#loading data from CSV file and fill out distance table and addess dictionary 
def load_distance_table():
    #creating 2D array
    distance_table =[]
    address_dicitonary = {}
    
    with open('WGUPS Distance Table.csv','r') as distance_table_csv:
        #skip unwanted line
        next(distance_table_csv)
        next(distance_table_csv)
        next(distance_table_csv)
        next(distance_table_csv)
        next(distance_table_csv)
        next(distance_table_csv)
        next(distance_table_csv)
        next(distance_table_csv)
        next(distance_table_csv)
        reader = csv.reader(distance_table_csv,delimiter=',')
        #skip header
        next(reader)
        row_count=0
        for row in reader:
            #adding a dictionary data struction into list.  For quikcer data value search in later use in the program
            distance_table.append(dict())
            #starting index for distance in the row
            index=2
            while index < len(row)-1:
                #adding the distance to list
                if row[index] is not '':
                    try:
                        #creating dictionary key=postion index in the distance table, value = distance in between
                        distance_table[row_count][index-2]=row[index]
                    except ValueError:
                        pass
                #increament index by 1
                index += 1
            #adding modify address to dictionary and its corresponding row postion index in the distance table
            address_dicitonary[validate_address(row[0].split('\n')[1])]=row_count
            row_count +=1
    return DistanceTable(distance_table, address_dicitonary)
        
#loading data from CSV file and fill out package hashing table
def load_package_file():
    with open('WGUPS Package File.csv','r') as package_file_csv:
        #skip unwanted line
        next(package_file_csv)
        next(package_file_csv)
        next(package_file_csv)
        next(package_file_csv)
        next(package_file_csv)
        next(package_file_csv)
        next(package_file_csv)
        next(package_file_csv)
        reader = csv.reader(package_file_csv,delimiter=',')
        package_hashing_table = PackageHashTable()
        #skip the header
        next(reader)
        special_notes_list=[]
        #insert each package into package hashing table
        for row in reader:
            package_hashing_table.insert(row[0],Package(row[0],validate_address(row[1]),validate_time(row[5]),row[2],row[4],row[6],row[7],'in hub'))
            #adding package id to special_notes_list if it contain special notes
            if(row[7] is not None):
                special_notes_list.append(row[0])
        package_hashing_table.set_special_notes_list(special_notes_list)
        return package_hashing_table

#clean address data if it has west, east, south and north in it. And make address upper case
def validate_address (address:str):
    address=address.upper()
    if address.find('WEST')>-1:
        address=address.replace('WEST','W')
    if address.find('EAST')>-1:
        address=address.replace('EAST','E')
    if address.find('SOUTH')>-1:
        address=address.replace('SOUTH','S')    
    if address.find('NORTH')>-1:
        address=address.replace('NORTH','N')
    if address.find('STATION')>-1:
        address=address.replace('STATION','STA')
    #remove , from address
    if address.find(',')>-1:
        address=address.replace(',','')
    #remove leading space in address
    if address.startswith(' '):
        address=address[1:]
    return address

#transfer datetime in string format to datetime format. If deadline is EOD set time to 11.59 pm
def validate_time (time:str):
    if(time=='EOD'):
        #make the date current date
        return datetime.strptime(str(date.today())+' '+'11:59 PM','%Y-%m-%d %I:%M %p')
    return datetime.strptime(str(date.today())+' '+time,'%Y-%m-%d %I:%M %p')

    