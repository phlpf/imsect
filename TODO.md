# TODO/Spec List

## minimum viable product

- [x] have bot up and running  
- [x] have easy to access backend  
    - Hopefully, one you can view and edit through other means than the bot  
        - current thoughts: Google Sheets. csv files stored on accesible server  
            - Google Sheets: Useful, but then i'd have 2 api's running, which could get cumbersome  
            - CSV files: probably will be used as a backup at least, but might be hard to format for slack   
        - SQL could be used, but has a steep learning curve
        - **For MVP, we will use CSV**
- [x] figure out what values we need. add them to README  
    - what should be the identifier? name or serial number?
        - serial number is more exact, but name is easier
    - `values` (so far):
        - database number (given by database for management)
        - name (important)
        - in house part number (important)
        - name of person currently in possesion (important)
        - location (drawer)
        - supplier
        - date added (automatic)
        - type of part (description)
        - quantity
        - project (optional)
        - serial number (optional)
    - [x] Idea: use a JSON file to denote the format of the values, telling what values you have and what key should be used to call them
- [x] have command to add items  
    - [x] what do we do if someone adds a duplicate item?
    - [x] automatic time added (possibly through the JSON file)
    - [x] add optional values
- [x] have command to remove items  
    - [x] command to remove only some of high quantity items (e.g. screws)  
    - [ ] **\*FUTURE GOAL\*** make sure only permitted individuals are removing items  
- [x] have command to 'checkout' items  
    - [x] add 'uncheckout'
        - what should the name be?
            - uncheckout?
    - should you be able to 'checkout' multiple items at a time?  
    - how do we checkout high quantity items (e.g. screws)?  
        - quantity taken out after name?  
            - should even singular items have this?  
        - how about if multiple people take out high quantity items?
            - for now, assume they wont take out high quantity items, but just remove them  
- [x] command to look at all items
    - [x] basic search (for `type of part`)
        - [ ] **\*FUTURE GOAL\*** other types of arguements:
            - all values (see `values`)
    - [ ] **\*FUTURE GOAL\*** sorting
- [x] have clean and documented code

## future goals

- [x] get rid of ugly "explanation row", replace it with format.json
    - [ ] get rid of hard-coded indices
- [ ] be able to only show important values
    - multiple list options?
        - `holders` option
        - `quantity` option
            - only show high quantity items
        - `type of part` option
- [ ] have the ability to set reminder to return item. put this on database sheet.  
    - should it be `<amount of time borrowing>` or `<returning on date>`  
        - e.g. `10h10m` or `9/10/20-5:30`  
- [ ] have the ability to remind what items to take, especially before competition

## possible goals

- [ ] 'to buy' list  
    - separate list, or another value?  
