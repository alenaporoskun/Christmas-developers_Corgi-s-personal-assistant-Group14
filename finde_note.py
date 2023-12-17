# def fun_delete_contact(address_book):
#     # Видалення контакту з книги контактів
#     contact_name = input('Enter the name of contact you want to delete: ')
#     if contact_name in address_book.data:
#         question = input(
#             f'Are you sure you want to delete this contact {contact_name}? (yes or no): ')
#         if question == 'yes':
#             del address_book.data[contact_name]
#             print('Contact deleted')
#         else:
#             print('Deletion canceled')
#     else:
#         print(f'contact with thw name {contact_name} not found.')
