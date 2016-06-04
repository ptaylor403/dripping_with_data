from datetime import datetime
import csv
import unicodedata
import fileinput

#used to convert SQL datetime format to Postgres
postgres_date_format = '%Y-%m-%d %H:%M:%S.%f'
# path = '/Users/Nic/TIY/customer-dtna/data/emp+item+punch.csv'
path2 = '/Users/Nic/TIY/customer-dtna/data/Direct_Run.csv'
path3 = '/Users/Nic/TIY/customer-dtna/data/temp.txt'


def read_csv_generator(path, headers=True):
    """
    csv file generator. Will return generator. Example usage:

    for idx, row in enumerate(read_csv_generator(path)):
    if idx > 10: break
    print(row)

    :param path: file path for the csv
    :param headers: if the csv has headers or is straight file
    :return: returns a generator of the csv file
    """
    if headers == True:
        with open(path, 'rU') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                yield row
    else:
        with open(path, 'rU') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                yield row


def process_date(date_string):
    """
    handles the SQL Dates and converts them Postgres SQL
    by converting a string into a date object and returning the default
    Postgres dateformat.

    :param date_string: takes in a date as a string
    :return:
    """
    if date_string == "NULL":
        return None
    else:
        date_object = datetime.strptime(date_string, postgres_date_format)
        return date_object.strftime('%Y-%m-%d %H:%M:%S')
