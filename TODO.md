# TODO/Spec List

## minimum viable product

- [x] 1. have bot up and running  
- [ ] have easy to access backend  
    - Hopefully, one you can view and edit through other means than the bot  
        - current thoughts: Google Sheets. csv files stored on accesible server  
            - Google Sheets: Useful, but then i'd have 2 api's running, which could get cumbersome  
            - CSV files: probably will be used as a backup at least, but might be hard to format for slack   
- [ ] figure out what values we need. add them to README  
    - what should be the identifier? name or serial number?
        - serial number is more exact, but name is easier
    - `values` (so far):
        - date added (automatic)
        - name of person currently in possesion
        - type of part
- [ ] have command to easily add items  
- [ ] have command to remove items  
- [ ] have command to 'checkout' items  
    - should you be able to 'checkout' multiple items?  
    - how do we checkout high quantity items (e.g. screws)?  
        - quantity taken out after name?  
            - should even singular items have this?  
        - how about if multiple people take out high quantity items?  
- [ ] command to look at all items
    - basic search (for `type of part`)
        - *\*FUTURE GOAL\** other types of arguements:
            - all values (see `values`)
    - *\*FUTURE GOAL\** sorting

## future goals

- [ ] have the ability to set reminder to return item. put this on database sheet.  
    - should it be `<amount of time borrowing>` or `<returning on date>`  
        - e.g. `10h10m` or `9/10/20-5:30`  

## possible goals

- [ ] 'to buy' list  
    - separate list, or another value?  
