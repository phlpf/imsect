import csv
import json
import datetime
#import csv_formatter as csvf

def get_current_date():
    return datetime.date.today()

class csv_file:
    def __init__(self, filename, deliminator=',', format_file="format.json"):
        self.filename = filename
        self.deliminator = deliminator #TODO: figure out how to use this
        
        try:
            with open(filename, newline='') as csvfile:
                # Open A file. Convert it to a list
                contents = csv.reader(csvfile, quotechar='"')
                self.contents = []
            
                for row in contents:
                    self.contents.append(row)
        
            with open(filename+'.old', 'w') as backup:
                # Save a backup, in case
                for row in self.contents:
            
                    for i in range(len(row)):
                        backup.write((self.deliminator if not i == 0 else '') + str(row[i]))
            
                    backup.write('\n')
        except FileNotFoundError:
            # Log that we don't have a file named that
            print("File Not Found. Will be created on exit")
            self.contents = []
        try:
            with open(format_file) as jsonfile:
                self.format_data = json.loads(jsonfile.read())
        except FileNotFoundError:
            print("The Format File (" + format_file + ") doesn't exist. Exiting")
            exit()
        self.date_key = self.format_data["automatic_date_key"]

    # get a specific item
    def get_item(self, item):
        for row in self.contents:
            if row[0] == item:
                return row

    # Add a row to our list 
    def add_item(self, row):
        added_row = row[:]
        
        if(self.date_key != -1):
            added_row.insert(self.date_key, str(get_current_date()))
        
        if len(added_row) < self.format_data["optional_start"]:
            print("Not enough keys. Skipping")
            return None

        if len(added_row) < self.format_data["amount_of_keys"] and len(added_row) >= self.format_data["optional_start"]:
            for i in range(len(added_row), self.format_data["amount_of_keys"]):
                added_row.append('N/A')
        
        added_row = [str(len(self.contents))] + added_row
        
        self.contents.append(added_row)
        return added_row
    # Save our file
    def save(self):
        with open(self.filename, 'w') as csvfile:
            
            for row in self.contents:
                # Save each datapoint individually
                for i in range(len(row)):
                    csvfile.write((self.deliminator if not i == 0 else '') + str(row[i]))

                csvfile.write('\n')

# Test our functions
if __name__ == '__main__':
    test = csv_file('test.csv')
    print(test.get_item('x'))
    print(test.get_item('row 2'))
    test.save()
    print(str(get_current_date()), type(str(get_current_date())))