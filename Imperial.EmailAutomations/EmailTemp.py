# Email template cases

import pyperclip
import re

def get_email_template(case, **kwargs):
    def remove_trailing_brackets(text):
        # Remove any trailing brackets (of any type) and whitespace at the end of the email
        return re.sub(r'[\[\]\(\)\{\}]+\s*$', '', text.strip())

    if case == 'confirmation_of_payment':
        email = f"""Dear {kwargs.get('name', 'Customer')},

We have received your payment of £{kwargs.get('amount', '0.00')}.
"""
    elif case == 'additional_info':
        email = f"""Dear {kwargs.get('name', 'Customer')},

We require some additional information to process your request: {kwargs.get('info_needed', 'N/A')}.
Please reply to this email at your earliest convenience.
"""
    elif case == 'redirect_department':
        email = f"""Dear {kwargs.get('name', 'Customer')},

Your inquiry has been forwarded to our {kwargs.get('department', 'relevant')} department.
They will contact you soon regarding your request.
"""
    elif case == 'signiture':
        email = ""
    elif case == 'refunds_request':
        email = f"""Dear {kwargs.get('name', 'Customer')},
In order for us to review and process your refund request, please submit a Student Refund Application request via our ServiceNow portal.
Once submitted, please keep a note of your ticket number as this will allow you to track the progress of your request.
"""
    elif case == 'cid':
        email = f"""Dear {kwargs.get('name', 'Customer')},
Please provide your CID number for further assistance.
"""
    elif case == 'invoice_not_received':
        email = f"""Dear {kwargs.get('name', 'Customer')},

We have not yet received your invoice. Please send it at your earliest convenience so we can proceed.
"""
    elif case == 'advance_billing':
        email = f"""Dear {kwargs.get('name', 'Customer')},

This is a reminder regarding your advance billing. Please let us know if you have any questions or concerns.
"""
    elif case == 'payment_method':
        email = f"""Dear {kwargs.get('name', 'Customer')},

Please confirm your preferred payment method so we can update our records accordingly.
"""
    elif case == 'cas':
        email = f"""You need to raise a request for instalment using Imperials AskNow portal. Once you submit we will be able to determinate if you eligible or not for it.

Kind regards

Santiago"""
    else:
        return "Invalid case."
    return remove_trailing_brackets(email)

def main():
    cases = {
        '1': ('confirmation_of_payment', 'Confirmation of Payment'),
        '2': ('additional_info', 'Additional Information Required'),
        '21': ('refunds_request', 'Refunds Request '),
        '3': ('redirect_department', 'Redirect to Another Department'),
        '4': ('invoice_not_received', 'Invoice Not Received'),
        '5': ('advance_billing', 'Advance Billing'),
        '6': ('payment_method', 'Payment Method'),
        '7': ('signiture', 'Signiture'),
        '8': ('cid', 'Provide CID'),
        '87': ('forward_it', 'Forward Request to IT'),
        '88': ('cas', 'CAS Status Request'),
        '9': ('exit', 'Exit'),
    }
    while True:
        print("Select an email template case:")
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
        if case_key == 'confirmation_of_payment':
            kwargs['name'] = input("Recipient name: ")
            kwargs['amount'] = input("Amount: ")
        elif case_key == 'additional_info':
            kwargs['name'] = input("Recipient name: ")
            kwargs['info_needed'] = input("Information needed: ")
        elif case_key == 'redirect_department':
            kwargs['name'] = input("Re8cipient name: ")
            kwargs['department'] = input("Department: ")
        # Add prompts for other cases as needed
        else:
            kwargs['name'] = input("Recipient name: ")
        print("\nGenerated Email:\n")
        email_body = get_email_template(case_key, **kwargs)
        # Remove all types of brackets globally
        for bracket in ['(', ')', '[', ']', '{', '}']:
            email_body = email_body.replace(bracket, '')
        print(email_body)
        pyperclip.copy(email_body)
        print("\n(The email body has been copied to your clipboard.)\n")

# Example usage:
if __name__ == "__main__":
    main()