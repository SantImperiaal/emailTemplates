from datetime import datetime
from dateutil.relativedelta import relativedelta

# Example data table for VLOOKUP/MATCH (replace with your actual data)
data_table = [
    # Example row: {'A': 'SOME_CODE', 'C': 'Cohort', 'D': datetime(2026, 7, 1), 'F': 'InstsPGR'}
    # Add your actual data rows here
    {'A': 'SOME_CODE', 'C': 'Cohort', 'D': datetime(2026, 7, 1), 'F': 'InstsPGR'},
    # ...
]

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except Exception:
        return None

def vlookup(value, table, col):
    for row in table:
        if row['A'] == value:
            return row.get(col)
    return None

def match(value, table):
    return any(row['A'] == value for row in table)

def edate(date_obj, months):
    return date_obj + relativedelta(months=months)

def first_of_month(date_obj):
    return date_obj.replace(day=1)

def get_cutoff_date(D2):
    # Replicates the nested IFs for D2 in the Excel formula
    cutoffs = [
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
    for cutoff, result in cutoffs:
        if D2 >= cutoff:
            return result
    return datetime(2025, 11, 1)

def process_data(data):
    A2 = data['A2']
    B2 = parse_date(data['B2'])
    C2 = parse_date(data['C2'])
    D2 = data['D2']
    E2 = parse_date(data['E2'])
    F2 = parse_date(data['F2'])

    # 1. Check for empty fields
    if not all([A2, C2, B2, F2]):
        return ""

    # 2. F2 > B2
    if F2 > B2:
        return "Not eligible, invoice past due"

    # 3. E2 < EDATE(F2, 8)
    if E2 is not None and F2 is not None and E2 < edate(F2, 8):
        return "Not eligible - less than eight months study remaining"

    # 4. A2 == "TFDE"
    if A2 == "TFDE":
        return "Instalments not available for deposit invoices"

    # 5. D2 == "2026-27 Entrant"
    if D2.strip() == "2026-27 Entrant":
        return "Not eligible - 2026-27 entrant"

    # 6. OR(MATCH/VLOOKUP logic)
    if match(A2, data_table):
        cohort = vlookup(A2, data_table, 'C')
        if cohort != "Cohort" and C2 > datetime(2026, 8, 29):
            return "Not eligible - 2026-27 entrant"

        # Cohort logic
        if cohort == "Cohort":
            D2_date = parse_date(D2) if parse_date(D2) else datetime(1900, 1, 1)
            cutoff_date = get_cutoff_date(D2_date)
            edate_b2_4 = edate(B2, 4)
            edate_b2_4_first = first_of_month(edate_b2_4)
            if cutoff_date > edate_b2_4_first:
                compare_date = cutoff_date
            else:
                compare_date = edate_b2_4_first

            edate_e2_minus6 = edate(E2, -6)
            edate_e2_minus6_first = first_of_month(edate_e2_minus6)
            if compare_date > edate_e2_minus6_first:
                schedule_date = edate_e2_minus6_first
            else:
                schedule_date = compare_date

            vlookup_d = vlookup(A2, data_table, 'D')
            if vlookup_d and schedule_date < F2:
                return "Option expired"

            vlookup_f = vlookup(A2, data_table, 'F')
            if vlookup_f == "InstsPGR":
                # Output: Insts + month of schedule_date + vlookup_f
                return f"Insts{schedule_date.strftime('%b')}{vlookup_f}"
            else:
                return "Instalment schedule not found, consult Team Leader"
        else:
            return "Instalment schedule not found, consult Team Leader"
    else:
        return "Instalment schedule not found, consult Team Leader"

def main():
    print("Enter the following values (YYYY-MM-DD for dates):")
    input_data = {}
    for col in ['A2', 'B2', 'C2', 'D2', 'E2', 'F2']:
        value = input(f"{col}: ")
        input_data[col] = value

    result = process_data(input_data)
    print(f"\nResult: {result}")

if __name__ == "__main__":
    main()