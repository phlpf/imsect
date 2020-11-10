import csv
import json
import datetime
import sheets_api_handler
#import csv_formatter as csvf

def get_current_date():
    return datetime.date.today()

class ItemDatabase:
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
        # Get important indexes
        self.date_key = self.format_data["automatic_date_index"]
        self.optional_start = self.format_data["optional_start"] - \
            (1 if self.date_key<self.format_data["optional_start"] and self.date_key>=0 else 0)
        self.identifier_index = self.format_data["identifier_index"]
        self.count_index = self.format_data["count_index"]
        self.name_index = self.format_data["name_index"]

        self.amount_of_keys = self.format_data["amount_of_keys"]

        # Get explanation row
        full_names = []
        for i in range (0,self.amount_of_keys):
            full_names.append(self.format_data["explanation_row"][str(i)])
        self.explanation_row =  '*' + (' | '.join(full_names)) + '*'

        self.sh = sheets_api_handler.SheetHandler()
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
        added_row = [str(int(self.contents[-1][0])+1)] + added_row
        
        # Add date if we need to
        if(self.date_key != -1):
            added_row.insert(self.date_key, str(get_current_date()))
        
        # Make sure we have enough data
        if len(added_row) < self.optional_start:
            print("Not enough data. Skipping")
            return None

        # Add optional data if it's not there
        if len(added_row) < self.format_data["amount_of_keys"] and len(added_row) >= self.optional_start:
            for _ in range(len(added_row), self.format_data["amount_of_keys"]-1):
                added_row.append('N/A')
        
        #Add this as holder by default
        added_row.append('N/A')
        # Add the row
        self.contents.append(added_row)
        # Return the row with all changes we made
        return added_row
    
    # Remove an amount of an item
    def remove_from_item(self, index, amount):
        # Get our length, accounting for the explanation row
        size_of_contents = len(self.contents) 
        
        # If our index is bigger than it, it's a bad index
        if index >= size_of_contents:
            print("Someone removed a bad index!")
            return None
        
        removed_row, absolute_index = self.get_item(str(index))

        # We can't remove that much!
        if amount > int(self.contents[absolute_index][self.count_index]):
            print("Someone removed a bad!")
            return None
        
        # Replace the old amount with the new amount
        self.contents[absolute_index][self.count_index] = str(int(self.contents[absolute_index][self.count_index])-amount) 
        return removed_row

    # Remove an item
    def remove_item(self, index):
        # Get our length, accounting for the explanation row
        size_of_contents = len(self.contents)  
        
        # If our index is bigger than it, it's a bad index
        if index >= size_of_contents:
            print("Someone removed a bad index!")
            return None
        
        # Get the row to remove and it's index 
        removed_row, absolute_index = self.get_item(str(index))
        
        # Copy contents into new contents to do work on data, remove row
        new_contents = self.contents[:]
        new_contents.pop(absolute_index)
        
        # Change indexes for rows after it
        for i in range(absolute_index, size_of_contents):
            new_contents[i][self.identifier_index] = str(int(new_contents[i][self.identifier_index])-1)
        
        # Update contents
        self.contents = new_contents[:]
        return removed_row

    def checkout_item(self, index, new_holder, needed_holder="N/A"):
        # Get our length, accounting for the explanation row
        size_of_contents = len(self.contents) 
        
        # If our index is bigger than it, it's a bad index
        if index >= size_of_contents:
            print("Someone checked out a bad index!")
            return None
        
        # Get row and index
        checkedout_row, absolute_index = self.get_item(str(index))

        # Change holder value, assumed to be last
        # needed_holder is so that we know who has it
        if checkedout_row[-1] == needed_holder:
            self.contents[absolute_index][-1] = new_holder
        else:
            return None
        
        return checkedout_row
    # Search for specific attributes
    def search_for(self, term, index=-1):
        # deal with default
        if index < 0:
            index = self.name_index
        
        term = term.lower()
        matches = []
        for row in self.contents:
            if term in row[index].lower():
                matches.append(row[:])
        
        return matches
    # Read from a google sheet
    def read_from_sheet(self):
        self.contents = self.sh.read()
        return self.contents
    # Save our file
    def save(self):
        with open(self.filename, 'w') as csvfile:
            
            for row in self.contents:
                # Save each datapoint individually
                for i in range(len(row)):
                    csvfile.write((self.deliminator if not i == 0 else '') + str(row[i]))

                csvfile.write('\n')
        self.sh.write(self.contents, sheets_api_handler.data_to_range(self.contents))
# Test our functions
if __name__ == '__main__':
    test = ItemDatabase('database.csv')
    print(test.get_item('x'))
    print(test.contents)
    print(test.explanation_row)
 