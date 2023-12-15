# Завдання  

У цьому домашньому завданні вам треба:  

* Додати функціонал збереження адресної книги на диск та відновлення з диска. Для цього ви можете вибрати будь-який зручний для вас протокол серіалізації/десеріалізації даних та реалізувати методи, які дозволять зберегти всі дані у файл і завантажити їх із файлу.   

* Додати користувачеві можливість пошуку вмісту книги контактів, щоб можна було знайти всю інформацію про одного або кількох користувачів за кількома цифрами номера телефону або літерами імені тощо.  

## Критерії прийому:  
* Програма не втрачає дані після виходу з програми та відновлює їх з файлу.    
* Програма виводить список користувачів, які мають в імені або номері телефону є збіги із введеним рядком.    
  
## Example of Output:

Add contacts...
  
book  
Contact name: John, phones: 1112223333; 5555555555, birthday: 2001-08-19  
Contact name: Jane, phones: 9876543210  
Contact name: Kol, phones: 1234567890  
Contact name: Anna, phones: 0667954896, birthday: 2003-02-24  
Contact name: Lily, phones: 0955739843, birthday: 2000-10-01  
  
Enter a name or phone number to search('exit' to finish): j  
Search results:  
Contact name: John, phones: 1112223333; 5555555555, birthday: 2001-08-19  
Contact name: Jane, phones: 9876543210  
 
Enter a name or phone number to search('exit' to finish): 066  
Search results:  
Contact name: Anna, phones: 0667954896, birthday: 2003-02-24  
  
Enter a name or phone number to search('exit' to finish): 843  
Search results:  
Contact name: Lily, phones: 0955739843, birthday: 2000-10-01  
  
Enter a name or phone number to search('exit' to finish): Li  
Search results:  
Contact name: Lily, phones: 0955739843, birthday: 2000-10-01  
  
Enter a name or phone number to search('exit' to finish): Bob  
No matching contacts found.  
  
Enter a name or phone number to search('exit' to finish): exit  
    
loaded_book  
Contact name: John, phones: 1112223333; 5555555555, birthday: 2001-08-19  
Contact name: Jane, phones: 9876543210  
Contact name: Kol, phones: 1234567890  
Contact name: Anna, phones: 0667954896, birthday: 2003-02-24  
Contact name: Lily, phones: 0955739843, birthday: 2000-10-01  
