from datetime import datetime

def calculate_discount(amount, payment_date_str, threshold_date_str):
    """
    Calculate 1.5% discount if payment is before the threshold date.
    Args:
        amount (float): The invoice amount.
        payment_date_str (str): Payment date in YYYY-MM-DD format.
        threshold_date_str (str): Threshold date in YYYY-MM-DD format.
    Returns:
        tuple: (discount_applied (bool), discount_amount (float), total_after_discount (float))
    """
    payment_date = datetime.strptime(payment_date_str, "%Y-%m-%d")
    threshold_date = datetime.strptime(threshold_date_str, "%Y-%m-%d")
    if payment_date < threshold_date:
        discount = round(amount * 0.015, 2)
        total = round(amount - discount, 2)
        return True, discount, total
    else:
        return False, 0.0, amount

if __name__ == "__main__":
    while True:
        print("\nSelect an option:")
        print("1. Calculate 1.5% discount (amount only)")
        print("2. Calculate discount with dates (advanced)")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            try:
                amount_str = input("Enter invoice amount (£): ")
                cleaned_amount = amount_str.replace('£', '').replace(',', '').strip()
                amount = float(cleaned_amount)
                discount = round(amount * 0.015, 2)
                total = round(amount - discount, 2)
                print(f"Discount: £{discount}\nTotal after discount: £{total}")
            except Exception as e:
                print(f"Error: {e}")
        elif choice == '2':
            try:
                amount_str = input("Enter invoice amount (£): ")
                cleaned_amount = amount_str.replace('£', '').replace(',', '').strip()
                amount = float(cleaned_amount)
                payment_date = input("Enter payment date (YYYY-MM-DD): ")
                threshold_date = input("Enter discount threshold date (YYYY-MM-DD): ")
                applied, discount, total = calculate_discount(amount, payment_date, threshold_date)
                if applied:
                    print(f"Discount applied: £{discount}\nTotal after discount: £{total}")
                else:
                    print("No discount applied. Payment was not before the threshold date.")
            except Exception as e:
                print(f"Error: {e}")
        elif choice == '3':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")
