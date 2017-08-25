import csv
from datetime import datetime


def parse_date(string_day, string_time):
    return datetime.strptime('19-Aug-2017 19:33', '%d-%b-%Y %H:%M')


def calculate_duration():
    return 0

def parse_csv(filename):
    result = []
    with open(filename) as csvfile:
        next(csvfile)
        csvfile
        reader = csv.DictReader(csvfile)
        for row in reader:
            result.append(row)
            print(row['Date'], row['Start Time'])

if __name__ == '__main__':
    FILENAME = "test-data/input.csv"
    parse_csv(FILENAME)

