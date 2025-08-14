# Email template cases

import pyperclip
import re
from folder_suggester import suggest_folder

def get_email_template(case, **kwargs):
    """Return the email template for the given case."""
    templates = {
        'refunds': f"""Dear {kwargs.get('name', 'Customer')},
In order for us to review and process your refund request, please submit a Student Refund Application request via our ServiceNow portal.
Once submitted, please keep a note of your ticket number as this will allow you to track the progress of your request.
""",
        'deposit': f"""Dear {kwargs.get('name', 'Customer')},
Thank you for your deposit. If you have any questions, please let us know.
""",
        'receipts': f"""Dear {kwargs.get('name', 'Customer')},
We have received your payment query. Our team will review and respond shortly.
""",
        'instalments': f"""Dear {kwargs.get('name', 'Customer')},
Please provide details regarding your instalment request.
""",
        'advance_billing': f"""Dear {kwargs.get('name', 'Customer')},
This is a reminder regarding your advance billing. Please let us know if you have any questions or concerns.
""",
        'confirmation_of_payment': f"""Dear {kwargs.get('name', 'Customer')},
We have received your payment of £{kwargs.get('amount', '0.00')}.
""",
        'payment_methods': f"""Dear {kwargs.get('name', 'Customer')},
Please confirm your preferred payment method so we can update our records accordingly.
""",
        'invoice_not_received': f"""Dear {kwargs.get('name', 'Customer')},
We have not yet received your invoice. Please send it at your earliest convenience so we can proceed.
""",
        'epd': f"""Dear {kwargs.get('name', 'Customer')},
Your EPD request has been received. We will process it and get back to you soon.
""",
        'unknown': f"""Dear {kwargs.get('name', 'Customer')},
Your request has been received. Please provide more details.
"""
    }
    email = templates.get(case, templates['unknown'])
    return re.sub(r'[\[\]\(\)\{\}]+\s*$', '', email.strip())

def main():
    cases = {
        '21': ('refunds', 'Refunds Request'),
        '22': ('deposit', 'Deposit'),
        '23': ('receipts', 'Send payment queries'),
        '24': ('instalments', 'Instalments'),
        '25': ('advance_billing', 'Advance Billing'),
        '26': ('confirmation_of_payment', 'Confirmation of Payment'),
        '27': ('payment_methods', 'Payment Methods'),
        '28': ('invoice_not_received', 'Invoice Not Received'),
        '29': ('unknown', '?'),
        '210': ('epd', 'EPD'),
        '9': ('exit', 'Exit'),
    }
    while True:
        print("Select a maintenance case:")
        for key, (_, desc) in cases.items():
            print(f"{key}. {desc}")
        choice = input("Enter the number of your choice: ").strip()
        if choice not in cases:
            print("Invalid selection.\n")
            continue
        case_key, case_desc = cases[choice]
        if case_key == 'exit':
            print("Exiting. Goodbye!")
            break
        kwargs = {}
        kwargs['name'] = input("Recipient name: ")
        if case_key == 'confirmation_of_payment':
            kwargs['amount'] = input("Amount: ")
        print("\nGenerated Email:\n")
        email_body = get_email_template(case_key, **kwargs)
        # Remove all typ6es of brackets globally
        for bracket in ['(', ')', '[', ']', '{', '}']:
            email_body = email_body.replace(bracket, '')
        print(email_body)
        pyperclip.copy(email_body)
        print("\n(The email body has been copied to your clipboard.)\n")
        folder = suggest_folder(email_body)
        print(f"Suggested folder: {folder}\n")

# Example usage:
if __name__ == "__main__":
    main()