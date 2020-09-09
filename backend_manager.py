import csv
import json
import datetime
#import csv_formatter as csvf

def get_current_date():
    return datetime.date.today()

class item_database:
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
        self.date_key = self.format_data["automatic_date_index"]
        self.optional_start = self.format_data["optional_start"] - \
            (1 if self.date_key<self.format_data["optional_start"] and self.date_key>=0 else 0)
        self.has_explanation_row = self.format_data["has_explanation_row"]
        self.identifier_index = self.format_data["identifier_index"]
    # get a specific item
    def get_item(self, item):
        for i in range(len(self.contents)):
            if self.contents[i][self.identifier_index] == item:
                return self.contents[i], i

    # Add a row to our list 
    def add_item(self, row):
        # Copy data to different address
        added_row = row[:]
        
        # Add part number
        added_row = [str(len(self.contents))] + added_row
        
        # Add date if we need to
        if(self.date_key != -1):
            added_row.insert(self.date_key, str(get_current_date()))
        
        # Make sure we have enough data
        if len(added_row) < self.optional_start:
            print("Not enough data. Skipping")
            return None

        # Add optional data if it's not there
        if len(added_row) < self.format_data["amount_of_keys"] and len(added_row) >= self.optional_start:
            for _ in range(len(added_row), self.format_data["amount_of_keys"]):
                added_row.append('N/A')
        
        # Add the row
        self.contents.append(added_row)
        added_row.append('N/A')
        # Return the row with all changes we made
        return added_row
    
    # Remove an item
    def remove_item(self, index):
        size_of_contents = len(self.contents) - (1 if self.has_explanation_row else 0) 
        if index >= size_of_contents:
            print("Someone removed a bad index!")
            return None
        removed_row, absolute_index = self.get_item(str(index))
        new_contents = self.contents[:]
        new_contents.pop(absolute_index)
        for i in range(absolute_index, size_of_contents):
            new_contents[i][self.identifier_index] = str(int(new_contents[i][self.identifier_index])-1)
        self.contents = new_contents[:]
        return removed_row

    def checkout_item(self, index, new_holder, needed_holder="N/A"):
        size_of_contents = len(self.contents) - (1 if self.has_explanation_row else 0) 
        if index >= size_of_contents:
            print("Someone checked out a bad index!")
            return None
        checkedout_row, absolute_index = self.get_item(str(index))

        if checkedout_row[-1] == needed_holder:
            self.contents[absolute_index][-1] = new_holder
        else:
            return None
        
        return checkedout_row

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
    test = item_database('test.csv')
    print(test.get_item('x'))
    print(test.get_item('row 2'))
    test.save()
    print(str(get_current_date()), type(str(get_current_date())))