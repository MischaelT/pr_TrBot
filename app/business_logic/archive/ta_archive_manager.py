import csv
import numpy


def clean_data(path):
    cleaned_data = []
    with open(path, 'r', newline='') as csvfile:
        data_reader = csv.reader(csvfile, delimiter=',')

        for row in data_reader:
            cleaned_data.append(numpy.double(row[3]))
    print(cleaned_data)
    return numpy.array(cleaned_data)
