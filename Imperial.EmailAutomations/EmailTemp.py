# Email template cases

import pyperclip
import re
from folder_suggester import suggest_folder

def get_email_template(case, **kwargs):
    """Return the email template for the given case."""
    sponsor = kwargs.get('sponsor', '').strip().lower()
    templates = {
        # General information about instalments (no calculation)
        'instalments_info': f"""Dear  {kwargs.get('name', 'Customer')},
You will need to raise a request using:
Payment in instalments | Study | Imperial College London
https://www.imperial.ac.uk/study/fees-and-funding/tuition-fees/payment-terms/instalments/

In general, we will have the 1st instalment on 1st Sep/Aug 2025 and 2nd on 5th of January 2026 (Dates may vary depending on your course start date ).
""",
        # Calculation for instalments WITHOUT sponsor
        'instalments_no_sponsor': f"""Dear  {kwargs.get('name', 'Customer')},
To request to pay in instalments, please visit: Payment in instalments | Study | Imperial College London
https://www.imperial.ac.uk/study/fees-and-funding/tuition-fees/payment-terms/instalments/ and raise a ticket.


In general, we will have the 1st instalment on 1st  Sep/Aug 2025 and 2nd on 5th of January 2026 (Dates may vary depending on your course start date ). 
""",
        # Calculation for instalments WITH sponsor
        'instalments_with_sponsor': f"""Dear  {kwargs.get('name', 'Customer')},
To request to pay in instalments, please visit: Payment in instalments | Study | Imperial College London
https://www.imperial.ac.uk/study/fees-and-funding/tuition-fees/payment-terms/instalments/ and raise a ticket.

In general, we will have the 1st instalment on 1st  Sep/Aug 2025 and 2nd on 5th of January 2026 (Dates may vary depending on your course start date ). 
""",
        'refunds': f"""Dear  {kwargs.get('name', 'Customer')},

In order for us to review and process your refund request, please submit a Student Refund Application https://servicemgt.service-now.com/ask?id=sc_cat_item&table=sc_cat_item&sys_id=0595da471b4146501533a8a4bd4bcb67 request via our ServiceNow portal.

Once submitted, please keep a note of your ticket number as this will allow you to track the progress of your request.
""",
        'deposit': f"""Dear  {kwargs.get('name', 'Customer')},
Thank you for your deposit. If you have any questions, please let us know.
""",
        'receipts': f"""Dear  {kwargs.get('name', 'Customer')},
We have received your payment query. Our team will review and respond shortly.
""",
        'advance_billing': f"""Dear  {kwargs.get('name', 'Customer')},
This is a reminder regarding your advance billing. Please let us know if you have any questions or concerns.
""",
        'confirmation_of_payment': f"""Dear  {kwargs.get('name', 'Customer')},
We have received your payment of £{kwargs.get('amount', '0.00')}.
""",
        'payment_methods': f"""Dear  {kwargs.get('name', 'Customer')},
Please confirm your preferred payment method so we can update our records accordingly.
""",
        'invoice_not_received': f"""Dear  {kwargs.get('name', 'Customer')},
We have not yet received your invoice. Please send it at your earliest convenience so we can proceed.
""",
        'epd': f"""Dear  {kwargs.get('name', 'Customer')},
Your EPD request has been received. We will process it and get back to you soon.
""",
        'unknown': f"""Dear  {kwargs.get('name', 'Customer')},
Your request has been received. Please provide more details.
""",
        'instalments_approved': f"""Dear  {kwargs.get('name', 'Customer')},

Your instalment plan request has been approved, please see the email below:

Thank you for your request to pay your 2025-26 tuition fees in instalments. I am pleased to confirm that this has now been actioned; 50% of the balance of your tuition fees is now due by the due date shown on your invoice, with the remaining 50% due by 5 January 2026. No new invoices will be generated.

The balance of your tuition fees is the 'Amount Due' quoted in the Payment Schedule section of your invoice email. To pay your instalments, please follow the payment instructions provided in the same email. For more information about available payment methods, please visit our How to Pay page (https://www.imperial.ac.uk/students/fees-and-funding/tuition-fees/payment-terms/how-to-pay/).
"""
    }

    # Select correct template for instalments
    if case == 'instalments':
        if sponsor == 'yes':
            email = templates['instalments_with_sponsor']
        elif sponsor == 'no':
            email = templates['instalments_no_sponsor']
        else:
            email = templates['instalments_info']
    else:
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
        '211': ('instalments_approved', 'Instalments Approved'),  
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
        if case_key == 'instalments':
            sponsor = input("Is there a sponsor? (y/n): ").strip().lower()
            if sponsor == 'y':
                kwargs['sponsor'] = 'yes'
            if sponsor == 'n':
                kwargs['sponsor'] = 'no'
            calc = input("Would you like to calculate the instalments? (y/n): ").strip().lower()
            if calc == 'y':
                total = float(input("Enter the total amount: "))
                deposit_paid = input("Has a deposit been paid? (y/n): ").strip().lower()
                if deposit_paid == 'y':
                    deposit = total * 0.10
                else:
                    deposit = 0.0
                if kwargs['sponsor'] == 'yes':
                    sponsorship = float(input("Enter sponsorship amount: "))
                    net_total = total - sponsorship
                    first_instalment = net_total * 0.5 - deposit
                    second_instalment = net_total * 0.5
                    deposit_line = f"Deposit: £{deposit:,.2f}\n" if deposit != 0.0 else ""
                    calc_text = (
                        f"\nCalculation:\n"
                        f"Total: £{total:,.2f}\n"
                        f"Sponsorship: £{sponsorship:,.2f}\n"
                        f"{deposit_line}"
                        f"1st instalment: £{first_instalment:,.2f}\n"
                        f"2nd instalment: £{second_instalment:,.2f}\n"
                    )
                else:
                    first_instalment = total * 0.5 - deposit
                    second_instalment = total * 0.5
                    deposit_line = f"Deposit: £{deposit:,.2f}\n" if deposit != 0.0 else ""
                    calc_text = (
                        f"\nCalculation:\n"
                        f"Total: £{total:,.2f}\n"
                        f"{deposit_line}"
                        f"1st instalment: £{first_instalment:,.2f}\n"
                        f"2nd instalment: £{second_instalment:,.2f}\n"
                    )
                kwargs['calc_text'] = calc_text
            else:
                kwargs['calc_text'] = ""
        elif case_key == 'instalments_approved':
            # Add calculation to approval confirmation if requested
            calc = input("Would you like to include the calculation? (y/n): ").strip().lower()
            if calc == 'y':
                sponsor = input("Is there a sponsor? (y/n): ").strip().lower()
                if sponsor == 'y':
                    sponsor_val = 'yes'
                else:
                    sponsor_val = 'no'
                total = float(input("Enter the total amount: "))
                deposit_paid = input("Has a deposit been paid? (y/n): ").strip().lower()
                if deposit_paid == 'y':
                    deposit = total * 0.10
                else:
                    deposit = 0.0
                if sponsor_val == 'yes':
                    sponsorship = float(input("Enter sponsorship amount: "))
                    net_total = total - sponsorship
                    first_instalment = net_total * 0.5 - deposit
                    second_instalment = net_total * 0.5
                    deposit_line = f"Deposit (10%): £{deposit:,.2f}\n" if deposit != 0.0 else ""
                    calc_text = (
                        f"\nCalculation:\n"
                        f"Total: £{total:,.2f}\n"
                        f"Sponsorship: £{sponsorship:,.2f}\n"
                        f"{deposit_line}"
                        f"1st instalment: £{first_instalment:,.2f}\n"
                        f"2nd instalment: £{second_instalment:,.2f}\n"
                    )
                else:
                    first_instalment = total * 0.5 - deposit
                    second_instalment = total * 0.5
                    deposit_line = f"Deposit (10%): £{deposit:,.2f}\n" if deposit != 0.0 else ""
                    calc_text = (
                        f"\nCalculation:\n"
                        f"Total: £{total:,.2f}\n"
                        f"{deposit_line}"
                        f"1st instalment: £{first_instalment:,.2f}\n"
                        f"2nd instalment: £{second_instalment:,.2f}\n"
                    )
                kwargs['calc_text'] = calc_text
            else:
                kwargs['calc_text'] = ""
        else:
            kwargs['calc_text'] = ""
        print("\nGenerated Email:\n")
        email_body = get_email_template(case_key, **kwargs)
        # Remove all typ6es of brackets globally
        for bracket in ['(', ')', '[', ']', '{', '}']:
            email_body = email_body.replace(bracket, '')
        # Add calculation if present
        if kwargs.get('calc_text'):
            email_body += kwargs['calc_text']
        print(email_body)
        pyperclip.copy(email_body)
        print("\n(The email body has been copied to your clipboard.)\n")
        folder = suggest_folder(email_body)
        print(f"Suggested folder: {folder}\n")

# Example usage:
if __name__ == "__main__":
    main()