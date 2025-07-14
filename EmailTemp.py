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
    elif case == 'signiture':
        return f"""
        Best regards,
        Santiago 
        """
    
    elif case == 'refunds_request':
        return f"""
        Dear {kwargs.get('name', 'Customer')},
        In order for us to review and process your refund request, please submit a Student Refund Application request via our ServiceNow portal.
        Once submitted, please keep a note of your ticket number as this will allow you to track the progress of your request.

        Kind regards 

        Santiago
        """ 
    elif case == 'cid':
        return f"""

        Dear {kwargs.get('name', 'Customer')},
        Please provide your CID number for further assistance.
        

        Best regards,
        Santiago 
        """
    elif case == 'invoice_not_received':
        return f"""
        Dear {kwargs.get('name', 'Customer')},
        
        We have not yet received your invoice. Please send it at your earliest convenience so we can proceed.
        
        Best regards,
        Santiago 
        """
    elif case == 'advance_billing':
        return f"""
        Dear {kwargs.get('name', 'Customer')},
        
        This is a reminder regarding your advance billing. Please let us know if you have any questions or concerns.
        
        Best regards,
        Santiago 
        """
    elif case == 'payment_method':
        return f"""
        Dear {kwargs.get('name', 'Customer')},
        
        Please confirm your preferred payment method so we can update our records accordingly.
        
        Best regards,
        Santiago 
        """
    elif case == 'cas':
        return f"""You need to raise a request for instalment using Imperials AskNow portal. Once you submit we will be able to determinate if you eligible or not for it. 

Kind regards 

Santiago 
"""
    else:
        return "Invalid case."

def main():
    cases = {
        '1': ('confirmation_of_payment', 'Confirmation of Payment'),
        '2': ('additional_info', 'Additional Information Required'),
        '21': ('refunds_request', 'Refunds Request '),
        '3': ('redirect_department', 'Redirect to Another Department'),
        # Add more cases as needed, e.g. from your menu structure
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
            kwargs['name'] = input("Recipient name: ")
            kwargs['department'] = input("Department: ")
        # Add prompts for other cases as needed
        else:
            kwargs['name'] = input("Recipient name: ")
        print("\nGenerated Email:\n")
        email_body = get_email_template(case_key, **kwargs)
        print(email_body)
        pyperclip.copy(email_body)
        print("\n(The email body has been copied to your clipboard.)\n")

# Example usage:
if __name__ == "__main__":
    main()