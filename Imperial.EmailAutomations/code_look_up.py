from datetime import datetime

def edate(date, months):
    month = date.month - 1 + months
    year = date.year + month // 12
    month = month % 12 + 1
    day = min(date.day, [31,
        29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
        31,30,31,30,31,31,30,31,30,31][month-1])
    return datetime(year, month, day)

def get_instalment_date(d2):
    date_ranges = [
        (datetime(2026, 6, 15), datetime(2026, 10, 1)),
        (datetime(2026, 5, 15), datetime(2026, 9, 1)),
        (datetime(2026, 4, 15), datetime(2026, 8, 1)),
        (datetime(2026, 3, 15), datetime(2026, 7, 1)),
        (datetime(2026, 2, 15), datetime(2026, 6, 1)),
        (datetime(2026, 1, 15), datetime(2026, 5, 1)),
        (datetime(2025, 12, 15), datetime(2026, 4, 1)), 
        (datetime(2025, 11, 15), datetime(2026, 3, 1)),
        (datetime(2025, 10, 15), datetime(2026, 2, 1)),
        (datetime(2025, 8, 15), datetime(2026, 1, 5)),
    ]
    for cutoff, result in date_ranges:
        if d2 >= cutoff:
            return result
    return datetime(2025, 11, 1)

def main():
    print("Enter values for A2, B2, C2, D2, E2, F2")
    A2 = input("A2 (e.g. TFDE or student ID): ")
    B2 = datetime.strptime(input("B2 (Invoice Due Date YYYY-MM-DD): "), "%Y-%m-%d")
    C2 = datetime.strptime(input("C2 (Application Date YYYY-MM-DD): "), "%Y-%m-%d")
    D2 = input("D2 (e.g. 2026-27 Entrant or date YYYY-MM-DD): ")
    E2 = datetime.strptime(input("E2 (Study End Date YYYY-MM-DD): "), "%Y-%m-%d")
    F2 = datetime.strptime(input("F2 (Invoice Date YYYY-MM-DD): "), "%Y-%m-%d")

    if not A2 or not B2 or not C2 or not F2:
        print("")
        return

    if F2 > B2:
        print("Not eligible, invoice past due")
        return

    if E2 < edate(F2, 8):
        print("Not eligible - less than eight months study remaining")
        return

    if A2 == "TFDE":
        print("Instalments not available for deposit invoices")
        return

    if D2 == "2026-27 Entrant" or C2 > datetime(2026, 8, 29):
        print("Not eligible - 2026-27 entrant")
        return

    inst_date = get_instalment_date(datetime.strptime(D2, "%Y-%m-%d"))
    b_shifted = edate(B2, 4)
    e_shifted = edate(E2, -6)

    if inst_date > datetime(b_shifted.year, b_shifted.month, 1):
        if inst_date > datetime(e_shifted.year, e_shifted.month, 1):
            print("Option expired")
        else:
            print(f"Insts{inst_date.strftime('%b')}InstsPGR")
    else:
        print("Instalment schedule not found, consult Team Leader")

if __name__ == "__main__":
    main()
