def invoice_total(items):
    return sum(i["price"] for i in items)
