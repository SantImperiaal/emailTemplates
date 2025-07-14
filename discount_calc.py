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
    try:
        amount = float(input("Enter invoice amount (£): "))
        payment_date = input("Enter payment date (YYYY-MM-DD): ")
        threshold_date = input("Enter discount threshold date (YYYY-MM-DD): ")
        applied, discount, total = calculate_discount(amount, payment_date, threshold_date)
        if applied:
            print(f"Discount applied: £{discount}\nTotal after discount: £{total}")
        else:
            print("No discount applied. Payment was not before the threshold date.")
    except Exception as e:
        print(f"Error: {e}")
