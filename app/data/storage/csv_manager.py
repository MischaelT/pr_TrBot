import csv
import numpy

from data.storage.storage_manager import storage_Manager


class Csv_manager(storage_Manager):

    def push_data(self, data, file_name):
        # self._validate(data)
        self._write(data, file_name)

    def _write(self, data, file_name):
        try:
            with open(f'{file_name}.csv', 'a') as file:
                writer = csv.writer(file)
                data_to_csv = []
                for element in data:
                    data_to_csv.append(element)
                writer.writerow(data_to_csv)
        except IOError:
            print("I/O error")  # noqa

    def _read(self):
        pass

    def clean_data(self, path):
        cleaned_data = []
        with open(path, 'r', newline='') as csvfile:
            data_reader = csv.reader(csvfile, delimiter=',')

            for row in data_reader:
                cleaned_data.append(numpy.double(row[3]))
        print(cleaned_data)
        return numpy.array(cleaned_data)
