# Christmas-developers_Santa-s-personal-assistant

## Team: Christmas Developers

## Project name: Mr. Corgi's personal assistant

* We have made a Python package and a console script from the personal assistant script that can be called anywhere in the system from the console with the **console-assistant** command. 
* To do this, we created a file and folder structure:

├── console_assistant  

│    ├── console_assistant 

│    │   ├── main.py   

│    │   ├── file_sorter.py 

│    │   └── __init__.py   

│    └── setup.py   

│    └── README.md  

│    └── README_ua.md  

* Next, the package is installed into the system with the command ```pip install -e .```(or ```pip install .```).
* After installation, the console_assistant package appears in the system.
* When the package is installed in the system, the script can be called anywhere from the console with 
```
console-assistant
``` 

A personal assistant was developed for Mr. Corgi. Mr. Corgi is Santa Claus's assistant. 
Because Mr.Corgi needs a program to help with his duties.
Mr. Corgi:  
- Responsible for the book of gift recipients:
1. adds, 
2. edits, 
3. deletes, 
4. searches for people in it.
- Saves and monitors the list of gift recipients' wishes.
- Can tell which of them has a birthday in a few days.
- Sorts files.

All the commands of our personal assistant for Mr. Corgi:
- add-contact [name]  - add contact [with it's name]
- edit-contact [name] - edit contact information [with it's name]
- delete-contact      - delete contact
- delete-phone        - delete phone from some contact
- show-contacts       - display all contacts in the address book
- upcoming-birthdays  - display a list of contacts whose birthday is a specified number of days from the current date
- search-contact      - search for contacts in the address book
- add-note            - add note with author if he/she is in the contact book
- show-notes          - show all notes with authors and tags
- search-notes        - search for a note by word or author
- edit-note           - edit a note
- delete-note         - delete note
- sort-files          - sort files in a directory 
- exit                - exit the Assistant
