from __future__ import print_function
import csv
import os
import sys


def write_csv(data, header, output_directory, name = None):
    if name == None:
        name = 'report1.csv'

    print("[+] Writing {} to {}".format(name, output_directory))

    with open(os.path.join(output_directory, name), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(data)

TEST_DATA_LIST = [["Ram", 32, "Bhopal", "Manager"], 
                  ["Raman", 42, "Indore", "Engg."],
                  ["Mohan", 25, "Chandigarh", "HR"], 
                  ["Parkash", 45, "Delhi", "IT"] ]

write_csv(TEST_DATA_LIST, ['Name','Age','City','Job Description'], os.getcwd()) 

