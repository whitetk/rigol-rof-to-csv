# https://docs.python.org/3/library/struct.html

import sys
import struct
import csv

def usage():
    print("Usage: python3 " + sys.argv[0] + " [<ROF_filename>] " + "[<CSV_filename>]\n")


if sys.argv[1] == '-h' or sys.argv[1] == '--help':
    usage()
    exit()

file_ROF_name = sys.argv[1]
file_CSV_name = sys.argv[2]

with open(file_ROF_name, mode='rb') as file_ROF:
    print("Reading: " + file_ROF_name)
    file_ROF_content = file_ROF.read()
    file_ROF_header = struct.unpack("<cccccchIhhIII", file_ROF_content[:28])
    sample_period = file_ROF_header[10]
    num_samples = file_ROF_header[11]
    print("Sample period: " + str(sample_period))
    print("Number of samples: " + str(num_samples))
    print("Timespan: " + str(num_samples * sample_period) + " seconds")
    file_ROF_data = struct.unpack("<" + ("ii" * num_samples), file_ROF_content[28:])

with open(file_CSV_name, mode='w') as file_CSV:
    print("Writing: " + file_CSV_name)
    file_CSV_writer = csv.writer(file_CSV)
    file_CSV_header = ('volt','cur')
    print(file_CSV_header)
    file_CSV_writer.writerow(file_CSV_header)
    count = 0
    for i in range(len(file_ROF_data)):
        if i % 2 == 0:
            count = count + 1
            data_row = (file_ROF_data[i]/10000, file_ROF_data[i+1]/10000)
            print(data_row)
            file_CSV_writer.writerow(data_row)