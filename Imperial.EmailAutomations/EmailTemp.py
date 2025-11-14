# Email template cases

import pyperclip
import re
from folder_suggester import suggest_folder

def get_email_template(case, **kwargs):
    """Return the email template for the given case."""
    # support 'yes'/'no' strings, True/False booleans or None
    sponsor_raw = kwargs.get('sponsor', None)
    if isinstance(sponsor_raw, bool):
        sponsor = 'yes' if sponsor_raw else 'no'
    elif isinstance(sponsor_raw, str):
        sponsor = sponsor_raw.strip().lower()
    else:
        sponsor = ''
    templates = {
        # General information about instalments (no calculation)
        'instalments_info': f"""Dear  {kwargs.get('name', 'Customer')},
You will need to raise a request using:
Payment in instalments | Study | Imperial College London
https://www.imperial.ac.uk/study/fees-and-funding/tuition-fees/payment-terms/instalments/

No additional charges will be applied for paying by instalments, however, please note that if you do not pay an instalment by the due date, you might face late payment fees.

In general, we will have the 1st instalment on Oct/Nov 2025 and the  2nd instalment  on 5th of January 2026 (Dates may vary depending on your course start date ).
""",
        # Calculation for instalments WITHOUT sponsor
        'instalments_no_sponsor': f"""Dear  {kwargs.get('name', 'Customer')},
To request to pay in instalments, please visit: Payment in instalments | Study | Imperial College London
https://www.imperial.ac.uk/study/fees-and-funding/tuition-fees/payment-terms/instalments/ and raise a ticket.


In general, we will have the 1st instalment on 1st  Oct/Nov 2025 and the 2nd instalment  on 5th of January 2026 (Dates may vary depending on your course start date ). 
""",
        # Calculation for instalments WITH sponsor
        'instalments_with_sponsor': f"""Dear  {kwargs.get('name', 'Customer')},
To request to pay in instalments, please visit: Payment in instalments | Study | Imperial College London
https://www.imperial.ac.uk/study/fees-and-funding/tuition-fees/payment-terms/instalments/ and raise a ticket.

In general, we will have the 1st instalment on 1st  Oct/Nov 2025 and the  2nd instalment  on 5th of January 2026 (Dates may vary depending on your course start date ). 
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
We have received your payment of £{kwargs.get('amount', '0.00')}. Thank you for your payment.
If you would like a receipt please contact studentpay.queries@imperial.ac.uk

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

def clean_amount_input(prompt):
    raw = input(prompt)
    # Remove commas, spaces, and parentheses
    cleaned = raw.replace(',', '').replace('(', '').replace(')', '').replace(' ', '')
    try:
        return float(cleaned)
    except ValueError:
        print("Invalid amount. Please enter a valid number.")
        return clean_amount_input(prompt)

def calculate_instalments(total, deposit_paid, sponsor, sponsorship=None):
    """Calculate instalments and return formatted calculation text.
    deposit_paid may be 'y'/'n' or boolean; sponsor may be 'y'/'n' or boolean.
    sponsorship should be numeric (0.0 default).
    """
    # normalize flags (accept 'y'/'n' or True/False)
    if isinstance(deposit_paid, bool):
        deposit_flag = 'y' if deposit_paid else 'n'
    else:
        deposit_flag = str(deposit_paid).strip().lower()
    if isinstance(sponsor, bool):
        sponsor_flag = 'y' if sponsor else 'n'
    else:
        sponsor_flag = str(sponsor).strip().lower()

    deposit = total * 0.10 if deposit_flag == 'y' else 0.0
    deposit_status = "(Paid)" if deposit_flag == 'y' else "(Not Paid)"
    
    if sponsor_flag == 'y':
        net_total = total - sponsorship
        first_instalment = net_total * 0.5 - deposit
        second_instalment = net_total * 0.5
        remaining_after_first = net_total - first_instalment - deposit
        remaining_after_second = net_total - first_instalment - second_instalment - deposit
        deposit_line = f"Deposit: £{deposit:,.2f} {deposit_status}\n" if deposit != 0.0 else ""
        calc_text = (
            f"\nTuition calculation breakdown:\n"
            f"Total: £{total:,.2f}\n"
            f"Sponsorship: £{sponsorship:,.2f}\n"
            f"{deposit_line}"
            f"1st instalment: £{first_instalment:,.2f} (£{remaining_after_first:,.2f} due after payment)\n"
            f"2nd instalment: £{second_instalment:,.2f} (£{remaining_after_second:,.2f} due after payment)\n"
        )
    else:
        first_instalment = total * 0.5 - deposit
        second_instalment = total * 0.5
        remaining_after_first = total - first_instalment - deposit
        remaining_after_second = total - first_instalment - second_instalment - deposit
        deposit_line = f"Deposit: £{deposit:,.2f} {deposit_status}\n" if deposit != 0.0 else ""
        calc_text = (
            f"\nTuition calculation breakdown:\n"
            f"Total: £{total:,.2f}\n"
            f"{deposit_line}"
            f"1st instalment: £{first_instalment:,.2f} (£{remaining_after_first:,.2f} due after payment)\n"
            f"2nd instalment: £{second_instalment:,.2f} (£{remaining_after_second:,.2f} due after payment)\n"
        )
    return calc_text

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
            calc = input("Would you like to calculate the instalments? (y/n): ").strip().lower()
            if calc == 'y':
                total = clean_amount_input("Enter the total amount: ")
                deposit_paid = input("Has a deposit been paid? (y/n): ").strip().lower()
                sponsor = input("Is there a sponsor? (y/n): ").strip().lower()
                if sponsor == 'y':
                    sponsorship = clean_amount_input("Enter sponsorship amount: ")
                    kwargs['calc_text'] = calculate_instalments(total, deposit_paid, sponsor, sponsorship)
                else:
                    kwargs['calc_text'] = calculate_instalments(total, deposit_paid, sponsor)
            else:
                kwargs['calc_text'] = ""

        elif case_key == 'instalments_approved':
            calc = input("Would you like to include the calculation? (y/n): ").strip().lower()
            if calc == 'y':
                total = clean_amount_input("Enter the total amount: ")
                deposit_paid = input("Has a deposit been paid? (y/n): ").strip().lower()
                sponsor = input("Is there a sponsor? (y/n): ").strip().lower()
                if sponsor == 'y':
                    sponsorship = clean_amount_input("Enter sponsorship amount: ")
                    kwargs['calc_text'] = calculate_instalments(total, deposit_paid, sponsor, sponsorship)
                else:
                    kwargs['calc_text'] = calculate_instalments(total, deposit_paid, sponsor)
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