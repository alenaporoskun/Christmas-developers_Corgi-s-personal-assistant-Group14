        elif words_commands[0] == 'search-contact':
            self.search_contact()


def search_contact(self):
    search_query = input("Enter search term: ")
    self.search(search_query)

def search(self, query):
    results = []
    suggestions = []

    try:
        int(query[0])
    except Exception:
        for name, record in self.data.items():
            if (
                query.casefold() in name.casefold() or
                any(query.casefold() in email.value.casefold() for email in record.emails) or
                (record.address and query.casefold() in record.address.value.casefold())
            ):
                results.append(record)
            elif name.casefold().startswith(query.casefold()):
                suggestions.append(name)
    else:
        for name, record in self.data.items():
            for phone in record.phones:
                if query.casefold() in phone.value.casefold():
                    results.append(record)

    if not results and not suggestions:
        print(f"Contact '{query}' not found. Phone number, address, and email were also not found.")
        # Возможные предложения на основе частичного совпадения
        if suggestions:
            print(f"Possible suggestions: {', '.join(suggestions)}")

    if results:
        print("Search results:")
        for result in results:
            print(result)
