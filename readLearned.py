import csv
with open('x.csv', 'rb') as f:
    reader = csv.reader(f)
    x_list = list(reader)
print x_list[33][8]

f.close()

with open('th.csv', 'rb') as f:
    reader = csv.reader(f)
    th_list = list(reader)
print th_list[33][8]
