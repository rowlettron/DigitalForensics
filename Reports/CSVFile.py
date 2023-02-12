import csv

person = [['SN', 'Person', 'DOB'],
['1', 'John', '01/18/1997'],
['2', 'Marie','03/09/1998'],
['3', 'Simon','03/20/1999'],
['4', 'Erik', '04/21/2000'],
['5', 'Ana', '05/22/2001']]

csv.register_dialect('myDialect', quoting=csv.QUOTE_ALL, skipinitialspace=True)

with open('person1.csv', 'w', newline = '') as f:
    writer = csv.writer(f, dialect='myDialect')
    for row in person:
        writer.writerow(row)

f.close()

