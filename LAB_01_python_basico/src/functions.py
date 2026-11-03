import csv
from math import inf
from pathlib import Path
import gzip



def load_data():
    data_path = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"

    with gzip.open(data_path, 'rt') as file:
        my_reader = csv.reader(file, delimiter='	')
        data = [row for row in my_reader]
    return data



def extract_column(index, data):
    column = []
    for row in data:
        column.append(row[index])
    return column


def column_mapper_1(column):
    letters = []
    for letter in column:
        letters.append((letter, 1))

    return letters

def column_mapper_2(column_1, column_2):
    letters = []
    for cell_index in range(len(column_1)):
        letters.append((column_1[cell_index], int(column_2[cell_index])))

    return letters
    
def column_mapper_3(column_1, column_2):
    numbers = []
    for cell_index in range(len(column_1)):
        numbers.append((int(column_1[cell_index]), column_2[cell_index]))
    
    return numbers


def shuffle_and_sort(sequence):
    """Shuffle and Sort"""
    return sorted(sequence, key = lambda x:x[0])

def reducer(sequence, return_dict = False):
    """Reducer"""
    result  = {}
    for key, value in sequence:
        if not key in result:
            result[key] = 0
        result[key] += value

    if return_dict:
        return result
    else:
        return list(result.items())

def reducer_2(sequence):
    """Reducer"""
    result  = {}
    for key, value in sequence:
        if not key in result:
            result[key] = []
        
        result[key].append(value)

    return list(result.items())

def reducer_3(sequence):
    """Reducer"""
    result  = {}
    for key, value in sequence:
        if not key in result:
            result[key] = [value]
        elif value not in result[key]:
            result[key].append(value)

    return [(key, sorted(lista)) for key, lista in list(result.items())]

def max_min_reducer(sequence, reversed = False):
    result  = {}
    for key, value in sequence:
        if not key in result:
            result[key] = [value, value]
        elif value < result[key][1]:
            result[key][1] = value
        elif value > result[key][0]:
            result[key][0] = value

    if reversed:
        return [(key, value[1], value[0]) for key, value in list(result.items())]
    else:    
        return [(key, value[0], value[1]) for key, value in list(result.items())]



def parse_column(column, sep):
    parsed_column = []
    for cell in column:
        parsed_column.append(cell.split(sep))
    return parsed_column

def parse_to_one_column(column):
    new_column = []
    for cell in column:
        new_column.extend(cell)
    return new_column

def parse_to_one_column_with_value(main_column, value_column, new_type = int):
    new_column = []
    for cell_index in range(len(main_column)):
        new_column.extend([(letter, new_type(value_column[cell_index])) for letter in main_column[cell_index]])
    return new_column

def extract_multiple_columns(indexes, data):
    columns = []
    for index in indexes:
        columns.append(extract_column(index, data))

    return tuple(columns)

def format_for_question_12(sequence):
    columns = []
    for cell in sequence:
        columns.append((cell[1], int(cell[0].split(":")[1])))
    return columns