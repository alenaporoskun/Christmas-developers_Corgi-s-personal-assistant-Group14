    def search(self, query):
    results = []
    try:
        int(query[0])
    except Exception:
        for name, record in self.data.items():
            if (
                query.lower() in name.lower()
                or any(query.lower() in email.value.lower() for email in record.emails)
                or (record.address and query.lower() in record.address.value.lower())
            ):
                results.append(record)
    else:
        for name, record in self.data.items():
            for phone in record.phones:
                if query.lower() in phone.value.lower():
                    results.append(record)

    if not results:
        print(f"Контакт з '{query}' не знайдено. Номер, адреса та email теж не знайдені.")
    
    return results


