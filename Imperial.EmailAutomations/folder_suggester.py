def suggest_folder(email_body):
    """Suggest a folder based on the email content."""
    body = email_body.lower()
    if "payment" in body:
        return "Payments"
    elif "refund" in body:
        return "Refunds"
    elif "invoice" in body:
        return "Invoices"
    elif "advance billing" in body:
        return "Advance Billing"
    elif "instalment" in body:
        return "Instalments"
    elif "epd" in body:
        return "EPD"
    else:
        return "General"