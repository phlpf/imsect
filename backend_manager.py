import csv
#import csv_formatter as csvf

class csv_file:
    def __init__(self, filename, deliminator=','):
        self.filename = filename
        self.deliminator = deliminator
        try:
            with open(filename, newline='') as csvfile:
                contents = csv.reader(csvfile, quotechar='"')
                self.contents = []
                for row in contents:
                    self.contents.append(row)
        except FileNotFoundError:
            print("File Not Found. Will be created on exit")
            self.contents = []
            
    def get_item(self, item):
        for row in self.contents:
            if row[0] == item:
                return row
    def add_item(self, row):
        self.contents.append(row)
    #def format_items(self):
    #    return csvf.format_csv_list(self.contents)
    def save(self):
        with open(self.filename, 'w') as csvfile:
            for row in self.contents:
                for i in range(len(row)):
                    csvfile.write((self.deliminator if not i == 0 else '') + str(row[i]))
                csvfile.write('\n')

if __name__ == '__main__':
    test = csv_file('test.csv')
    print(test.get_item('x'))
    print(test.get_item('row 2'))
    test.save()