import csv

def format_csv(filename):
    line_format = '|'
    with open(filename, newline='') as csvfile:
        contents = csv.reader(csvfile, quotechar='"')
        line_format = '|'
        biggest_elements = []
        for row in contents:
            for i in range(len(row)):
                if i >= len(biggest_elements):
                    biggest_elements.append(len(row[i]))
                    line_format += '{:%d}|'
                if len(row[i]) > biggest_elements[i]:
                    biggest_elements[i] = len(row[i])
        line_format = line_format%tuple(biggest_elements)
    formatted = ""
    with open(filename, newline='') as csvfile:
        contents = csv.reader(csvfile, quotechar='"')
        separator = ""
        for row in contents:
            formatted += '+' + '-'*(len(line_format.format(*row))-2) +'+' +'\n'
            separator = '+' + '-'*(len(line_format.format(*row))-2) +'+'
            formatted += line_format.format(*row) + '\n'
        formatted += separator
    return formatted

if __name__ == '__main__':
    print(format_csv('test.csv'))
