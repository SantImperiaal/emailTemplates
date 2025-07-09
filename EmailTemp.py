# Email template cases

import pyperclip

def get_email_template(case, **kwargs):
    if case == 'confirmation_of_payment':
        return f"""
        Dear {kwargs.get('name', 'Customer')},
        
        We have received your payment of £{kwargs.get('amount', '0.00')}.
        
        Best regards,
        Santiago
        """
    elif case == 'additional_info':
        return f"""
        Dear {kwargs.get('name', 'Customer')},
        
        We require some additional information to process your request: {kwargs.get('info_needed', 'N/A')}.
        Please reply to this email at your earliest convenience.
        
        Best regards,
        Santiago 
        """
    elif case == 'redirect_department':
        return f"""
        Dear {kwargs.get('name', 'Customer')},
        
        Your inquiry has been forwarded to our {kwargs.get('department', 'relevant')} department.
        They will contact you soon regarding your request.
        
        Best regards,
        Santiago 
        """
    else:
        return "Invalid case."

def main():
    cases = {
        '1': ('confirmation_of_payment', 'Confirmation of Payment'),
        '2': ('additional_info', 'Additional Information Required'),
        '3': ('redirect_department', 'Redirect to Another Department'),
        # Add more cases as needed, e.g. from your menu structure
        '4': ('invoice_not_received', 'Invoice Not Received'),
        '5': ('advance_billing', 'Advance Billing'),
        '6': ('payment_method', 'Payment Method'),
        # ... add more as needed ...
    }
    print("Select an email template case:")
    for key, (_, desc) in cases.items():
        print(f"{key}. {desc}")
    choice = input("Enter the number of your choice: ").strip()
    if choice not in cases:
        print("Invalid selection.")
        return
    case_key, case_desc = cases[choice]
    kwargs = {}
    if case_key == 'confirmation_of_payment':
        kwargs['name'] = input("Recipient name: ")
        kwargs['amount'] = input("Amount: ")
    elif case_key == 'additional_info':
        kwargs['name'] = input("Recipient name: ")
        kwargs['info_needed'] = input("Information needed: ")
    elif case_key == 'redirect_department':
        kwargs['name'] = input("Recipient name: ")
        kwargs['department'] = input("Department: ")
    # Add prompts for other cases as needed
    else:
        kwargs['name'] = input("Recipient name: ")
    print("\nGenerated Email:\n")
    email_body = get_email_template(case_key, **kwargs)
    print(email_body)
    pyperclip.copy(email_body)
    print("\n(The email body has been copied to your clipboard.)")

# Example usage:
if __name__ == "__main__":
    main()